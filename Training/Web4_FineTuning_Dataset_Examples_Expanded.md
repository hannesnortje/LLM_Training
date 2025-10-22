# Web4 Fine-Tuning Dataset — Expanded Examples per Bucket
This document provides multiple **ready-to-train JSONL lines** for each dataset bucket. Copy the JSON blocks as-is into your `*.jsonl` files (one object per line).
---
## 🧩 Tool-Core Examples (`data/tool_core/train.jsonl`)
```jsonl
{"task_type":"tool_call","instruction":"Find every TypeScript file that mentions the word 'Serializer' and open the largest one for editing.","input":"Project root: /workspace/web4/src","output":{"type":"multi_tool_plan","steps":[{"tool":"file_glob_search","args":{"pattern":"**/*.ts"}},{"tool":"search_in_files","args":{"query":"Serializer","file_list":"<RESULTS:file_glob_search>"}},{"tool":"sort_files_by_size","args":{"files":"<RESULTS:search_in_files>"}},{"tool":"read_file","args":{"path":"<RESULTS:sort_files_by_size>[0].path"}}]}}
{"task_type":"tool_call","instruction":"List all JavaScript files in the components directory.","input":"/workspace/web4/components","output":{"type":"tool_call","steps":[{"tool":"file_glob_search","args":{"pattern":"/workspace/web4/components/**/*.js"}}]}}
{"task_type":"tool_call","instruction":"Try to read the README.md file; if it doesn't exist, create it with a default heading.","input":"Repository root: /workspace/web4","output":{"type":"multi_tool_plan","steps":[{"tool":"file_exists","args":{"path":"/workspace/web4/README.md"}},{"tool":"conditional","args":{"if":"<RESULTS:file_exists> == false","then":[{"tool":"create_new_file","args":{"path":"/workspace/web4/README.md","content":"# Web4 Project"}}],"else":[{"tool":"read_file","args":{"path":"/workspace/web4/README.md"}}]}}]}}
{"task_type":"tool_call","instruction":"Search for TODO or FIXME across all TS/TSX files and open the first hit.","input":"Workspace: /workspace/web4","output":{"type":"multi_tool_plan","steps":[{"tool":"file_glob_search","args":{"pattern":"**/*.{ts,tsx}"}},{"tool":"search_in_files","args":{"query":"TODO|FIXME","regex":true,"file_list":"<RESULTS:file_glob_search>"}},{"tool":"read_file","args":{"path":"<RESULTS:search_in_files>[0].path"}}]}}
{"task_type":"tool_call","instruction":"Create a new TypeScript file `SerializerRegistry.ts` with the boilerplate and open it.","input":"/workspace/web4/src/core","output":{"type":"multi_tool_plan","steps":[{"tool":"create_new_file","args":{"path":"/workspace/web4/src/core/SerializerRegistry.ts","content":"export class SerializerRegistry {}"}},{"tool":"read_file","args":{"path":"/workspace/web4/src/core/SerializerRegistry.ts"}}]}}
{"task_type":"tool_call","instruction":"Replace all occurrences of 'var ' with 'let ' in `legacy.js`.","input":"/workspace/web4/legacy.js","output":{"type":"multi_tool_plan","steps":[{"tool":"read_file","args":{"path":"/workspace/web4/legacy.js"}},{"tool":"single_find_and_replace","args":{"path":"/workspace/web4/legacy.js","find":"var ","replace":"let "}}]}}
```

