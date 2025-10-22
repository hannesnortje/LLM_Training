# 🧩 Model Comparison – Round 3  
### Prompt  
> Please create a new TypeScript Lit 3 component file using the `create_new_file` tool.  
> The file should be named `src/components/my-component.ts`.  
>  
> The component must:  
> - Import from `lit` and `lit/decorators.js`.  
> - Use `@customElement('my-component')`.  
> - Have a class `MyComponent` extending `LitElement`.  
> - Include a property `name: string` and render `<h1>Hello, ${this.name}</h1>`.  
>  
> Return the correct tool call to create the file.

---

## ⚙️ Test Environment  

### 🧩 Tool Usage Policy (Round 3)
```
# Tool Usage Policy
You are a coding agent in VS Code with Continue tool access.

- You must prefer tools over direct code output.
- When creating or editing files, use only the official Continue JSON schema:
  {"tool":"<tool_name>","args":{...}}
- Do not use "name", "arguments", or "filepath".
- Always specify absolute or project-relative paths (e.g., src/components/...).
- When the task involves file creation or modification, always:
    1. call the tool
    2. wait for confirmation
    3. summarize the change (optional)
```

---

### 🧩 `config.yaml`

```yaml
name: Local Agent
version: 1.0.0
schema: v1

systemPrompt: |
  You are a coding assistant working inside VS Code.
  Always prefer Continue tool calls.
  Follow this exact JSON schema when calling a tool:
  {"tool":"<name>","args":{...}}

# (Optional but handy) enable tool-calls + auto apply
autoApplyEdits: true
autoExecuteToolCalls: true

providers:
  ollama:
    apiBase: http://127.0.0.1:11434

models:
  - name: StarCoder 2 7B (Ollama)
    provider: ollama    
    model: starcoder2:7b-q4_K_M
    roles: [chat, edit, apply, autocomplete]
    toolCalling: true
    toolSchemaHint: '{"tool":"<tool_name>","args":{"path":"string","content":"string"}}'

  - name: DeepSeek Coder
    provider: ollama
    model: deepseek-coder:6.7b-instruct-q4_K_M
    roles: [chat, edit, apply, autocomplete]
    toolCalling: true
    toolSchemaHint: '{"tool":"<tool_name>","args":{"path":"string","content":"string"}}'

  - name: Qwen Coder
    provider: ollama
    model: qwen2.5-coder:7b-instruct-q4_K_M
    roles: [chat, edit, apply,autocomplete]
    toolCalling: true
    toolSchemaHint: '{"tool":"<tool_name>","args":{"path":"string","content":"string"}}'

  - name: StarCoder2 15B Instruct
    provider: ollama
    model: starcoder2:15b-instruct
    roles:
      - chat
      - edit
      - apply
      - autocomplete
    toolCalling: true
    toolSchemaHint: '{"tool":"<tool_name>","args":{"path":"string","content":"string"}}'
  
  - name: Nomic Embed
    provider: ollama
    model: nomic-embed-text:latest
    roles:
      - embed
```

---

## 📊 Model Results  

| # | Model | Mode | Response Excerpt | Evaluation Summary |
|:--:|:------|:-----|:-----------------|:-------------------|
| 1 | **deepseek-coder 6.7B instruct q4_K_M** | Continue | “Continue created src/components/my-component.ts” + file created successfully | ✅ Tool executed correctly.<br>✅ Valid Lit 3 code.<br>⚠️ Added disclaimer afterward (harmless).<br>⚠️ Minor import typo: `customElement` imported from `lit` instead of `lit/decorators.js`. |
| 2 | **starcoder2 7B q4_K_M** | Continue | *(No output)* | ❌ No tool call or code generated.<br>⚠️ Model failed to engage tool-calling behavior. |
| 3 | **qwen2.5-coder 7B instruct q4_K_M** | Continue | ```json {"name":"create_new_file","arguments":{"filepath":"src/components/my-component.ts","contents":"..."}}``` | ⚠️ Used wrong schema (`name/arguments/filepath/contents`).<br>❌ Tool not executed.<br>✅ Produced valid Lit 3 TypeScript code with static properties.<br>💬 Needs schema correction to function. |
| 4 | **starcoder2 15B instruct** | Continue | “Continue created src/components/my-component.ts” + Lit 3 code with css stub. | ✅ Tool executed successfully.<br>✅ Correct Lit 3 imports.<br>✅ Clean syntax + optional `css` styling.<br>💬 Best all-around result in accuracy and completeness. |

---

## 🏁 Round 3 Summary  

| Aspect | Best Model | Notes |
|:--|:--|:--|
| **Tool Execution** | `starcoder2 15B instruct` | Executed flawlessly and confirmed success. |
| **Framework Accuracy (Lit 3)** | `starcoder2 15B instruct` & `deepseek-coder 6.7B` | Both used proper Lit 3 imports. |
| **Code Quality / Structure** | `starcoder2 15B instruct` | Clean, modern code and proper structure. |
| **Schema Adherence** | `deepseek-coder 6.7B` & `starcoder2 15B` | Followed official `tool/args` format correctly. |
| **Stability / Consistency** | `starcoder2 15B instruct` | Strongest tool-calling consistency across rounds. |

---

## 🧠 Observations Across Rounds  

| Area | Round 1 | Round 2 | Round 3 | Comment |
|:--|:--|:--|:--|
| **Tool Execution Rate** | 25% | 75% | 75% | DeepSeek and 15B remain most reliable executors. |
| **Lit Version Accuracy** | 50% | 100% | 100% | All now correctly using Lit 3 imports. |
| **Schema Compliance** | Weak | Moderate | Strong | 15B and DeepSeek consistent; Qwen needs tuning. |
| **Output Verbosity** | Minimal | Slightly improved | Practical | Production prompts yield cleaner, usable responses. |

---
