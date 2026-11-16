import ast
import copy
import json
from pathlib import Path

repo = Path('/workspace/scratch/cd53b069f320/p39-repair/astrid-agent')
evidence = Path('/workspace/scratch/cd53b069f320/p39-g2-evidence/agent/k1a-posix-parameters')
files = {
    'tests/core/generation/test_model_verification_record.py': 'test_non_utf8_filename_hashes_then_reuses',
    'tests/core/pack/test_verified_relocations.py': 'test_forged_personal_relocation_is_rejected',
    'tests/packs/runpod/test_failure_diagnostics.py': {
        'test_bounded_observer_rejects_malformed_or_late_child_frame',
        'test_partial_ipc_from_unkillable_caller_returns_with_pending_fence',
    },
}

def target_functions(tree, expected):
    return {node.name: node for node in tree.body if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name in (expected if isinstance(expected, set) else {expected})}

def is_pytest_skip(node):
    return isinstance(node, ast.Expr) and isinstance(node.value, ast.Call) and isinstance(node.value.func, ast.Attribute) and isinstance(node.value.func.value, ast.Name) and node.value.func.value.id == 'pytest' and node.value.func.attr == 'skip'

def normalize_function(path, name, node, side):
    node = copy.deepcopy(node)
    # Gate decorators are deliberately compared by the separately recorded diff and collected IDs.
    node.decorator_list = []
    if name == 'test_non_utf8_filename_hashes_then_reuses' and side == 'before':
        node.body = [stmt for stmt in node.body if not (isinstance(stmt, ast.If) and isinstance(stmt.test, ast.Compare) and isinstance(stmt.test.left, ast.Attribute) and isinstance(stmt.test.left.value, ast.Name) and stmt.test.left.value.id == 'os' and stmt.test.left.attr == 'name' and is_pytest_skip(stmt.body[0]))]
    if name == 'test_forged_personal_relocation_is_rejected':
        class RemoveWindowsSkip(ast.NodeTransformer):
            def visit_If(self, candidate):
                candidate = self.generic_visit(candidate)
                if (isinstance(candidate.test, ast.Compare) and isinstance(candidate.test.left, ast.Attribute)
                        and isinstance(candidate.test.left.value, ast.Name) and candidate.test.left.value.id == 'sys'
                        and candidate.test.left.attr == 'platform' and is_pytest_skip(candidate.body[0])):
                    return None
                return candidate
        node = RemoveWindowsSkip().visit(node)
    return node

results = {}
for rel, spec in files.items():
    before = ast.parse((evidence / 'before' / Path(rel).name).read_text())
    after = ast.parse((repo / rel).read_text())
    expected = spec if isinstance(spec, set) else {spec}
    bfunc = target_functions(before, expected)
    afunc = target_functions(after, expected)
    assert bfunc.keys() == afunc.keys() == expected, (rel, bfunc.keys(), afunc.keys(), expected)
    # Compare complete module AST after replacing only the target test definitions with normalized forms.
    for tree, funcs, side in ((before, bfunc, 'before'), (after, afunc, 'after')):
        for i, node in enumerate(tree.body):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name in expected:
                tree.body[i] = normalize_function(rel, node.name, node, side)
    assert ast.dump(before, include_attributes=False) == ast.dump(after, include_attributes=False), rel
    results[rel] = {'module_ast_equal_after_gate_normalization': True, 'target_functions': sorted(expected)}

# Explicit parameter identity check: only the public case receives the lane mark; all original cases remain.
rel = 'tests/core/pack/test_verified_relocations.py'
tree = ast.parse((repo / rel).read_text())
fn = target_functions(tree, 'test_forged_personal_relocation_is_rejected')['test_forged_personal_relocation_is_rejected']
param = next(d for d in fn.decorator_list if isinstance(d, ast.Call) and ast.unparse(d.func) == 'pytest.mark.parametrize')
items = param.args[1].elts
ids = [ast.literal_eval(x) if isinstance(x, ast.Constant) else ast.literal_eval(x.args[0]) for x in items]
assert ids == ['original', 'selection', 'digest', 'reused', 'outside', 'public'], ids
public = items[-1]
assert isinstance(public, ast.Call) and len(public.keywords) == 1 and ast.unparse(public.keywords[0].value) == 'pytest.mark.posix_native'
results['verified_relocations_parameter_ids'] = ids
results['verified_relocations_public_parameter_mark'] = 'pytest.mark.posix_native'
(evidence / 'ast-equivalence.json').write_text(json.dumps(results, indent=2) + '\n')
print(json.dumps(results, indent=2))
