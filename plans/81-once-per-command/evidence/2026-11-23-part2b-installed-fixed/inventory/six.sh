export PYTHONHASHSEED=0
PY=/home/user/p81b/wt/pb2-review-fixes.env/bin/python
cd "$1"
for id in \
 "tests/test_ir_boundary_kpi.py::test_boundary_kpi_is_zero_ci_violations" \
 "tests/test_ir_laws.py::test_law_5_boundary_has_no_provisional_exceptions" \
 "tests/test_codemod_hypothesis.py::test_codemod_hypothesis_property_7_subgraph_materialization" \
 "tests/test_porting_edit_session.py::TestSeededPropertyFuzz::test_fuzz_landed_op_replay_is_deterministic" \
 "tests/test_demo_factory_multinode.py::test_all_multinode_fixtures_remove_exact_slice_without_dangling_links[M-35]" \
 "tests/test_demo_factory_multinode.py::test_all_multinode_fixtures_remove_exact_slice_without_dangling_links[M-36]"; do
 s=$(date +%s); $PY -m pytest -p no:cacheprovider -q "$id" 2>&1 | tail -3 | tr '\n' ' '; echo " [$(( $(date +%s)-s ))s] $id"
done
