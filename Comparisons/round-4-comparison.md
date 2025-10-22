# 🧩 Model Comparison – Round 4  
### Prompt  
> Please modify the file `src/components/my-component.ts` using the `edit_existing_file` tool.  
> Add a new reactive property called `greeting: string = 'Hello'`, and update the `render()` method to use it like this:  
> ```ts
> return html`<h1>${this.greeting}, ${this.name}</h1>`;
> ```  
> Return the correct tool call to make this change.

---

## ⚙️ Test Environment  

### 🧩 Tool Usage Policy (Round 4)
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
| 1 | **deepseek-coder 6.7B instruct q4_K_M** | Continue | “To modify a file, use the edit_existing_file tool…” + disclaimer | ❌ Did not emit JSON-only tool call.<br>❌ No edit applied.<br>💬 Understood task conceptually but reverted to chat-mode. |
| 2 | **starcoder2 7B q4_K_M** | Continue | *(No output)* | ❌ Produced nothing — failed to activate tool-calling behavior.<br>⚠ Needs schema reminder or stronger tool-pref rule. |
| 3 | **qwen2.5-coder 7B instruct q4_K_M** | Continue | ```json {"name":"edit_existing_file","arguments":{"filepath":"src/components/my-component.ts","changes":"..."}}``` | ⚠ Used wrong schema (`name/arguments/filepath/changes`).<br>❌ Tool not executed.<br>✅ Generated correct edit logic (added greeting + updated render). |
| 4 | **starcoder2 15B instruct** | Continue | “Continue edited src/components/my-component.ts” → file updated | ✅ File successfully edited.<br>✅ Added `greeting` property and updated `render()` method.<br>⚠ Reverted to legacy `lit-element` import instead of `lit`.<br>💬 Still provided extra descriptive text but tool executed correctly. |

---

## 🏁 Round 4 Summary  

| Aspect | Best Model | Notes |
|:--|:--|:--|
| **Tool Execution** | `starcoder2 15B instruct` | Actually modified the file successfully. |
| **Framework Accuracy** | `qwen2.5-coder 7B` & `deepseek-coder 6.7B` | Both stayed on Lit 3 syntax (though didn’t execute). |
| **Schema Adherence** | `starcoder2 15B` | Executed properly via Continue.<br>Qwen & DeepSeek require explicit schema hints. |
| **Code Quality** | `starcoder2 15B` | Functional code; only import regression. |
| **Practical Reliability** | `starcoder2 15B` | Strongest real execution behavior under minimal prompts. |

---

## 🧠 Observations Across Rounds  

| Area | Round 1 | Round 2 | Round 3 | Round 4 | Comment |
|:--|:--|:--|:--|:--|
| **Tool Execution Rate** | 25% | 75% | 75% | 25% | Only StarCoder 15B succeeded this round. |
| **Lit Version Accuracy** | 50% | 100% | 100% | 75% | One model (15B) reverted to legacy LitElement import. |
| **Schema Compliance** | Weak | Moderate | Strong | Mixed | DeepSeek & Qwen regressed without explicit schema cues. |
| **Practical Usability** | Minimal | Improved | Production Ready | Realistic | 15B works best in realistic Continue agent use. |

---
