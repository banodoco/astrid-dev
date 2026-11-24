"""SV-L8 isolated CPU sample. Optional full Agent schema path; no product imports."""
import copy
import json
import statistics
import sys
import time
from collections import OrderedDict
from jsonschema import Draft202012Validator

# Exact transitive CommitRead definitions from Agent blob 8cf011bc52480db2ffbe0713516901acf8810244.
SCHEMA = json.loads(r'''{"$schema":"https://json-schema.org/draft/2020-12/schema","$id":"https://astrid.local/schemas/timeline/edit-command.schema.json","$ref":"#/$defs/CommitRead","$defs":{"CommitRead":{"oneOf":[{"type":"object","properties":{"ref":{"type":"string","pattern":"^(timeline|parent|(?:shot|shot-revision|internal|internal-revision):.+)$"},"path":{"type":"array","items":{"type":"string"}},"kind":{"const":"field"},"state":{"$ref":"#/$defs/AgentState"}},"required":["ref","path","kind","state"],"additionalProperties":false},{"type":"object","properties":{"ref":{"type":"string","pattern":"^(timeline|parent|(?:shot|shot-revision|internal|internal-revision):.+)$"},"path":{"type":"array","items":{"type":"string"}},"kind":{"const":"collection"},"members":{"type":"array","items":{"type":"string","minLength":1},"uniqueItems":true},"order":{"anyOf":[{"type":"null"},{"type":"array","items":{"type":"string","minLength":1},"uniqueItems":true}]}},"required":["ref","path","kind","members","order"],"additionalProperties":false},{"type":"object","properties":{"ref":{"type":"string","pattern":"^(timeline|parent|(?:shot|shot-revision|internal|internal-revision):.+)$"},"path":{"const":[]},"kind":{"const":"scope"}},"required":["ref","path","kind"],"additionalProperties":false}]},"AgentState":{"type":"object","oneOf":[{"required":["state"],"properties":{"state":{"const":"absent"}},"additionalProperties":false},{"required":["state","value"],"properties":{"state":{"const":"present"},"value":{"$ref":"#/$defs/JSON"}},"additionalProperties":false}]},"JSON":{"description":"Only finite JSON enters validation; transport rejects duplicate keys and non-finite numeric tokens before schema validation.","anyOf":[{"type":["null","boolean","number","string"]},{"type":"array","items":{"$ref":"#/$defs/JSON"}},{"type":"object","additionalProperties":{"$ref":"#/$defs/JSON"}}]}}}''')
if len(sys.argv) > 1:
    with open(sys.argv[1]) as f:
        full = json.load(f)
    assert all(full['$defs'][k] == v for k, v in SCHEMA['$defs'].items())
    SCHEMA = {**full, '$ref': '#/$defs/CommitRead'}

class CommandError(Exception):
    pass

def strict_json(value):
    pending = [value]
    while pending:
        item = pending.pop()
        t = type(item)
        if t is dict:
            if any(type(k) is not str for k in item):
                return False
            pending.extend(item.values())
        elif t is list:
            pending.extend(item)
        elif t not in (str, int, float, bool, type(None)):
            return False
    return True

def validate_reads(reads, memo=None, counts=None):
    # Baseline is the Agent validate_reads body; candidate changes only schema dispatch.
    validator = Draft202012Validator(SCHEMA)
    if not isinstance(reads, list):
        raise CommandError('reads must be an array')
    for read in reads:
        try:
            encoded = json.dumps(read, allow_nan=False)
        except (ValueError, TypeError) as exc:
            raise CommandError('reads must contain finite JSON') from exc
        # ASCII escaping aliases a supplementary character and a literal surrogate pair.
        # Keep the original finite check, then use the exact Unicode JSON string as key.
        key = (json.dumps(read, allow_nan=False, ensure_ascii=False)
               if memo is not None and len(encoded) <= 16384 and strict_json(read) else None)
        if key is None or key not in memo:
            if counts is not None:
                counts[0] += 1
            errors = list(validator.iter_errors(read))
            if errors:
                raise CommandError(errors[0].message)
            if key is not None:
                memo[key] = True
                if len(memo) > 1024:
                    memo.popitem(last=False)
        elif counts is not None:
            counts[1] += 1
        if read['ref'] == 'timeline' and read['kind'] != 'scope':
            raise CommandError('timeline is a read-only closure scope')
        if read['kind'] == 'collection' and (read['members'] != sorted(read['members'])
                or read['order'] is not None and set(read['order']) != set(read['members'])):
            raise CommandError('collection members/order must describe the same unique IDs')

