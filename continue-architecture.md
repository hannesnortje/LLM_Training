# Architecture: Using Continue in VSCode over SSH with Ollama Offline Models on Mac M1

## Overview
This setup allows you to use the Continue extension in VSCode running on your Kubuntu machine, while leveraging powerful offline AI models (via Ollama) hosted on a remote Mac M1 (32GB RAM). The connection is established through SSH, with an additional tunnel for the Ollama API, enabling seamless access to local models from your remote development environment.

## Prerequisites
- **VSCode** with Remote - SSH extension
- **Continue extension** v1.2.9
- **Kubuntu 24.04** (or compatible Linux distribution)
- **Mac M1** with Ollama installed
- **SSH key authentication** configured between Kubuntu and Mac M1
- **Network connectivity** between machines

---

## Components

- **Kubuntu 24.04 Machine**
  - VSCode with Continue extension v1.2.9 installed
  - SSH client for remote connection
  - Terminal for SSH tunnel management

- **Mac M1 (32GB RAM)**
  - Ollama server running on localhost:11434
  - Continue configuration files
  - AI models (DeepSeek, Qwen, StarCoder2, etc.)


## Continue Tools and Offline LLMs

Continue provides a set of tools that can be called by supported models to automate coding tasks. These include:

| Tool Name                 | Description                                                        |
|--------------------------|--------------------------------------------------------------------|
| read_file                | Reads a file from the specified path                                |
| create_new_file          | Creates a new file at the specified path with provided content      |
| run_terminal_command     | Runs a terminal command                                             |
| file_glob_search         | Searches for files matching a glob pattern                          |
| view_diff                | Views the current git diff                                          |
| read_currently_open_file | Reads the currently open file                                       |
| ls                       | Lists files and folders in a given directory                        |
| create_rule_block        | Creates or edits rules for code generation                          |
| fetch_url_content        | Fetches content from a URL                                          |
| edit_existing_file       | Edits an existing file at the specified path with provided changes   |
| single_find_and_replace  | Performs exact string replacements in files                         |

**Offline LLM Tool Usage:**

- Most offline models (Qwen, StarCoder2, etc.) struggle to reliably use these tools.
- The only offline model that can consistently use Continue's tools is DeepSeek (e.g., `deepseek-coder:6.7b-instruct-q4_K_M`), but even then, it requires careful prompting and effort to get tool calls to work. *(Tested as of October 15, 2024)*
- For best tool support, cloud models like Google Gemini are recommended, but if you need offline, DeepSeek is currently the most capable for tool usage.

## Model Recommendations

Based on practical usage experience:

- **DeepSeek Coder (6.7b-instruct-q4_K_M)**: Best overall experience with better answers and more reliable tool usage
- **Qwen2.5 Coder (7b-instruct-q4_K_M)**: Good for general coding tasks but inconsistent tool calling
- **StarCoder2 (7b)**: Basic coding assistance but limited tool support

**Note**: Even with DeepSeek, tool calling can be inconsistent and may require multiple attempts or rephrasing prompts.

## Workflow Diagram Description

1. **VSCode (Kubuntu) Startup**
    - User opens VSCode and connects to Mac M1 via SSH (Remote - SSH)
    - VSCode workspace is now on Mac M1, but UI is on Kubuntu

2. **Ollama Server (Mac M1)**
    - Ollama is running on Mac M1, serving models on `localhost:11434`
    - Models available (example):
      - `deepseek-coder:6.7b-instruct-q4_K_M`
      - `qwen2.5-coder:7b-instruct-q4_K_M`
      - `starcoder2:7b`
      - Others as configured in Continue

3. **SSH Tunnel Setup (Kubuntu Terminal)**
    - User runs:
      ```bash
      ssh -N -L 11434:127.0.0.1:11434 mac-via-home
      ```
    - This forwards Kubuntu's `localhost:11434` to Mac's `localhost:11434`
    - Required for Continue to access Ollama API

4. **Continue Extension Configuration**
    - In `.continue/config.yaml` (on Mac M1):
      ```yaml
      providers:
        ollama:
          apiBase: http://127.0.0.1:11434
      models:
        - name: DeepSeek Coder
          provider: ollama
          model: deepseek-coder:6.7b-instruct-q4_K_M
          toolCalling: true
        - name: Qwen Coder
          provider: ollama
          model: qwen2.5-coder:7b-instruct-q4_K_M
          toolCalling: true
        - name: StarCoder2 7B
          provider: ollama
          model: starcoder2:7b
          toolCalling: true
      ```
    - Continue is now able to use these models for chat, code editing, and tool calls

---

## Data Flow

1. **User interacts with Continue in VSCode (Kubuntu)**
2. **Continue sends requests to `localhost:11434` (Kubuntu)**
3. **SSH tunnel forwards requests to Mac M1's Ollama server**
4. **Ollama processes requests using offline models**
5. **Responses are sent back through the tunnel to Continue in VSCode**

---

## Key Points for Diagram
- Kubuntu VSCode (Continue) → SSH Remote → Mac M1 workspace
- Kubuntu VSCode (Continue) → SSH Tunnel → Mac M1 Ollama API
- Ollama models run only on Mac M1, not Kubuntu
- All AI requests from Continue go through the tunnel
- Manual tunnel setup is required for API access

---


## Troubleshooting

### Common Issues and Solutions

**SSH Tunnel Problems:**
- **Issue**: Continue can't connect to Ollama
- **Solution**: Ensure SSH tunnel is active: `ssh -N -L 11434:127.0.0.1:11434 mac-via-home`
- **Check**: Verify tunnel is working with `curl http://localhost:11434/api/tags`

**Model Response Issues:**
- **Issue**: Prompts sometimes don't get responses or seem out of context
- **Solution**: Try sending the prompt again or rephrasing it
- **Note**: This is common with offline models and may require multiple attempts

**Tool Calling Problems:**
- **Issue**: Models claim they can't perform tasks or tools don't work consistently
- **Solution**: 
  - Use DeepSeek for best tool support
  - Try rephrasing your request
  - Break complex tasks into smaller steps
  - Be explicit about wanting to use tools

**Connection Drops:**
- **Issue**: SSH tunnel drops or Mac M1 becomes unavailable
- **Symptoms**: Nothing happens or VSCode warns about installing Ollama locally
- **Solution**: Re-establish SSH tunnel or check Mac M1 connectivity

## Notes
- You can add or change models in `.continue/config.yaml` on Mac M1
- The SSH tunnel must be active for Continue to access Ollama
- If you use Google Gemini or other cloud models, the tunnel is not needed

---

## References
- [Continue Docs](https://docs.continue.dev/)
- [Ollama Docs](https://ollama.com/library)
- [VSCode Remote SSH](https://code.visualstudio.com/docs/remote/ssh)

---
