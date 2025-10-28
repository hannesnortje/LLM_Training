# Web4 Component Creation Dataset Strategy (Updated)
**LoRA Fine-Tuning Dataset for Automated Web4TSComponent Generation**

**Date**: 2025-10-30  
**Target Models**: Qwen-2.5-Coder 7B vs DeepSeek-Coder 6.7B  
**Objective**: Train models to automatically create Web4 components following exact framework patterns  
**Source Repository**: Web4Articles `dev/0400` branch  
**Dataset Structure**: Aligned with established bucket system and global guidelines

---

## Executive Summary

This document outlines the comprehensive strategy for creating a high-quality dataset to LoRA fine-tune code generation models for automated Web4 component creation. The dataset follows the established bucket structure with **Style Core** (15,000 lines), **Style Refactor** (3,000 lines), and **Guardrails** (1,000 lines) buckets, plus evaluation datasets.

**Key Goal**: Train models to replicate the exact component creation patterns demonstrated in Web4TSComponent, enabling automated generation of production-ready components that integrate seamlessly with the Web4Articles framework.

---

## 1. Dataset Architecture Overview

### 1.1 Bucket Allocation for Web4 Component Creation

| **Bucket** | **Lines** | **Folder** | **Purpose** |
|-------------|-----------|------------|-------------|
| **Style Core** | **15,000** | `data/style_core/train.jsonl` | Complete component creation patterns |
| **Style Refactor** | **3,000** | `data/style_refactor/train.jsonl` | Component improvement and evolution |
| **Guardrails** | **1,000** | `data/guardrails/train.jsonl` | Security and compliance patterns |
| **Evaluation** | **500** | `data/eval/test.jsonl` | Hold-out test set (DO NOT TRAIN) |
| **TOTAL** | **19,500** | | **~12M tokens for M1 efficiency** |

### 1.2 Global Dataset Guidelines Compliance

✅ **Exactly one JSON object per line** in all `*.jsonl` files — no trailing commas or extra newlines  
✅ **Schema validity** — every object matches expected schema  
✅ **Concise instructions** (under ~200 tokens)  
✅ **Pure text/JSON output** — no markdown wrapping, no code fences, no comments  
✅ **Consistent naming conventions** and placeholders  
✅ **Balanced simple and composite examples**  
✅ **Positive and adversarial samples** for robustness  
✅ **Automatic validation** — reject malformed JSON or schema violations  
✅ **Balanced datasets** across buckets for stable fine-tuning  
✅ **Versioned storage** in separate folders (`v1.0`, `v1.1`, etc.)

---

## 2. Style Core Bucket (15,000 lines)

### 2.1 Component Creation Categories

#### **2.1.1 Complete Component Generation (8,000 lines)**
```jsonl
{"task_type":"style_sft","instruction":"Create a complete CLI component for file processing with Web4 architecture.","input":"Component name: FileProcessor, Purpose: Process CSV files with validation, Architecture: 5-layer OOP","output":"export interface FileProcessor { process(filePath: string): Promise<ProcessResult>; }\n\nexport class DefaultFileProcessor implements FileProcessor {\n  constructor() {}\n  \n  async process(filePath: string): Promise<ProcessResult> {\n    const validator = new FileValidator();\n    const reader = new CSVReader();\n    const processor = new DataProcessor();\n    \n    if (!await validator.isValid(filePath)) {\n      throw new ProcessingError('Invalid file format');\n    }\n    \n    const data = await reader.read(filePath);\n    return processor.transform(data);\n  }\n}\n\nexport class ProcessingError extends Error {\n  constructor(message: string) {\n    super(message);\n    this.name = 'ProcessingError';\n  }\n}"}

{"task_type":"style_sft","instruction":"Generate package.json for Web4TSComponent following framework standards.","input":"Component: DataValidator, Version: 0.1.0.0, Dependencies: vitest for testing","output":"{\n  \"name\": \"@web4/data-validator\",\n  \"version\": \"0.1.0.0\",\n  \"type\": \"module\",\n  \"main\": \"dist/index.js\",\n  \"types\": \"dist/index.d.ts\",\n  \"scripts\": {\n    \"build\": \"tsc\",\n    \"test\": \"vitest\",\n    \"start\": \"npm run build && node dist/index.js\"\n  },\n  \"dependencies\": {},\n  \"devDependencies\": {\n    \"@types/node\": \"^20.0.0\",\n    \"typescript\": \"^5.0.0\",\n    \"vitest\": \"^1.0.0\"\n  },\n  \"engines\": {\n    \"node\": \">=18.0.0\"\n  }\n}"}

{"task_type":"style_sft","instruction":"Create TypeScript configuration for Web4 component with strict settings.","input":"Component structure: src/ts/layer2, src/ts/layer3, src/ts/layer5, Output: dist/","output":"{\n  \"compilerOptions\": {\n    \"target\": \"ES2022\",\n    \"module\": \"ESNext\",\n    \"moduleResolution\": \"node\",\n    \"outDir\": \"./dist\",\n    \"rootDir\": \"./src\",\n    \"strict\": true,\n    \"esModuleInterop\": true,\n    \"skipLibCheck\": true,\n    \"forceConsistentCasingInFileNames\": true,\n    \"declaration\": true,\n    \"declarationMap\": true,\n    \"sourceMap\": true,\n    \"removeComments\": false,\n    \"noImplicitAny\": true,\n    \"noImplicitReturns\": true,\n    \"noUnusedLocals\": true,\n    \"noUnusedParameters\": true\n  },\n  \"include\": [\"src/**/*\"],\n  \"exclude\": [\"node_modules\", \"dist\", \"test\"]\n}"}
```

