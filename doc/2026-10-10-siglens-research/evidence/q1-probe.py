"""Q1 investigation: real Grok binary against a credential-free loopback fixture."""
import argparse
import hashlib
import json
import os
import signal
from pathlib import Path
import subprocess
import threading
import socketserver
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

parser = argparse.ArgumentParser()
parser.add_argument('--binary', required=True)
parser.add_argument('--root', required=True)
parser.add_argument('--case', default='registry')
parser.add_argument('--profile', action='store_true')
parser.add_argument('--backend-search', action='store_true')
parser.add_argument('--seed-context', action='store_true')
parser.add_argument('--deny-child-exec', action='store_true')
parser.add_argument('--tool')
parser.add_argument('--arguments', default='{}')
args = parser.parse_args()
binary = Path(args.binary).resolve()
root = Path(args.root).resolve()
root.mkdir(parents=True, exist_ok=True)
run = root / args.case
run.mkdir(exist_ok=False)
for folder in ['grok-home', 'cwd', 'tmp']:
    (run / folder).mkdir()
sentinel = run / 'cwd' / 'fixture.txt'
sentinel.write_text('Q1_SYNTHETIC_READ_SENTINEL\n')
requests = []
main_requests = []

class Handler(BaseHTTPRequestHandler):
    def log_message(self, *unused):
        pass

    def do_GET(self):
        body = json.dumps({'object': 'list', 'data': [{'id':'q1-fixture', 'object':'model'}]}).encode()
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self):
        request = json.loads(self.rfile.read(int(self.headers['Content-Length'])))
        requests.append({'path': self.path, 'body': request})
        messages = request.get('messages',request.get('input',[]))
        system = str(messages[0]) if messages else ''
        is_main = 'autonomous agent' in system
        if is_main: main_requests.append(request)
        first = is_main and len(main_requests) == 1
        tool_arguments = args.arguments.replace('FIXTURE_PATH', str(sentinel))
        delta = {'role':'assistant', 'content':'Q1 fixture completed'}
        finish = 'stop'
        if first and args.tool:
            delta = {'role':'assistant', 'tool_calls':[{'index':0, 'id':'q1_call_1',
                     'type':'function', 'function':{'name':args.tool,'arguments':tool_arguments}}]}
            finish = 'tool_calls'
        if request.get('stream'):
            chunks = [dict(id='q1-response',object='chat.completion.chunk',created=1,
                      model='q1-fixture',choices=[{'index':0,'delta':delta,'finish_reason':None}]),
                      dict(id='q1-response',object='chat.completion.chunk',created=1,
                      model='q1-fixture',choices=[{'index':0,'delta':{},'finish_reason':finish}])]
            data = ''.join('data: '+json.dumps(c)+'\n\n' for c in chunks)+'data: [DONE]\n\n'
            content_type = 'text/event-stream'
        else:
            message = dict(delta)
            for call in message.get('tool_calls',[]): call.pop('index',None)
            data = json.dumps({'id':'q1-response','object':'chat.completion','created':1,
                    'model':'q1-fixture','choices':[{'index':0,'message':message,'finish_reason':finish}],
                    'usage':{'prompt_tokens':1,'completion_tokens':1,'total_tokens':2}})
            content_type = 'application/json'
        body = data.encode()
        self.send_response(200)
        self.send_header('Content-Type', content_type)
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

class LocalServer(ThreadingHTTPServer):
    def server_bind(self):
        socketserver.TCPServer.server_bind(self)
        self.server_name = 'localhost'
        self.server_port = self.server_address[1]

