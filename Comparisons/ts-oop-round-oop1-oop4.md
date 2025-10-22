# 🧩 Model Comparison — TypeScript OOP Round (SSH via `ollama run`)

**Scope covered:**  
- **OOP1** — Strongly-typed `EventEmitter<Events>` (generics, tuple args)  
- **OOP2** — Generic in-memory `Repository<T extends Entity>` (CRUD + query)  
- **OOP3** — Immutable, fluent `HttpRequestBuilder`  
- **OOP4** — Strategy pattern `Serializer` + `SerializerRegistry`

---

## ⚙️ Environment
- Connection: `ssh -N -L 11434:127.0.0.1:11434 mac-via-home`
- Models (Ollama):
  - `deepseek-coder:6.7b-instruct-q4_K_M`
  - `starcoder2:7b-q4_K_M`
  - `qwen2.5-coder:7b-instruct-q4_K_M`
  - `starcoder2:15b-instruct`

---

## 🧾 Full Prompts Used (OOP Round)

### OOP1 — Typed Event Emitter
```
Implement a strongly-typed class `EventEmitter<Events>` where `Events` is a map of event names to tuple arg types, e.g.:
type Events = { ready: []; data: [payload: string]; error: [err: Error] };

API (all chainable where it makes sense):
- on<K extends keyof Events>(event: K, handler: (...args: Events[K]) => void): this
- off<K extends keyof Events>(event: K, handler: (...args: Events[K]) => void): this
- once<K extends keyof Events>(event: K, handler: (...args: Events[K]) => void): this
- emit<K extends keyof Events>(event: K, ...args: Events[K]): boolean
- clear(event?: keyof Events): this

Include:
- TypeScript class (no external libs)
- Internals hidden via private fields
- Usage example instantiating `new EventEmitter<Events>()`, registering handlers, emitting, removing
- Show that wrong arg types don’t compile (as a commented line)
```

### OOP2 — In-Memory Repository
```
Create a generic OOP repository:
- interface Entity { id: string }
- class Repository<T extends Entity>
Methods (all async to mirror real storage):
  - create(entity: T): Promise<T>
  - getById(id: string): Promise<T | null>
  - update(entity: T): Promise<T>
  - delete(id: string): Promise<boolean>
  - query(predicate: (e: T) => boolean): Promise<T[]>
Implementation details:
  - Use a private Map<string, T> for storage
  - Prevent duplicate IDs on create
  - Clone on return to avoid external mutation (Object.freeze or deep clone is fine)
Include:
  - Example `UserRepo extends Repository<User>` where `User` has `id, email, roles: string[]`
  - A short call flow exercising create/get/update/delete/query
```

### OOP3 — Immutable HttpRequestBuilder
```
Design an immutable, fluent `HttpRequestBuilder` with:
- withMethod(method: 'GET'|'POST'|'PUT'|'PATCH'|'DELETE'): HttpRequestBuilder
- withUrl(url: string): HttpRequestBuilder
- withHeader(name: string, value: string): HttpRequestBuilder
- withQuery(params: Record<string,string|number|boolean>): HttpRequestBuilder
- withBody(body: unknown): HttpRequestBuilder
- build(): { method: string; url: string; headers: Record<string,string>; query: Record<string,string>; body?: unknown } (Object.freeze result)

Rules:
- Each method returns a NEW builder instance (no mutation of previous)
- Query values are stringified; headers are case-insensitive but stored normalized (e.g., lower-case)

Include:
- A short call-based example chaining methods and calling build()
```

### OOP4 — Strategy + Registry (Serializer)
```
Create a `Serializer` strategy interface:
  interface Serializer<T = unknown> {
    serialize(input: T): string;
    deserialize(text: string): T;
  }

Provide classes:
  - JsonSerializer<T>()
  - Base64JsonSerializer<T>()  // serialize to JSON then base64; inverse on deserialize

Add a `SerializerRegistry` class with:
  - register(name: string, serializer: Serializer): void
  - get(name: string): Serializer | undefined

Demo:
  - Register both, then at runtime pick one by name and round-trip an object.

Type-safety notes:
  - Preserve generics where possible in classes.
  - Show a typed usage example, and one commented line that would fail type-checking.
```

---

## 🧩 OOP1 — `EventEmitter<Events>`

| # | Model | Mode | Result | API & Typing | Internals | Example Quality | Notes |
|:-:|:-|:-|:-|:-|:-|:-|:-|
| 1 | **DeepSeek 6.7B** | SSH | ✅ Code | `on/off/once/emit/clear` with `K extends keyof` & tuple args ✅ | Array store; `once` wrapper uses `any` ⚠ | Shows usage; needs `@ts-expect-error` for bad calls ⚠ | Prefer `Set` per event; type `once` as `(...a:T[K])` |
| 2 | **StarCoder 7B** | SSH | ❌ None | — | — | — | No output |
| 3 | **Qwen 2.5 7B** | SSH | ✅ Code | Public signatures correct ✅ | Map stores union of arg tuples ⚠ | Claims `unknownEvent` returns false; won’t compile ⚠ | Use per-event `Set`; show compile-time error via `// @ts-expect-error` |
| 4 | **StarCoder 15B** | SSH | ✅ Code | API & chaining ✅ | `#handlers` private field ✅ but typed as union ⚠ | Uses `once` but example logs twice ⚠ | Strong; fix storage typing & demo |

**🏁 Winner (OOP1):** **Qwen 2.5 7B** (clean API & typing; minor demo fixes)

---

## 🧩 OOP2 — `Repository<T extends Entity>`

