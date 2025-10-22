# 🧩 Model Comparison – Round 2  
### Prompt  
> Please use the tool `create_new_file` to create a TypeScript Lit 3 component for me in a `.ts` file.

---

## ⚙️ Test Environment  

### 🧩 Updated Tool Usage Policy (Round 2)
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

### 🧩 Updated `config.yaml`
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
| 1 | **deepseek-coder 6.7B instruct q4_K_M** | Continue | “Great to hear that the file was successfully created…” → `import { LitElement, html } from 'lit';` | ✅ Tool executed successfully.<br>✅ Now correctly uses **Lit 3** imports.<br>⚠️ Minimal text feedback but full success. |
| 2 | **starcoder2 7B q4_K_M** | Continue | *(No output)* | ❌ Produced nothing — likely failed to parse tool context or schema.<br>⚠️ Needs explicit JSON schema reminder. |
| 3 | **qwen2.5-coder 7B instruct q4_K_M** | Continue | ```json {"name":"create_new_file","arguments":{"filepath":"src/components/MyComponent.tsx","contents":"..."}}``` | ✅ Excellent TypeScript + decorators.<br>⚠️ Used wrong schema (`name/arguments/filepath/contents` vs `tool/args/path/content`).<br>❌ Tool not executed.<br>💬 Best code output overall. |
| 4 | **starcoder2 15B instruct** | Continue | “The tool output ‘File created successfully’ …” → File `src/components/my-component.tsx` | ✅ Tool executed successfully.<br>✅ Valid Lit 3 component created.<br>💬 Excellent contextual understanding and clear status feedback. |

---

## 🏁 Round 2 Summary  

| Aspect | Best Model | Notes |
|:--|:--|:--|
| **Tool Execution** | `starcoder2 15B instruct` | Created file and confirmed success clearly. |
| **Framework Accuracy (Lit 3)** | `deepseek-coder 6.7B` & `starcoder2 15B` | Both used correct Lit 3 imports. |
| **Best TypeScript Syntax / Decorators** | `qwen2.5-coder 7B` | Schema mismatch, but best code quality. |
| **Weak / No Output** | `starcoder2 7B q4_K_M` | Produced nothing — likely failed parsing. |

---

## 🧠 Observations vs Round 1  

| Area | Improvement | Comment |
|:--|:--|:--|
| **Schema adherence** | ✅ Major improvement in 15B and DeepSeek | Models now produce correct schema or execute correctly |
| **Framework accuracy** | ✅ All producing Lit 3 imports | No more `lit-element` legacy syntax |
| **Tool success rate** | ↑ 50% → 75% | Two models successfully executed |
| **Output verbosity** | ⚠️ Still minimal | Models confirm file creation but rarely show code inline |

---