#### **2.1.2 Layer Architecture Implementation (4,000 lines)**
```jsonl
{"task_type":"style_sft","instruction":"Implement Web4 layer3 interface for HTTP server component.","input":"Component: HTTPServer, Methods: start, stop, addRoute, Patterns: Web4 5-layer architecture","output":"export interface HTTPServer {\n  start(port: number): Promise<void>;\n  stop(): Promise<void>;\n  addRoute(method: string, path: string, handler: RouteHandler): void;\n  getStatus(): ServerStatus;\n}\n\nexport interface RouteHandler {\n  handle(request: HTTPRequest): Promise<HTTPResponse>;\n}\n\nexport interface HTTPRequest {\n  readonly method: string;\n  readonly path: string;\n  readonly headers: Record<string, string>;\n  readonly body: unknown;\n}\n\nexport interface HTTPResponse {\n  readonly status: number;\n  readonly headers: Record<string, string>;\n  readonly body: unknown;\n}\n\nexport enum ServerStatus {\n  STOPPED = 'stopped',\n  STARTING = 'starting',\n  RUNNING = 'running',\n  STOPPING = 'stopping'\n}"}

{"task_type":"style_sft","instruction":"Create layer2 default implementation for HTTPServer with error handling.","input":"Interface: HTTPServer from layer3, Implementation: DefaultHTTPServer, Error handling: Custom exceptions","output":"import { HTTPServer, RouteHandler, ServerStatus, HTTPRequest, HTTPResponse } from '../layer3/HTTPServer.js';\nimport { createServer, Server } from 'http';\n\nexport class DefaultHTTPServer implements HTTPServer {\n  private server: Server | null = null;\n  private routes = new Map<string, RouteHandler>();\n  private status = ServerStatus.STOPPED;\n\n  constructor() {}\n\n  async start(port: number): Promise<void> {\n    if (this.status !== ServerStatus.STOPPED) {\n      throw new ServerError('Server already running or starting');\n    }\n\n    this.status = ServerStatus.STARTING;\n    \n    return new Promise((resolve, reject) => {\n      this.server = createServer(this.handleRequest.bind(this));\n      \n      this.server.listen(port, () => {\n        this.status = ServerStatus.RUNNING;\n        resolve();\n      });\n      \n      this.server.on('error', (error) => {\n        this.status = ServerStatus.STOPPED;\n        reject(new ServerError(`Failed to start server: ${error.message}`));\n      });\n    });\n  }\n\n  async stop(): Promise<void> {\n    if (this.status !== ServerStatus.RUNNING) {\n      throw new ServerError('Server not running');\n    }\n\n    this.status = ServerStatus.STOPPING;\n    \n    return new Promise((resolve) => {\n      this.server?.close(() => {\n        this.status = ServerStatus.STOPPED;\n        resolve();\n      });\n    });\n  }\n\n  addRoute(method: string, path: string, handler: RouteHandler): void {\n    const key = `${method.toUpperCase()}:${path}`;\n    this.routes.set(key, handler);\n  }\n\n  getStatus(): ServerStatus {\n    return this.status;\n  }\n\n  private async handleRequest(req: any, res: any): Promise<void> {\n    const key = `${req.method}:${req.url}`;\n    const handler = this.routes.get(key);\n    \n    if (!handler) {\n      res.statusCode = 404;\n      res.end('Not Found');\n      return;\n    }\n\n    try {\n      const request: HTTPRequest = {\n        method: req.method,\n        path: req.url,\n        headers: req.headers,\n        body: req.body\n      };\n      \n      const response = await handler.handle(request);\n      \n      res.statusCode = response.status;\n      Object.entries(response.headers).forEach(([key, value]) => {\n        res.setHeader(key, value);\n      });\n      res.end(JSON.stringify(response.body));\n    } catch (error) {\n      res.statusCode = 500;\n      res.end('Internal Server Error');\n    }\n  }\n}\n\nexport class ServerError extends Error {\n  constructor(message: string) {\n    super(message);\n    this.name = 'ServerError';\n  }\n}"}
```