def field(i, value=None):
    return {'ref': f'shot:s{i}', 'path': ['config'], 'kind': 'field', 'state': {'state': 'present', 'value': value}}

def outcome(reads, memo):
    before = repr(reads)
    try:
        validate_reads(reads, memo)
        result = ('accepted', None)
    except Exception as exc:
        result = (type(exc).__name__, str(exc))
    assert repr(reads) == before
    return result

scope = {'ref':'timeline','path':[],'kind':'scope'}
collection = {'ref':'parent','path':['clips'],'kind':'collection','members':['a','b'],'order':['b','a']}
valid = [field(1, {'nested':[True, 1, 1.0, None, 'x']}), scope, collection,
         {**field(2), 'state': {'state':'absent'}}]
cases = [valid, copy.deepcopy(valid), [], {}, [field(1, float('nan'))], [field(1, float('inf'))],
         [field(1, (1,2))], [field(1, {1:'x'})], [field(1, {True:'x'})],
         [{**field(1), 'ref':'timeline'}], [{**scope,'path':['x']}],
         [{**collection,'members':['b','a']}], [{**collection,'order':['a','c']}],
         [{**collection,'members':['a','a']}], [{**field(1),'path':[1]}],
         [{**field(1),'extra':1}], [{**field(1),'state':{'state':'present'}}],
         [{**field(1),'state':{'state':'absent','value':None}}], [field(1, -0.0)], [field(1, 0.0)],
         [field(1, True)], [field(1, 1)], [field(1, 1.0)], [field(1, {'1':'x'})],
         [{**field(1), 'ref':'invalid'}], [field(1, 'x'*17000)]]
cycle=[]; cycle.append(cycle); cases.append([field(1,cycle)])
# ASCII JSON aliases the two Unicode forms; the duplicate must still refuse.
paired = '\ud83d\ude00'; scalar = '\U0001f600'
assert paired != scalar and json.dumps(paired) == json.dumps(scalar)
cases.extend([[{**collection, 'members':[paired,scalar], 'order':None}],
              [{**collection, 'members':[scalar,scalar], 'order':None}]])
# Warm successes, then changed and invalid values; compare exact exception text, not counts.
memo=OrderedDict(); accepted=refused=0
for reads in cases + list(reversed(cases)):
    a=outcome(reads,None); b=outcome(reads,memo); assert a==b,(a,b)
    accepted += a[0]=='accepted'; refused += a[0]!='accepted'
# Mutate the same read after a hit; distinct bytes must be checked again.
mutated=field(99, {'v':1}); assert outcome([mutated],memo)==('accepted',None)
mutated['path']=[1]; assert outcome([mutated],memo)==outcome([mutated],None)
# Verify boundedness and eviction do not hide a later invalid read.
large=OrderedDict()
validate_reads([field(i,i) for i in range(1025)],large)
assert len(large)==1024 and outcome([field(0,0)],large)==('accepted',None)
assert len(large)==1024
print(f'differential: {accepted} accepted, {refused} refused; exact outcomes and unchanged inputs; mutation checked')
for overlap in (False, True):
    first=[field(i, {'clip':i,'nested':[0,1,None,True]}) for i in range(300)]
    second=copy.deepcopy(first) if overlap else [field(i+300, {'clip':i,'nested':[0,1,None,True]}) for i in range(300)]
    times=[]
    for cached in (False, True):
        samples=[]
        for _ in range(5):
            memo=OrderedDict() if cached else None; counts=[0,0]; start=time.perf_counter()
            validate_reads(first,memo,counts); validate_reads(second,memo,counts)
            samples.append(time.perf_counter()-start)
        times.append(round(statistics.median(samples)*1000,2))
        print(f'overlap={overlap} cached={cached} checks={counts[0]} hits={counts[1]} median_ms={times[-1]}')
