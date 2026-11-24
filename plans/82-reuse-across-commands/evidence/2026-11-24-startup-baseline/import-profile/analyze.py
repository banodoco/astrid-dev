import re,sys,json
def parse(path):
    rows=[]  # (self,cum,depth,name,idx)
    for line in open(path,errors="replace"):
        m=re.match(r"import time:\s+(\d+) \|\s+(\d+) \| (\s*)(\S+)",line)
        if m: rows.append((int(m[1]),int(m[2]),len(m[3])//2,m[4]))
    return rows
def importer(rows,i):
    d=rows[i][2]
    # importtime lists children before parent; the importer is the next later row with depth d-1
    for j in range(i+1,len(rows)):
        if rows[j][2]==d-1: return rows[j][3]
    return None
for run in sys.argv[1:]:
    rows=parse(run); out={"file":run,"modules":len(rows),"total_toplevel_s":round(sum(r[1] for r in rows if r[2]==0)/1e6,3)}
    # top 25 by cumulative, all depths, de-duplicate nested? report as is with depth+importer
    idx=sorted(range(len(rows)),key=lambda i:-rows[i][1])[:25]
    out["top25_cumulative"]=[(rows[i][3],round(rows[i][1]/1e6,3),rows[i][2],importer(rows,i)) for i in idx]
    targets=["astrid.core.execution.generic_host","vibecomfy.porting.emit.ui","astrid.core.generation.backends.comfy_schema","numpy"]
    out["targets"]={}
    for t in targets:
        for i,r in enumerate(rows):
            if r[3]==t:
                chain=[];k=i
                while k is not None and len(chain)<8:
                    nm=importer(rows,k); chain.append(nm)
                    k=next((j for j in range(k+1,len(rows)) if rows[j][3]==nm and rows[j][2]==rows[k][2]-1),None) if nm else None
                out["targets"][t]={"cum_s":round(r[1]/1e6,3),"self_s":round(r[0]/1e6,3),"depth":r[2],"importer_chain":chain}
                break
        else: out["targets"][t]="not loaded"
    print(json.dumps(out,indent=1))