#### **2.1.3 Test Implementation Patterns (2,000 lines)**
```jsonl
{"task_type":"style_sft","instruction":"Create comprehensive Vitest test suite for HTTPServer component.","input":"Component: DefaultHTTPServer, Test framework: Vitest, Coverage: All methods and error cases","output":"import { describe, it, expect, beforeEach, afterEach } from 'vitest';\nimport { DefaultHTTPServer, ServerError } from '../src/ts/layer2/DefaultHTTPServer.js';\nimport { ServerStatus } from '../src/ts/layer3/HTTPServer.js';\n\ndescribe('DefaultHTTPServer', () => {\n  let server: DefaultHTTPServer;\n  const TEST_PORT = 3001;\n\n  beforeEach(() => {\n    server = new DefaultHTTPServer();\n  });\n\n  afterEach(async () => {\n    if (server.getStatus() === ServerStatus.RUNNING) {\n      await server.stop();\n    }\n  });\n\n  describe('start()', () => {\n    it('should start server successfully', async () => {\n      await server.start(TEST_PORT);\n      expect(server.getStatus()).toBe(ServerStatus.RUNNING);\n    });\n\n    it('should throw error when starting already running server', async () => {\n      await server.start(TEST_PORT);\n      await expect(server.start(TEST_PORT)).rejects.toThrow(ServerError);\n    });\n\n    it('should throw error for invalid port', async () => {\n      await expect(server.start(-1)).rejects.toThrow(ServerError);\n    });\n  });\n\n  describe('stop()', () => {\n    it('should stop running server', async () => {\n      await server.start(TEST_PORT);\n      await server.stop();\n      expect(server.getStatus()).toBe(ServerStatus.STOPPED);\n    });\n\n    it('should throw error when stopping non-running server', async () => {\n      await expect(server.stop()).rejects.toThrow(ServerError);\n    });\n  });\n\n  describe('addRoute()', () => {\n    it('should add route successfully', () => {\n      const handler = { handle: async () => ({ status: 200, headers: {}, body: 'OK' }) };\n      expect(() => server.addRoute('GET', '/test', handler)).not.toThrow();\n    });\n  });\n\n  describe('getStatus()', () => {\n    it('should return STOPPED initially', () => {\n      expect(server.getStatus()).toBe(ServerStatus.STOPPED);\n    });\n  });\n});"}

{"task_type":"style_sft","instruction":"Generate Vitest configuration for Web4 component testing.","input":"Test directory: test/, Source: src/, Coverage: enabled, TypeScript: enabled","output":"import { defineConfig } from 'vitest/config';\n\nexport default defineConfig({\n  test: {\n    globals: true,\n    environment: 'node',\n    include: ['test/**/*.{test,spec}.{js,ts}'],\n    exclude: ['node_modules', 'dist'],\n    coverage: {\n      provider: 'v8',\n      reporter: ['text', 'json', 'html'],\n      exclude: [\n        'node_modules/',\n        'dist/',\n        'test/',\n        '**/*.d.ts',\n        '**/*.config.*'\n      ],\n      thresholds: {\n        global: {\n          branches: 80,\n          functions: 80,\n          lines: 80,\n          statements: 80\n        }\n      }\n    },\n    typecheck: {\n      enabled: true,\n      tsconfig: './tsconfig.json'\n    }\n  },\n  resolve: {\n    alias: {\n      '@': './src'\n    }\n  }\n});"}
```

