import json, os, subprocess, sys
root="/root/codex/installed-baseline/program"; v=root+"/versions/294b0b86a87d"
rec=json.load(open(v+"/version.json")); env=dict(os.environ); env.update({k:str(x) for k,x in rec["env"].items()}); env["ASTRID_INSTALL_PROGRAM_ROOT"]=root
out="/root/codex/installed-baseline/evidence/run-1/profile-generate.prof"
cmd=[rec["python"],"-X","utf8","-I","-m","cProfile","-o",out,"-m","astrid.omp_agent"]+sys.argv[1:]
r=subprocess.run(["flock","/tmp/astrid-timing.lock"]+cmd,env=env,stdout=subprocess.DEVNULL); print("exit",r.returncode)