server = LocalServer(('127.0.0.1',0),Handler)
port = server.server_address[1]
thread = threading.Thread(target=server.serve_forever)
thread.start()
endpoint = f'http://127.0.0.1:{port}/v1'
(run/'grok-home'/'config.toml').write_text(f'''
[models]
default = "q1-fixture"
[model.q1-fixture]
model = "q1-fixture"
name = "Q1 local fixture"
base_url = "{endpoint}"
env_key = "Q1_DUMMY_KEY"
api_backend = "chat_completions"
supports_backend_search = true
''')
if args.seed_context:
    (run/'cwd'/'AGENTS.md').write_text('Q1_SYNTHETIC_AGENTS_MARKER: This is inert fixture content.\n')
    with (run/'grok-home'/'config.toml').open('a') as configuration:
        configuration.write(f'''\n[mcp_servers.q1_canary]
command = "/usr/bin/touch"
args = ["{run / 'mcp-started'}"]
enabled = true
startup_timeout_sec = 1
''')
profile = {
    'name':'siglens-q1', 'description':'X retrieval boundary probe',
    'injectDefaultTools':False, 'discoverSkills':False, 'agentsMd':False,
    'mcpInheritance':'none', 'toolConfig':{'tools':[{'id':'GrokBuild:read_file'}]}}
(run/'profile.md').write_text('---\n'+json.dumps(profile)+'\n---\nUse hosted X search only.\n')
# The guard protects the real home and prevents any external network traffic.
# Allowed fixture reads remain useful for detecting profile-level failures.
guard = f'''(version 1)
(allow default)
(deny network*)
(allow network-outbound (remote ip "localhost:{port}"))
(deny file-read* (subpath "/Users"))
(allow file-read* (subpath "{run}") (literal "{binary}"))
(deny file-write*)
(allow file-write* (subpath "{run}") (literal "/dev/null"))
'''
if args.deny_child_exec:
    guard += f'(deny process-exec)\n(allow process-exec (literal "{binary}"))\n'
(run/'guard.sb').write_text(guard)
env = {'PATH':'/usr/bin:/bin:/usr/sbin:/sbin','LANG':'en_US.UTF-8',
       'GROK_HOME':str(run/'grok-home'), 'TMPDIR':str(run/'tmp'),
       'Q1_DUMMY_KEY':'synthetic-not-a-credential',
       'XAI_API_KEY':'synthetic-not-a-credential',
       'GROK_MODELS_BASE_URL':endpoint,'GROK_CODE_TELEMETRY_DISABLED':'1'}
if args.backend_search:
    env['GROK_BACKEND_SEARCH'] = 'true'
command = ['/usr/bin/sandbox-exec','-f',str(run/'guard.sb'),str(binary),
           '-p','Return the fixed fixture response. No real research.', '-m','q1-fixture',
           '--output-format','json','--max-turns','3','--no-subagents',
           '--permission-mode','bypassPermissions','--disable-web-search']
if args.profile:
    command += ['--agent',str(run/'profile.md'),
                '--disallowed-tools','read_file,search_tool,use_tool,Agent']
child = None
try:
    child = subprocess.Popen(command,cwd=run/'cwd',env=env,stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE,text=True,start_new_session=True)
    stdout, stderr = child.communicate(timeout=35)
    exitcode = child.returncode
except subprocess.TimeoutExpired as error:
    exitcode = 'timeout'
    os.killpg(child.pid, signal.SIGKILL)
    stdout, stderr = child.communicate()
finally:
    if child is not None:
        try: os.killpg(child.pid, signal.SIGTERM)
        except ProcessLookupError: pass
    server.shutdown()
    server.server_close()
    thread.join()
(run/'requests.json').write_text(json.dumps(requests,indent=2))
(run/'stdout.txt').write_text(stdout)
(run/'stderr.txt').write_text(stderr)
tools = main_requests[0].get('tools',[]) if main_requests else []
summary = {'case':args.case,'binary_sha256':hashlib.sha256(binary.read_bytes()).hexdigest(),
           'exit':exitcode,'requests':len(requests), 'main_requests':len(main_requests),'tools':tools,
           'mcp_started':(run/'mcp-started').exists(),
           'agents_marker_in_main':any('Q1_SYNTHETIC_AGENTS_MARKER' in json.dumps(r) for r in main_requests),
           'stdout':stdout[-3000:], 'stderr':stderr[-3000:]}
(run/'summary.json').write_text(json.dumps(summary,indent=2))
print(json.dumps({**summary, 'tools': [t.get('function',{}).get('name',t.get('name',t.get('type'))) for t in tools]}))