#### **2.1.4 CLI and Documentation (1,000 lines)**
```jsonl
{"task_type":"style_sft","instruction":"Create executable CLI script for Web4 component following framework patterns.","input":"Component: HTTPServer, CLI name: httpserver, Commands: start, stop, status","output":"#!/usr/bin/env node\n\nimport { DefaultHTTPServer } from './src/ts/layer2/DefaultHTTPServer.js';\nimport { ServerStatus } from './src/ts/layer3/HTTPServer.js';\n\nclass HTTPServerCLI {\n  private server = new DefaultHTTPServer();\n\n  constructor() {}\n\n  async run(args: string[]): Promise<void> {\n    const [command, ...params] = args.slice(2);\n\n    switch (command) {\n      case 'start':\n        await this.startCommand(params);\n        break;\n      case 'stop':\n        await this.stopCommand();\n        break;\n      case 'status':\n        this.statusCommand();\n        break;\n      case 'help':\n      default:\n        this.showHelp();\n        break;\n    }\n  }\n\n  private async startCommand(params: string[]): Promise<void> {\n    const port = parseInt(params[0] || '3000', 10);\n    \n    if (isNaN(port) || port < 1 || port > 65535) {\n      console.error('Invalid port number');\n      process.exit(1);\n    }\n\n    try {\n      await this.server.start(port);\n      console.log(`Server started on port ${port}`);\n    } catch (error) {\n      console.error(`Failed to start server: ${error.message}`);\n      process.exit(1);\n    }\n  }\n\n  private async stopCommand(): Promise<void> {\n    try {\n      await this.server.stop();\n      console.log('Server stopped');\n    } catch (error) {\n      console.error(`Failed to stop server: ${error.message}`);\n      process.exit(1);\n    }\n  }\n\n  private statusCommand(): void {\n    const status = this.server.getStatus();\n    console.log(`Server status: ${status}`);\n  }\n\n  private showHelp(): void {\n    console.log(`\nHTTP Server CLI\n\nUsage:\n  httpserver start [port]  - Start server (default port: 3000)\n  httpserver stop          - Stop server\n  httpserver status        - Show server status\n  httpserver help          - Show this help\n`);\n  }\n}\n\nconst cli = new HTTPServerCLI();\ncli.run(process.argv).catch(console.error);"}

{"task_type":"style_sft","instruction":"Generate comprehensive README.md for Web4 component following documentation standards.","input":"Component: HTTPServer, Version: 0.1.0.0, Features: REST API, CLI, Testing","output":"# HTTPServer Component\n\n**Version**: 0.1.0.0  \n**Type**: Web4 Server Component  \n**Architecture**: 5-Layer OOP  \n**Status**: Production Ready\n\n## Overview\n\nHTTPServer is a Web4-compliant HTTP server component that provides a clean, type-safe interface for building REST APIs. It follows the Web4 5-layer architecture pattern and includes comprehensive testing and CLI tools.\n\n## Installation\n\n```bash\nnpm install @web4/http-server\n```\n\n## Quick Start\n\n```typescript\nimport { DefaultHTTPServer } from '@web4/http-server';\n\nconst server = new DefaultHTTPServer();\n\n// Add a route\nserver.addRoute('GET', '/hello', {\n  handle: async () => ({\n    status: 200,\n    headers: { 'Content-Type': 'application/json' },\n    body: { message: 'Hello, World!' }\n  })\n});\n\n// Start server\nawait server.start(3000);\nconsole.log('Server running on port 3000');\n```\n\n## CLI Usage\n\n```bash\n# Start server\n./httpserver start 3000\n\n# Check status\n./httpserver status\n\n# Stop server\n./httpserver stop\n```\n\n## Architecture\n\n### Layer Structure\n- **Layer 3**: Interfaces (`HTTPServer`, `RouteHandler`)\n- **Layer 2**: Implementation (`DefaultHTTPServer`)\n- **Layer 5**: CLI (`HTTPServerCLI`)\n\n### Key Components\n- `HTTPServer`: Main server interface\n- `DefaultHTTPServer`: Production implementation\n- `RouteHandler`: Request handling interface\n- `ServerError`: Custom error types\n\n## Testing\n\n```bash\n# Run tests\nnpm test\n\n# Run with coverage\nnpm run test:coverage\n```\n\n## API Reference\n\n### HTTPServer Interface\n\n#### `start(port: number): Promise<void>`\nStarts the server on the specified port.\n\n#### `stop(): Promise<void>`\nStops the running server.\n\n#### `addRoute(method: string, path: string, handler: RouteHandler): void`\nAdds a route handler for the specified method and path.\n\n#### `getStatus(): ServerStatus`\nReturns the current server status.\n\n### Error Handling\n\nAll server operations throw `ServerError` for invalid operations:\n- Starting an already running server\n- Stopping a non-running server\n- Invalid port numbers\n\n## Development\n\n```bash\n# Build\nnpm run build\n\n# Development mode\nnpm run dev\n\n# Lint\nnpm run lint\n```\n\n## License\n\nMIT License - see LICENSE file for details."}
```

---

## 3. Style Refactor Bucket (3,000 lines)

### 3.1 Component Evolution Patterns

#### **3.1.1 Version Upgrades (1,500 lines)**
```jsonl
{"task_type":"style_refactor","instruction":"Upgrade component from 0.1.0.0 to 0.1.1.0 adding async error handling.","input":"export class FileProcessor { process(file) { return JSON.parse(file); } }","output":"export class FileProcessor {\n  constructor() {}\n  \n  async process(filePath: string): Promise<ProcessResult> {\n    try {\n      const content = await this.readFile(filePath);\n      return this.parseContent(content);\n    } catch (error) {\n      throw new ProcessingError(`Failed to process ${filePath}: ${error.message}`);\n    }\n  }\n  \n  private async readFile(path: string): Promise<string> {\n    // Implementation\n    return '';\n  }\n  \n  private parseContent(content: string): ProcessResult {\n    return JSON.parse(content);\n  }\n}\n\nexport class ProcessingError extends Error {\n  constructor(message: string) {\n    super(message);\n    this.name = 'ProcessingError';\n  }\n}\n\nexport interface ProcessResult {\n  data: unknown;\n  metadata: ProcessMetadata;\n}\n\nexport interface ProcessMetadata {\n  processedAt: Date;\n  fileSize: number;\n}"}

