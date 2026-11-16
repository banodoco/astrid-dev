"""Focused reproduction of the LS-6 hash test from Agent cb1a590e.

Only its settled_media fixture and named test are copied; the product modules
are the actual recovered candidate modules. This is not the whole original file.
"""
import hashlib
import io
import json
from pathlib import Path
from types import SimpleNamespace
from tests._local_speed_hashes import OutputHashObserver
from astrid.core.generation.backends.comfy_target import ComfyTarget, ComfyTargetClient

def sha(data): return hashlib.sha256(data).hexdigest()

def settled_media(*,filenames=("one.png","two.png")):
    from astrid.sdk.remote import RemoteMedia
    objects,metadata,outputs,rows={},{},[],[]
    metadata=[]
    for index,filename in enumerate(filenames):
        data=f"output {index}".encode(); digest="sha256:"+sha(data)
        objects[digest]=data
        row={"object_id":digest,"digest":digest,"size":len(data),"filename":filename,
             "media_type":"image/png","role":"result","project_id":"project-1"}
        rows.append(row); metadata.append(row)
        outputs.append({"sha256":sha(data),"bytes":len(data),"path":filename})
    manifest=json.dumps({"outputs":outputs}).encode(); reference="sha256:"+sha(manifest)
    objects[reference]=manifest
    metadata.append({"object_id":reference,"size":len(manifest),"filename":"manifest.json","media_type":"application/json"})
    transport=SimpleNamespace(get_object=lambda digest:{"data":objects[digest]},
        list_project_objects=lambda project,**kwargs:(metadata,None))
    payload={"task_id":"task-1","manifest_ref":reference,"manifest":{"outputs":rows},"image_paths":[],"run_dir":None}
    return SimpleNamespace(payload=payload,rows=rows,objects=objects,client=SimpleNamespace(media=RemoteMedia(transport)))

def test_output_hash_passes_across_download_host_runtime_and_delivery(tmp_path,monkeypatch):
    from astrid.core._shared.result_manifest import harvest_staged_outputs
    from astrid.core.execution.generic_host import GenericPackHost, RuntimeProtocolClient
    from astrid.core.generation.delivery import deliver_generation
    from runtime_protocol.service import RuntimeService
    from runtime_protocol.store import RealmStore
    runtime=settled_media(filenames=("one.png",)); data=b"output 0"; digest="sha256:"+sha(data)
    root=tmp_path/"attempt"; output_root=root/"outputs"; output_root.mkdir(parents=True)
    path=output_root/"one.png"
    observer=OutputHashObserver({digest.removeprefix("sha256:"):len(data)}).install(monkeypatch)
    def count(): return observer.snapshot().completed_streams
    def phase(name):
        state=observer.snapshot()
        print("HASH_PHASE",json.dumps({"phase":name,"streams":state.completed_streams,"bytes":state.bytes_hashed,"gaps":state.coverage_gaps}))
    class Response(io.BytesIO):
        status=200; headers={"Content-Length":str(len(data))}
    client=ComfyTargetClient(ComfyTarget("http://127.0.0.1:8188","attached"),opener=lambda *_args,**_kwargs:Response(data))
    client.download_output({"filename":"one.png","subfolder":"","type":"output"},path)
    phase("download"); assert count()==1
    declared=SimpleNamespace(name="result",path_template="one.png",artifact_type="image/png")
    record=SimpleNamespace(definition=SimpleNamespace(outputs=(declared,),metadata={}))
    (output_root/"manifest.json").write_text(json.dumps({"outputs":[{"name":"result","path":"one.png","content_hash":digest,"bytes":len(data)}]}))
    harvested=harvest_staged_outputs(output_root,declared_outputs=(declared,))
    phase("harvest"); assert count()==2
    host=object.__new__(GenericPackHost); host.client=object.__new__(RuntimeProtocolClient)
    typed=host._typed_outputs(record,harvested,root,defer_content_check_to_runtime=True)
    outputs=host._upload_outputs(typed,project_id=None)
    phase("host"); assert count()==2
    assert outputs[0]["digest"]==digest
    realm=tmp_path/"realm"; RealmStore.initialize(realm).close(); service=RuntimeService(realm)
    try:
        before=count(); service._stage_outputs("attempt-1",outputs)
        phase("runtime"); assert count()>before
    finally: service.close()
    before=count()
    result=deliver_generation(runtime.payload,client=runtime.client,out=tmp_path/"delivered.png")
    assert Path(result["image_paths"][0]).read_bytes()==data
    phase("delivery")
    assert count()-before==3
