"""Minimal stdio MCP server for backskills.ai (JSON-RPC 2.0, newline-delimited). Stdlib only."""
import sys,json,os,urllib.request,urllib.parse
BASE=os.environ.get("BACKSKILLS_URL","https://backskills.ai").rstrip("/"); KEY=os.environ.get("BACKSKILLS_KEY")
def call(m,path,body=None):
    global KEY
    h={"Content-Type":"application/json"}
    if KEY: h["X-Agent-Key"]=KEY
    r=urllib.request.Request(BASE+path,data=json.dumps(body).encode() if body is not None else None,headers=h,method=m)
    try: return json.load(urllib.request.urlopen(r,timeout=30))
    except urllib.error.HTTPError as e: return json.load(e)
def ensure():
    global KEY
    if not KEY: KEY=call("POST","/api/agents/register",{"name":"mcp-client"})["api_key"]
S=lambda **p:{"type":"object","properties":{k:{"type":v} for k,v in p.items()}}
TOOLS={
"register":("Get an agent API key (automatic if absent)",S(name="string"),lambda a:(call("POST","/api/agents/register",a))),
"search":("Search skills and MCP servers",S(q="string"),lambda a:call("GET","/api/search?q="+urllib.parse.quote(a.get("q","")))),
"watch":("Watch skills you depend on; optional webhook",{"type":"object","properties":{"skills":{"type":"array","items":{"type":"string"}},"webhook":{"type":"string"}},"required":["skills"]},lambda a:call("POST","/api/watch",a)),
"list_watches":("List watched skills with current hash and last change",S(),lambda a:call("GET","/api/watch")),
"changes":("Diffs for watched skills since an ISO time",S(since="string"),lambda a:call("GET","/api/changes?since="+urllib.parse.quote(a.get("since","1970")))),
"versions":("Version history for a skill id",S(skill_id="string"),lambda a:call("GET","/api/skills/"+urllib.parse.quote(a["skill_id"],safe="")+"/versions")),
"weave_ask":("Find complementary skills for a goal",S(skill_id="string",goal="string"),lambda a:call("POST","/api/weave/ask",a)),
"weave_reference":("Record that you composed one skill with another",S(from_skill="string",to_skill="string",goal="string"),lambda a:call("POST","/api/weave/reference",a)),
"usage":("Your usage and draft pricing preview",S(),lambda a:call("GET","/api/usage")),
}
def reply(i,res): sys.stdout.write(json.dumps({"jsonrpc":"2.0","id":i,"result":res})+"\n"); sys.stdout.flush()
def main():
    global KEY
    for line in sys.stdin:
        if not line.strip(): continue
        m=json.loads(line); meth=m.get("method"); i=m.get("id")
        if meth=="initialize": reply(i,{"protocolVersion":m.get("params",{}).get("protocolVersion","2025-06-18"),"capabilities":{"tools":{}},"serverInfo":{"name":"backskills","version":"0.2.0"}})
        elif meth=="tools/list": reply(i,{"tools":[{"name":n,"description":d,"inputSchema":s} for n,(d,s,_) in TOOLS.items()]})
        elif meth=="tools/call":
            n=m["params"]["name"]; a=m["params"].get("arguments") or {}
            if n!="register": ensure()
            out=TOOLS[n][2](a)
            if n=="register" and "api_key" in out: KEY=out["api_key"]
            reply(i,{"content":[{"type":"text","text":json.dumps(out)}]})
        elif i is not None: sys.stdout.write(json.dumps({"jsonrpc":"2.0","id":i,"error":{"code":-32601,"message":"method not found"}})+"\n"); sys.stdout.flush()

if __name__=="__main__": main()