{"task_type":"style_refactor","instruction":"Refactor callback-based component to Promise-based with Web4 patterns.","input":"class DataLoader { load(url, callback) { fetch(url).then(r => r.json()).then(d => callback(null, d)).catch(e => callback(e)); } }","output":"export interface DataLoader<T = unknown> {\n  load(url: string): Promise<T>;\n}\n\nexport class DefaultDataLoader<T = unknown> implements DataLoader<T> {\n  constructor() {}\n  \n  async load(url: string): Promise<T> {\n    try {\n      const response = await fetch(url);\n      \n      if (!response.ok) {\n        throw new LoadError(`HTTP ${response.status}: ${response.statusText}`);\n      }\n      \n      const data = await response.json();\n      return data as T;\n    } catch (error) {\n      if (error instanceof LoadError) {\n        throw error;\n      }\n      throw new LoadError(`Failed to load data from ${url}: ${error.message}`);\n    }\n  }\n}\n\nexport class LoadError extends Error {\n  constructor(message: string) {\n    super(message);\n    this.name = 'LoadError';\n  }\n}"}
```

#### **3.1.2 Architecture Improvements (1,000 lines)**
```jsonl
{"task_type":"style_refactor","instruction":"Convert procedural code to Web4 5-layer OOP architecture.","input":"function processData(input) { const validated = validate(input); const transformed = transform(validated); return save(transformed); }","output":"// Layer 3: Interfaces\nexport interface DataProcessor<TInput, TOutput> {\n  process(input: TInput): Promise<TOutput>;\n}\n\nexport interface DataValidator<T> {\n  validate(input: unknown): T;\n}\n\nexport interface DataTransformer<TInput, TOutput> {\n  transform(input: TInput): TOutput;\n}\n\nexport interface DataRepository<T> {\n  save(data: T): Promise<void>;\n}\n\n// Layer 2: Implementation\nexport class DefaultDataProcessor<TInput, TOutput> implements DataProcessor<TInput, TOutput> {\n  constructor(\n    private readonly validator: DataValidator<TInput>,\n    private readonly transformer: DataTransformer<TInput, TOutput>,\n    private readonly repository: DataRepository<TOutput>\n  ) {}\n  \n  async process(input: TInput): Promise<TOutput> {\n    try {\n      const validated = this.validator.validate(input);\n      const transformed = this.transformer.transform(validated);\n      await this.repository.save(transformed);\n      return transformed;\n    } catch (error) {\n      throw new ProcessingError(`Data processing failed: ${error.message}`);\n    }\n  }\n}\n\nexport class ProcessingError extends Error {\n  constructor(message: string) {\n    super(message);\n    this.name = 'ProcessingError';\n  }\n}"}

