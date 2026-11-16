import ast, copy, json
from pathlib import Path
repo=Path('/workspace/scratch/cd53b069f320/p39-repair/astrid-agent')
evidence=Path('/workspace/scratch/cd53b069f320/p39-g2-evidence/agent/k1a-posix-recovery')
targets={
 'tests/test_boundary_registration_launchd.py': {'test_launchd_sigkill_after_publication_link_replays'},
 'tests/test_installer_r0_stop.py': {'test_killed_after_disable_next_invocation_recovers','test_launchd_sigkill_at_each_stop_step_then_recover'},
}
def skip_expr(stmt):
 return (isinstance(stmt,ast.Expr) and isinstance(stmt.value,ast.Call) and isinstance(stmt.value.func,ast.Attribute)
         and isinstance(stmt.value.func.value,ast.Name) and stmt.value.func.value.id=='pytest' and stmt.value.func.attr=='skip')
def normalize(tree, names, side):
 tree=copy.deepcopy(tree)
 for i,node in enumerate(tree.body):
  if isinstance(node,ast.FunctionDef) and node.name in names:
   node.decorator_list=[]
   if side=='before' and node.name in {'test_killed_after_disable_next_invocation_recovers','test_launchd_sigkill_at_each_stop_step_then_recover'}:
    node.body=[s for s in node.body if not (isinstance(s,ast.If) and isinstance(s.test,ast.UnaryOp) and isinstance(s.test.op,ast.Not)
             and isinstance(s.test.operand,ast.Call) and isinstance(s.test.operand.func,ast.Name) and s.test.operand.func.id=='hasattr' and skip_expr(s.body[0]))]
 return tree
results={}
for rel,names in targets.items():
 before=ast.parse((evidence/'before'/Path(rel).name).read_text())
 after=ast.parse((repo/rel).read_text())
 assert ast.dump(normalize(before,names,'before'),include_attributes=False)==ast.dump(normalize(after,names,'after'),include_attributes=False),rel
 results[rel]={'module_ast_equal_after_gate_normalization':True,'target_functions':sorted(names)}
(evidence/'ast-equivalence.json').write_text(json.dumps(results,indent=2)+'\n')
print(json.dumps(results,indent=2))
