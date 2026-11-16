import ast
import subprocess
from pathlib import Path

BASE = "6c06460d3e7b46001f9d57e5b011cb114bfa23d0"
TARGETS = {
    "tests/core/pack/test_cli_manage.py": {"test_implicit_descriptor_refuses_writable_and_aliases"},
    "tests/core/pack/test_git_environment.py": {
        "test_planted_ssh_in_working_directory_never_runs",
        "test_recorded_git_that_lost_its_execute_bit_falls_back_to_absolute_path_lookup",
    },
    "tests/test_installer_pack_cleanup.py": {"test_posix_failed_removal_never_chmods_a_symlink_target_outside_the_tree"},
    "tests/test_installer_sources.py": {
        "test_missing_runtime_lock_names_the_missing_path_not_aliasing",
        "test_missing_candidate_or_product_root_directory_is_named",
    },
}

def function_nodes(source):
    tree = ast.parse(source)
    return {n.name: n for n in ast.walk(tree) if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))}

def normalized_function(node):
    node = ast.fix_missing_locations(ast.parse(ast.unparse(node)).body[0])
    normalized = []
    for decorator in node.decorator_list:
        text = ast.unparse(decorator)
        if text.startswith("pytest.mark.skipif(os.name") or text == "pytest.mark.posix_native":
            normalized.append(ast.Name(id="POSIX_NATIVE_MARK", ctx=ast.Load()))
        else:
            normalized.append(decorator)
    node.decorator_list = normalized
    return ast.dump(node, include_attributes=False)

for path, names in TARGETS.items():
    before = subprocess.check_output(["git", "show", f"{BASE}:{path}"], text=True)
    after = Path(path).read_text()
    old_nodes, new_nodes = function_nodes(before), function_nodes(after)
    for name in sorted(names):
        assert name in old_nodes and name in new_nodes, (path, name)
        assert normalized_function(old_nodes[name]) == normalized_function(new_nodes[name]), (path, name)
        assert len(old_nodes[name].decorator_list) == len(new_nodes[name].decorator_list), (path, name)
        print(f"PASS {path}::{name}: signature, body, and all decorators except POSIX marker identical")