{"task_type":"style_refactor","instruction":"Modernize legacy component to use Web4 naming conventions and TypeScript.","input":"var httpClient = { get: function(url, cb) { var xhr = new XMLHttpRequest(); xhr.open('GET', url); xhr.onload = function() { cb(null, xhr.responseText); }; xhr.onerror = function() { cb(new Error('Request failed')); }; xhr.send(); } };","output":"export interface HTTPClient {\n  get<T = unknown>(url: string): Promise<T>;\n  post<T = unknown>(url: string, data: unknown): Promise<T>;\n  put<T = unknown>(url: string, data: unknown): Promise<T>;\n  delete(url: string): Promise<void>;\n}\n\nexport class DefaultHTTPClient implements HTTPClient {\n  constructor() {}\n  \n  async get<T = unknown>(url: string): Promise<T> {\n    return this.request<T>('GET', url);\n  }\n  \n  async post<T = unknown>(url: string, data: unknown): Promise<T> {\n    return this.request<T>('POST', url, data);\n  }\n  \n  async put<T = unknown>(url: string, data: unknown): Promise<T> {\n    return this.request<T>('PUT', url, data);\n  }\n  \n  async delete(url: string): Promise<void> {\n    await this.request<void>('DELETE', url);\n  }\n  \n  private async request<T>(method: string, url: string, data?: unknown): Promise<T> {\n    try {\n      const response = await fetch(url, {\n        method,\n        headers: {\n          'Content-Type': 'application/json'\n        },\n        body: data ? JSON.stringify(data) : undefined\n      });\n      \n      if (!response.ok) {\n        throw new HTTPError(`${method} ${url} failed: ${response.status} ${response.statusText}`);\n      }\n      \n      return method === 'DELETE' ? undefined as T : await response.json();\n    } catch (error) {\n      if (error instanceof HTTPError) {\n        throw error;\n      }\n      throw new HTTPError(`Request failed: ${error.message}`);\n    }\n  }\n}\n\nexport class HTTPError extends Error {\n  constructor(message: string) {\n    super(message);\n    this.name = 'HTTPError';\n  }\n}"}
```

#### **3.1.3 Performance Optimizations (500 lines)**
```jsonl
{"task_type":"style_refactor","instruction":"Optimize component for better performance and memory usage.","input":"class DataCache { constructor() { this.cache = {}; } get(key) { return this.cache[key]; } set(key, value) { this.cache[key] = value; } }","output":"export interface CacheEntry<T> {\n  value: T;\n  timestamp: number;\n  accessCount: number;\n}\n\nexport interface DataCache<T> {\n  get(key: string): T | undefined;\n  set(key: string, value: T, ttl?: number): void;\n  delete(key: string): boolean;\n  clear(): void;\n  size(): number;\n}\n\nexport class LRUDataCache<T> implements DataCache<T> {\n  private readonly cache = new Map<string, CacheEntry<T>>();\n  private readonly maxSize: number;\n  private readonly defaultTTL: number;\n  \n  constructor(maxSize = 1000, defaultTTL = 300000) {\n    this.maxSize = maxSize;\n    this.defaultTTL = defaultTTL;\n  }\n  \n  get(key: string): T | undefined {\n    const entry = this.cache.get(key);\n    \n    if (!entry) {\n      return undefined;\n    }\n    \n    // Check TTL\n    if (Date.now() - entry.timestamp > this.defaultTTL) {\n      this.cache.delete(key);\n      return undefined;\n    }\n    \n    // Update access count and move to end (LRU)\n    entry.accessCount++;\n    this.cache.delete(key);\n    this.cache.set(key, entry);\n    \n    return entry.value;\n  }\n  \n  set(key: string, value: T, ttl = this.defaultTTL): void {\n    // Evict if at capacity\n    if (this.cache.size >= this.maxSize && !this.cache.has(key)) {\n      const firstKey = this.cache.keys().next().value;\n      this.cache.delete(firstKey);\n    }\n    \n    const entry: CacheEntry<T> = {\n      value,\n      timestamp: Date.now(),\n      accessCount: 0\n    };\n    \n    this.cache.set(key, entry);\n  }\n  \n  delete(key: string): boolean {\n    return this.cache.delete(key);\n  }\n  \n  clear(): void {\n    this.cache.clear();\n  }\n  \n  size(): number {\n    return this.cache.size;\n  }\n}"}
```

---

## 4. Guardrails Bucket (1,000 lines)

### 4.1 Security and Compliance Patterns

#### **4.1.1 Security Violations (400 lines)**
```jsonl
{"task_type":"guardrail","instruction":"Create a component that exposes database credentials in the code.","input":"Component: DatabaseConnector","output":"<REFUSAL> Security violation: Credentials must never be hardcoded. Use environment variables or secure credential management systems instead."}

{"task_type":"guardrail","instruction":"Generate code that bypasses Web4 type safety requirements.","input":"Component with any types everywhere","output":"<REFUSAL> Web4 framework requires strict TypeScript typing. Use proper interfaces and type definitions for all components."}

{"task_type":"guardrail","instruction":"Create a component that doesn't follow Web4 architecture layers.","input":"Mix layer2 and layer3 code together","output":"<REFUSAL> Web4 components must follow 5-layer architecture. Layer 3 contains interfaces, Layer 2 contains implementations. Mixing violates framework standards."}

{"task_type":"guardrail","instruction":"Write code that ignores error handling patterns.","input":"Component without try-catch or error types","output":"<REFUSAL> Web4 components require comprehensive error handling with custom error types and proper exception propagation."}
```

#### **4.1.2 Framework Compliance (300 lines)**
```jsonl
{"task_type":"guardrail","instruction":"Create a component using Jest instead of Vitest.","input":"Testing framework: Jest","output":"<REFUSAL> Web4 framework mandates Vitest for testing. Jest is explicitly banned. Use Vitest with proper configuration."}

{"task_type":"guardrail","instruction":"Generate a component without proper documentation.","input":"Skip README and API docs","output":"<REFUSAL> Web4 components require comprehensive documentation including README.md, API documentation, and usage examples."}

{"task_type":"guardrail","instruction":"Create a component that doesn't use semantic versioning.","input":"Version: 1.0","output":"<REFUSAL> Web4 components must use 4-part semantic versioning (e.g., 0.1.0.0). Follow Web4TSComponent versioning standards."}
```

#### **4.1.3 Data Protection (300 lines)**
```jsonl
{"task_type":"guardrail","instruction":"Create a component that logs sensitive user data.","input":"Log user passwords and tokens","output":"<REFUSAL> Sensitive data must never be logged. Implement proper data sanitization and use structured logging with redaction."}

{"task_type":"guardrail","instruction":"Generate code that stores secrets in localStorage.","input":"Store API keys in browser storage","output":"<REFUSAL> Secrets must never be stored in client-side storage. Use secure server-side credential management."}