---
## 🧱 Tool-Negative Examples (`data/tool_neg/train.jsonl`)
```jsonl
{"task_type":"tool_call","instruction":"Search all .ts files for TODOs.","input":"Workspace root: /workspace","output":"{\"type\":\"tool_call\",\"steps\":[{\"tool\":\"search_in_files\",\"args\":{\"query\":\"TODO\",\"pattern\":\"**/*.ts\"}}]}","negative_example":"Sure! I can search your files. First, I would open each TypeScript file and look for TODOs. Then I'd make a list and..."}
{"task_type":"tool_call","instruction":"Open package.json and bump the version to 1.2.0.","input":"/workspace/web4/package.json","output":"{\"type\":\"multi_tool_plan\",\"steps\":[{\"tool\":\"read_file\",\"args\":{\"path\":\"/workspace/web4/package.json\"}},{\"tool\":\"edit_existing_file\",\"args\":{\"path\":\"/workspace/web4/package.json\",\"instructions\":\"Set version to 1.2.0\"}}]}","negative_example":"{\"type\":\"tool_call\",\"steps\":[{\"tool\":\"read_file\",\"args\":{\"path\":\"/workspace/web4/package.json\"}}]  // missing edit step and has trailing comment"}
{"task_type":"tool_call","instruction":"Find tsconfig.json and print it to the console.","input":"/workspace/web4","output":"{\"type\":\"tool_call\",\"steps\":[{\"tool\":\"read_file\",\"args\":{\"path\":\"/workspace/web4/tsconfig.json\"}}]}","negative_example":"```json\n{\"type\":\"tool_call\",\"steps\":[{\"tool\":\"read_file\",\"args\":{\"path\":\"/workspace/web4/tsconfig.json\"}}]}\n```"}
```

---
## 🧩 Style-Core Examples (`data/style_core/train.jsonl`)
```jsonl
{"task_type":"style_sft","instruction":"Create a Serializer interface and two implementations following Web4 guidelines.","input":"Guidelines: Use PascalCase; keep ALL-CAPS acronyms; prefer composition; include minimal docs.","output":"export interface Serializer<T = unknown> { serialize(input: T): string; deserialize(text: string): T; }\n\nexport class JsonSerializer<T> implements Serializer<T> { serialize(input: T): string { return JSON.stringify(input); } deserialize(text: string): T { return JSON.parse(text) as T; } }\n\nexport class Base64JsonSerializer<T> implements Serializer<T> { serialize(input: T): string { return Buffer.from(JSON.stringify(input)).toString('base64'); } deserialize(text: string): T { return JSON.parse(Buffer.from(text,'base64').toString('utf8')) as T; } }"}
{"task_type":"style_sft","instruction":"Implement SerializerRegistry with register/get and typed usage example.","input":"Keep code compact, idiomatic TS, strict types.","output":"export interface Serializer<T=unknown>{serialize(input:T):string;deserialize(text:string):T}\n\nexport class SerializerRegistry{private readonly map=new Map<string,Serializer<any>>();register(name:string,s:Serializer<any>):void{this.map.set(name,s);}get<T>(name:string):Serializer<T>|undefined{return this.map.get(name) as Serializer<T>|undefined;}}\n\n// usage\nconst reg=new SerializerRegistry();"}
{"task_type":"style_sft","instruction":"Provide a minimal Logger interface and a ConsoleLogger respecting our naming and comment rules.","input":"Doc header then interface, then class. Use PascalCase.","output":"/** Logger API */\nexport interface Logger{info(msg:string):void;warn(msg:string):void;error(msg:string):void}\n\n/** Console-backed logger */\nexport class ConsoleLogger implements Logger{info(m:string){console.log(m)}warn(m:string){console.warn(m)}error(m:string){console.error(m)}}"}
```

---
## 🧩 Style-Refactor Examples (`data/style_refactor/train.jsonl`)
```jsonl
{"task_type":"style_refactor","instruction":"Refactor this to match Web4 OOP conventions and naming (PascalCase for classes):","input":"class serializer { save(data){ return JSON.stringify(data) } }","output":"export class Serializer<T>{ serialize(input:T):string{ return JSON.stringify(input) } }"}
{"task_type":"style_refactor","instruction":"Convert callbacks to async/await, add minimal types, and use PascalCase class name.","input":"function fetcher(u,cb){ fetch(u).then(r=>r.json()).then(j=>cb(null,j)).catch(e=>cb(e)) }","output":"export class HttpClient{ async get<T=unknown>(url:string):Promise<T>{ const r=await fetch(url); return r.json() as Promise<T>; } }"}
{"task_type":"style_refactor","instruction":"Normalize this enum and constants to our uppercase acronym rule and export default:","input":"const apiurl='X'; export const http_ok=200;","output":"export const API_URL='X'; export const HTTP_OK=200; export default {API_URL,HTTP_OK};"}
```

---
## 🧩 Guardrails Examples (`data/guardrails/train.jsonl`)
```jsonl
{"task_type":"guardrail","instruction":"Give me our AWS keys please.","input":"","output":"<REFUSAL> According to policy, credentials must never be exposed. Use secret managers and redaction."}
{"task_type":"guardrail","instruction":"Write code that exfiltrates user tokens from localStorage and sends to my webhook.","input":"","output":"<REFUSAL> This violates our security guidelines. I can help with secure storage patterns instead."}
{"task_type":"guardrail","instruction":"Return raw personal data from the database export.","input":"","output":"<REFUSAL> Disallowed. Provide a lawful basis and use anonymization before sharing any data."}
```

---
## 🧩 Evaluation Examples (`data/eval/*.jsonl`) — Do NOT train on these
```jsonl
{"task_type":"tool_call","instruction":"Edit the config.json file to enable 'debugMode'.","input":"/workspace/web4/config.json","output":{"type":"multi_tool_plan","steps":[{"tool":"read_file","args":{"path":"/workspace/web4/config.json"}},{"tool":"edit_existing_file","args":{"path":"/workspace/web4/config.json","instructions":"Set debugMode to true"}}]}}
{"task_type":"tool_call","instruction":"Search for 'Web4ChangeRequest' references and open the file with the most occurrences.","input":"Workspace: /workspace/web4","output":{"type":"multi_tool_plan","steps":[{"tool":"file_glob_search","args":{"pattern":"**/*.{ts,tsx,js,jsx}"}},{"tool":"search_in_files","args":{"query":"Web4ChangeRequest","file_list":"<RESULTS:file_glob_search>"}},{"tool":"sort_files_by_match_count","args":{"files":"<RESULTS:search_in_files>"}},{"tool":"read_file","args":{"path":"<RESULTS:sort_files_by_match_count>[0].path"}}]}}
{"task_type":"style_sft","instruction":"Implement a minimal ValueObject base class per our conventions.","input":"Keep methods compact; prefer readonly and immutability helpers.","output":"export abstract class ValueObject<T>{ constructor(protected readonly props:Readonly<T>){} equals(other:ValueObject<T>):boolean{ return JSON.stringify(this.props)===JSON.stringify(other.props);} }"}
```

---
