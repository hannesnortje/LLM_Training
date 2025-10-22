# 🧩 Model Comparison – Round 1  
### Prompt  
> Please use the tool `create_new_file` to create a TypeScript Lit 3 component for me in a `.ts` file.

---

## ⚙️ Test Environment  

### Continue Agent Rules
> You are a coding agent inside VS Code using Continue Agent mode.  
>  
> **Goal:** prefer tools to modify the workspace, then verify with `view_diff()` when relevant.  
>  
> If uncertain about a path, call `ls()` or `file_glob_search()` first.  
>  
> After executing tools, continue until the user’s task is complete, then summarize what changed.  
>  
> **Tools available:**  
> (listed in the Continue configuration, each with one example)

---

### `config.yaml`

```yaml
name: Local Agent
version: 1.0.0
schema: v1

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

  - name: DeepSeek Coder
    provider: ollama
    model: deepseek-coder:6.7b-instruct-q4_K_M
    roles: [chat, edit, apply, autocomplete]
    toolCalling: true

  - name: Qwen Coder
    provider: ollama
    model: qwen2.5-coder:7b-instruct-q4_K_M
    roles: [chat, edit, apply, autocomplete]
    toolCalling: true

  - name: StarCoder2 15B Instruct
    provider: ollama
    model: starcoder2:15b-instruct
    roles: [chat, edit, apply, autocomplete]
    toolCalling: true
  
  - name: Nomic Embed
    provider: ollama
    model: nomic-embed-text:latest
    roles: [embed]
```

---

## 📊 Model Results  

| # | Model | Mode | Response Excerpt | Evaluation Summary |
|:--:|:------|:-----|:-----------------|:-------------------|
| 1 | **deepseek-coder 6.7B instruct q4_K_M** | Continue | “I’m glad to hear that the file was successfully created…” → file `src/components/my-component.ts` | ✅ Tool executed successfully.<br>✅ Valid TypeScript LitElement code.<br>⚠️ Used legacy `lit-element` import.<br>💬 Good tool handling but minimal feedback. |
| 2 | **starcoder2 7B q4_K_M** | Continue | “**1. What is your current setup?** …” | ❌ Misinterpreted prompt as a GitHub issue form.<br>❌ No tool call or code generation. |
| 3 | **qwen2.5-coder 7B instruct q4_K_M** | Continue | ```json {"name":"create_new_file","arguments":{"filepath":"src/components/MyComponent.tsx","contents":"..."}}``` | ✅ Excellent reasoning and modern Lit 3 code with decorators.<br>⚠️ Used wrong JSON schema (`name/arguments/filepath/contents` vs `tool/args/path/content`).<br>❌ Tool not executed — file not created.<br>💬 Best TypeScript/Lit understanding. |
| 4 | **starcoder2 15B instruct** | Continue | ```python\nimport os\n\ndef create_lit_component(name): ...``` | ✅ Creative workaround — wrote a Python script to generate the `.ts` file.<br>⚠️ Ignored Continue’s tool schema.<br>❌ Off-language output (Python instead of TypeScript).<br>💬 Shows flexible reasoning but poor context adherence. |

---

## 🏁 Round 1 Summary  

| Aspect | Best Model | Notes |
|:--|:--|:--|
| **Tool Execution** | `deepseek-coder 6.7B instruct` | Actually created the file successfully. |
| **Code Quality / Modern Lit Syntax** | `qwen2.5-coder 7B instruct` | Used decorators and correct `lit` imports. |
| **Creative Reasoning (Off-Task)** | `starcoder2 15B instruct` | Generated a helper script instead of tool call. |
| **Weak Interpretation** | `starcoder2 7B q4_K_M` | Produced irrelevant issue template. |