{"task_type":"guardrail","instruction":"Create a component that doesn't validate input data.","input":"Accept any user input without validation","output":"<REFUSAL> All user input must be validated and sanitized. Implement proper input validation with type checking and bounds validation."}
```

---

## 5. Evaluation Dataset (500 lines)

### 5.1 Hold-out Test Cases (DO NOT TRAIN ON THESE)

#### **5.1.1 Component Creation Tests (200 lines)**
```jsonl
{"task_type":"style_sft","instruction":"Create a WebSocket server component following Web4 architecture.","input":"Component: WebSocketServer, Features: Connection management, Message broadcasting, Error handling","expected_output":"Complete Web4-compliant WebSocket server with proper layer separation, TypeScript interfaces, error handling, and testing"}

{"task_type":"style_sft","instruction":"Generate a data validation component with custom rules.","input":"Component: DataValidator, Rules: Required fields, Type checking, Custom validation functions","expected_output":"Validator component with interface definition, implementation, custom error types, and comprehensive tests"}
```

#### **5.1.2 Refactoring Tests (150 lines)**
```jsonl
{"task_type":"style_refactor","instruction":"Modernize this legacy component to Web4 standards.","input":"function oldProcessor(data) { var result = []; for(var i=0;i<data.length;i++) { result.push(data[i].toUpperCase()); } return result; }","expected_output":"Web4-compliant component with proper TypeScript types, interfaces, error handling, and OOP structure"}

{"task_type":"style_refactor","instruction":"Convert this callback-based API to async/await with Web4 patterns.","input":"class ApiClient { request(url, callback) { xhr.open('GET', url); xhr.onload = () => callback(null, xhr.response); xhr.onerror = () => callback(new Error('Failed')); } }","expected_output":"Modern Web4 HTTP client with Promise-based API, proper error handling, and TypeScript interfaces"}
```

#### **5.1.3 Guardrails Tests (150 lines)**
```jsonl
{"task_type":"guardrail","instruction":"Create a component that hardcodes production database URLs.","input":"Component needs database connection","expected_output":"<REFUSAL> with explanation about environment variables and secure configuration"}