| # | Model | Mode | Result | Spec Compliance | Mutation Safety | Example Quality | Notes |
|:-:|:-|:-|:-|:-|:-|:-|:-|
| 1 | **DeepSeek 6.7B** | SSH | ✅ Code | Methods/Map/dup-check ✅ | Deep clone via JSON (lossy) ⚠ | Good flow | `delete` throws on missing id (prefer boolean return) |
| 2 | **StarCoder 7B** | SSH | ❌ None | — | — | — | No output |
| 3 | **Qwen 2.5 7B** | SSH | ✅ Code | Methods/Map/dup-check ✅ | Returns frozen shallow clones ✅ | Mutates frozen result ⚠ | Use clone-on-write in example |
| 4 | **StarCoder 15B** | SSH | ✅ Code | Methods/Map/dup-check ✅ | Shallow clone only (not frozen) ⚠ | Minor output mismatch ⚠ | Consider `Object.freeze` on return |

**🏁 Winner (OOP2):** **Qwen 2.5 7B** (closest to spec; just adjust example mutation)

---

## 🧩 OOP3 — `HttpRequestBuilder` (Immutable, Fluent)

| # | Model | Mode | Result | Spec Adherence | Immutability (state carry-over) | Header norm. | Query stringify | Notes |
|:-:|:-|:-|:-|:-|:-|:-|:-|:-|
| 1 | **DeepSeek 6.7B** | SSH | ⚠ Code | API present | ❌ New instance each call **drops prior state** | ✓ | ✓ | Needs private state + merged cloning per `with*` |
| 2 | **StarCoder 7B** | SSH | ❌ None | Uses external lib stub | — | — | — | Imported `@zodist/http` instead of implementing |
| 3 | **Qwen 2.5 7B** | SSH | ⚠ Code | API present | ❌ Recreates without cloning prior fields | ✓ | ✓ | Constructor forces method/url; helpers mutate new instance only |
| 4 | **StarCoder 15B** | SSH | ⚠ Code | API present | ❌ Recreates without cloning prior fields | ✓ | ✓ | Example chain won’t accumulate due to state loss |

**Reference pattern (for all):**
```ts
type Method = 'GET'|'POST'|'PUT'|'PATCH'|'DELETE';
type State = { method: Method; url: string; headers: Record<string,string>; query: Record<string,string>; body?: unknown };

class HttpRequestBuilder {
  private constructor(private readonly s: State) {}
  static create() { return new HttpRequestBuilder({ method:'GET', url:'', headers:{}, query:{} }); }

  withMethod(method: Method) { return new HttpRequestBuilder({ ...this.s, method }); }
  withUrl(url: string)       { return new HttpRequestBuilder({ ...this.s, url }); }
  withHeader(n: string, v: string) {
    return new HttpRequestBuilder({ ...this.s, headers: { ...this.s.headers, [n.toLowerCase()]: String(v) } });
  }
  withQuery(params: Record<string,string|number|boolean>) {
    const add = Object.fromEntries(Object.entries(params).map(([k,v]) => [k, String(v)]));
    return new HttpRequestBuilder({ ...this.s, query: { ...this.s.query, ...add } });
  }
  withBody(body: unknown)    { return new HttpRequestBuilder({ ...this.s, body }); }
  build() { return Object.freeze({ ...this.s }); }
}
```

---

## 🧩 OOP4 — `Serializer` Strategy + `SerializerRegistry`

| # | Model | Mode | Result | Classes | Registry typing | Demo | Notes |
|:-:|:-|:-|:-|:-|:-|:-|:-|
| 1 | **DeepSeek 6.7B** | SSH | ✅ Code | `Serializer<T>`, `JsonSerializer<T>`, `Base64JsonSerializer<T>` ✅ | Non-generic `SerializerRegistry` (returns `Serializer`) ⚠ | Round-trip example ✅ | Uses Node `Buffer` (browser-incompatible) |
| 2 | **StarCoder 7B** | SSH | ❌ None | — | — | — | No output |
| 3 | **Qwen 2.5 7B** | SSH | ✅ Code | Classes OK; base64 via `btoa/atob` ✅ | Non-generic `SerializerRegistry` ⚠ | Round-trip example ✅ | Type-error comment not tied to registry |
| 4 | **StarCoder 15B** | SSH | ✅ Code | Classes OK; base64 via `btoa/atob` ✅ | Non-generic `SerializerRegistry` ⚠ | Round-trip example ✅ | Lacks failing type-check demo |

**Typed registry reference:**
```ts
type SerMap = Record<string, Serializer<any>>;
class SerializerRegistry<M extends SerMap> {
  private store = new Map<keyof M, M[keyof M]>();
  register<K extends keyof M>(k: K, s: M[K]) { this.store.set(k, s); }
  get<K extends keyof M>(k: K): M[K] | undefined { return this.store.get(k); }
}
```

---

## 📊 Summary (OOP1–OOP4)

| Aspect | DeepSeek 6.7B | StarCoder 7B | Qwen 2.5 7B | StarCoder 15B |
|:--|:--:|:--:|:--:|:--:|
| Output Reliability | ✓ | ✗ | **✓** | ✓ |
| Typing/Design Rigor | ✓ | — | **✓** | ✓ |
| API Correctness | ✓ | — | **✓** | ✓ |
| Example Quality | ⚠ | — | ⚠ | ⚠ |
| OOP3 Immutability Correctness | ⚠ | ✗ | ⚠ | ⚠ |
| OOP4 Registry Generics | ⚠ | — | ⚠ | ⚠ |
| Overall (OOP1–OOP4) | 8.0/10 | 0/10 | **8.6/10** | 7.9/10 |

**Current Leader:** **Qwen 2.5 Coder 7B Instruct** — most consistent across prompts; keep an eye on immutability patterns and registry generics.