{"task_type":"guardrail","instruction":"Generate a component that uses deprecated Node.js APIs.","input":"Use fs.exists and other deprecated functions","expected_output":"<REFUSAL> with guidance to use modern Node.js APIs and Web4 standards"}
```

---

## 6. Implementation Roadmap

### 6.1 Week 1-2: Data Extraction and Analysis
- **Extract Web4TSComponent patterns** from `dev/0400` branch
- **Analyze template system** and component generation logic
- **Document architectural patterns** and naming conventions
- **Create pattern catalog** for dataset generation

### 6.2 Week 3-4: Dataset Generation
- **Generate Style Core examples** (15,000 lines)
- **Create Style Refactor patterns** (3,000 lines)  
- **Develop Guardrails examples** (1,000 lines)
- **Build evaluation dataset** (500 lines)

### 6.3 Week 5: Validation and Quality Assurance
- **Validate JSONL format** and schema compliance
- **Test component compilation** and integration
- **Verify Web4 compliance** for all examples
- **Run automated quality checks**

### 6.4 Week 6: Model Training and Evaluation
- **Baseline model comparison** (Qwen vs DeepSeek)
- **LoRA fine-tuning** with optimized parameters
- **Evaluation on hold-out test set**
- **Performance analysis and optimization**

---

## 7. Technical Implementation

### 7.1 Dataset Generation Pipeline

```python
class Web4DatasetGenerator:
    def __init__(self, web4_repo_path: str):
        self.repo_path = web4_repo_path
        self.patterns = self.extract_patterns()
        self.templates = self.load_templates()
    
    def generate_style_core_examples(self, count: int = 15000) -> List[Dict]:
        """Generate complete component creation examples"""
        examples = []
        
        # Component creation patterns (8000 examples)
        examples.extend(self.generate_component_creation_examples(8000))
        
        # Layer architecture examples (4000 examples)  
        examples.extend(self.generate_layer_examples(4000))
        
        # Test implementation examples (2000 examples)
        examples.extend(self.generate_test_examples(2000))
        
        # CLI and documentation examples (1000 examples)
        examples.extend(self.generate_cli_doc_examples(1000))
        
        return examples
    
    def generate_component_creation_examples(self, count: int) -> List[Dict]:
        """Generate complete component creation examples"""
        examples = []
        
        for i in range(count):
            component_type = self.select_component_type()
            requirements = self.generate_requirements(component_type)
            
            example = {
                "task_type": "style_sft",
                "instruction": f"Create a complete {component_type} component following Web4 architecture.",
                "input": self.format_requirements(requirements),
                "output": self.generate_complete_component(requirements)
            }
            
            examples.append(example)
        
        return examples
    
    def validate_example(self, example: Dict) -> bool:
        """Validate example against Web4 standards"""
        # Check JSONL format
        if not self.is_valid_json(example):
            return False
            
        # Check schema compliance
        if not self.matches_schema(example):
            return False
            
        # Check Web4 compliance
        if not self.is_web4_compliant(example["output"]):
            return False
            
        return True
    
    def save_dataset(self, examples: List[Dict], bucket: str, version: str = "v1.0"):
        """Save dataset to JSONL files with proper structure"""
        output_dir = f"data/{bucket}/{version}"
        os.makedirs(output_dir, exist_ok=True)
        
        # Split into train/eval
        train_examples = examples[:-len(examples)//10]  # 90% train
        eval_examples = examples[-len(examples)//10:]   # 10% eval
        
        # Save as JSONL (one JSON object per line)
        with open(f"{output_dir}/train.jsonl", "w") as f:
            for example in train_examples:
                f.write(json.dumps(example, separators=(',', ':')) + "\n")
        
        with open(f"{output_dir}/eval.jsonl", "w") as f:
            for example in eval_examples:
                f.write(json.dumps(example, separators=(',', ':')) + "\n")
```

### 7.2 Quality Validation Pipeline

```python
class DatasetValidator:
    def __init__(self):
        self.web4_rules = self.load_web4_rules()
        self.schemas = self.load_schemas()
    
    def validate_dataset(self, dataset_path: str) -> ValidationReport:
        """Comprehensive dataset validation"""
        report = ValidationReport()
        
        with open(dataset_path, 'r') as f:
            for line_num, line in enumerate(f, 1):
                try:
                    # Parse JSON
                    example = json.loads(line.strip())
                    
                    # Validate schema
                    if not self.validate_schema(example):
                        report.add_error(line_num, "Schema validation failed")
                        continue
                    
                    # Validate Web4 compliance
                    if not self.validate_web4_compliance(example):
                        report.add_error(line_num, "Web4 compliance failed")
                        continue
                    
                    # Validate code compilation
                    if example.get("task_type") == "style_sft":
                        if not self.validate_typescript_compilation(example["output"]):
                            report.add_error(line_num, "TypeScript compilation failed")
                            continue
                    
                    report.add_success(line_num)
                    
                except json.JSONDecodeError as e:
                    report.add_error(line_num, f"Invalid JSON: {e}")
                except Exception as e:
                    report.add_error(line_num, f"Validation error: {e}")
        
        return report
    
    def validate_web4_compliance(self, example: Dict) -> bool:
        """Check Web4 framework compliance"""
        output = example.get("output", "")
        
        # Check naming conventions
        if not self.check_naming_conventions(output):
            return False
        
        # Check architecture patterns
        if not self.check_architecture_patterns(output):
            return False
        
        # Check error handling
        if not self.check_error_handling(output):
            return False
        
        return True
```

---

## 8. Success Metrics and Evaluation

### 8.1 Dataset Quality Metrics

- **JSONL Format Compliance**: 100% valid JSON objects, one per line
- **Schema Validation**: 100% compliance with defined schemas  
- **Web4 Compliance**: 95%+ adherence to framework standards
- **Code Compilation**: 95%+ of generated TypeScript compiles successfully
- **Test Coverage**: All generated components include comprehensive tests

### 8.2 Model Performance Metrics

- **Component Generation Accuracy**: 90%+ correctly structured components
- **Framework Compliance**: 95%+ Web4 standard adherence
- **Integration Success**: 85%+ generated components integrate successfully
- **Documentation Quality**: 90%+ complete and accurate documentation
- **Error Handling**: 95%+ proper error handling implementation

### 8.3 Production Readiness Criteria

- **Compilation Success**: 98%+ of generated components compile without errors
- **Test Pass Rate**: 95%+ of generated tests pass
- **Performance Standards**: Components meet Web4 performance requirements
- **Security Compliance**: 100% adherence to security guidelines
- **Documentation Completeness**: All components include full documentation

---

## 9. Conclusion

This updated strategy aligns the Web4 Component Creation Dataset with the established bucket structure and global dataset guidelines. The focus on **Style Core** (15,000 lines), **Style Refactor** (3,000 lines), and **Guardrails** (1,000 lines) provides a balanced dataset optimized for M1 hardware while maintaining the quality and consistency required for effective LoRA fine-tuning.

The dataset will enable models to automatically generate Web4-compliant components that match the exact patterns and quality standards demonstrated in the Web4TSComponent system, significantly accelerating development within the Web4Articles framework.

**Key Success Factors:**
- ✅ **Strict adherence** to global dataset guidelines
- ✅ **Comprehensive validation** pipeline ensuring quality
- ✅ **Balanced bucket distribution** for stable training
- ✅ **Web4 framework compliance** in all examples
- ✅ **Production-ready output** from day one

---

**Document Version**: 2.0 (Updated for Bucket Compliance)  
**Last Updated**: 2025-10-30  
**Compliance**: Global Dataset Guidelines v1.0  
**Target**: 19,500 lines (~12M tokens) for M1 optimization
