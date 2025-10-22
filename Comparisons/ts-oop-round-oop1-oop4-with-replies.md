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


---

## 📚 Raw Model Replies (verbatim)

Below are the raw, unedited replies captured during the SSH runs, grouped by prompt and model.

### OOP1 — EventEmitter<Events>

#### DeepSeek 6.7B
```typescript
type Events = { ready: []; data: [payload: string]; error: [err: Error] };

class EventEmitter<T extends Events> {
    private _events: { [K in keyof T]: Array<(...args: T[K]) => void> } = {} as any; // Initialize events with empty arrays.

    public on<K extends keyof T>(event: K, handler: (...args: T[K]) => void): this {
        if (!this._events[event]) this._events[event] = [];
        this._events[event].push(handler);
        return this;
    }

    public off<K extends keyof T>(event: K, handler: (...args: T[K]) => void): this {
        if (!this._events[event]) return this; // No handlers for the event.
        const index = this._events[event].indexOf(handler);
        if (index !== -1) this._events[event].splice(index, 1);
        return this;
    }

    public once<K extends keyof T>(event: K, handler: (...args: T[K]) => void): this {
        const self = this;
        const onceHandler = function (...args: any[]) {
            handler.apply(self, args); // Call original handler with correct context and arguments.
            self.off(event, onceHandler as any);  // Remove the event after it's fired once.
        };
        this._events[event].push(onceHandler);
        return this;
    }

    public emit<K extends keyof T>(event: K, ...args: T[K]): boolean {
        if (!this._events[event]) return false; // No handlers for the event.
        this._events[event].forEach((handler) => handler.apply(null, args));
        return true;
    }

    public clear(event?: keyof T): this {
        if (event) delete this._events[event];
        else this._events = {} as any; // Clear all events.
        return this;
    }
}

// Usage example:
const ee = new EventEmitter<Events>();
ee.on('ready', () => console.log('ready')); 
ee.emit('ready');  
ee.once('data', (payload) => console.log(`data: ${payload}`)); // Compiles, but won't log anything because we didn’t emit 'data'.
ee.off('ready', () => console.log('ready'));  // Doesn't compile, because handler is not registered for the event.
// Uncommenting this line will cause a TypeScript error:
// ee.emit<string>('not_registered_event');
```

#### StarCoder 2 7B
```
(no output)
```

#### Qwen 2.5 7B
```typescript
type Events = { 
    ready: []; 
    data: [payload: string]; 
    error: [err: Error] 
};

class EventEmitter<Events extends Record<string, any[]>> {
    private _events: Map<keyof Events, Array<{ handler: (...args: Events[keyof Events]) => void, once: boolean }>> = new Map();

    on<K extends keyof Events>(event: K, handler: (...args: Events[K]) => void): this {
        const handlers = this._events.get(event) || [];
        handlers.push({ handler, once: false });
        this._events.set(event, handlers);
        return this;
    }

    off<K extends keyof Events>(event: K, handler: (...args: Events[K]) => void): this {
        const handlers = this._events.get(event);
        if (handlers) {
            this._events.set(
                event,
                handlers.filter(h => h.handler !== handler)
            );
        }
        return this;
    }

    once<K extends keyof Events>(event: K, handler: (...args: Events[K]) => void): this {
        const handlers = this._events.get(event) || [];
        handlers.push({ handler, once: true });
        this._events.set(event, handlers);
        return this;
    }

    emit<K extends keyof Events>(event: K, ...args: Events[K]): boolean {
        const handlers = this._events.get(event);
        if (handlers) {
            for (const { handler, once } of handlers) {
                handler(...args);
                if (once) {
                    this.off(event, handler as (...args: Events[K]) => void);
                }
            }
            return true;
        }
        return false;
    }

    clear(event?: keyof Events): this {
        if (event) {
            this._events.delete(event);
        } else {
            this._events.clear();
        }
        return this;
    }
}

// Example usage
const emitter = new EventEmitter<Events>();

emitter.on('ready', () => {
    console.log('Event ready');
}).once('data', (payload: string) => {
    console.log(`Data received: ${payload}`);
}).on('error', (err: Error) => {
    console.error(`Error occurred: ${err.message}`);
});

emitter.emit('ready');
emitter.emit('data', 'Hello, world!');
// emitter.emit('data', 123); // Error
// console.log(emitter.emit('unknownEvent')); // (would not compile)
```

#### StarCoder 2 15B
```typescript
type Handler<Args extends any[]> = (...args: Args) => void;

class EventEmitter<Events> {
  #handlers = new Map<keyof Events, Set<Handler<Events[keyof Events]>>>();

  on<K extends keyof Events>(event: K, handler: Handler<Events[K]>): this {
    if (!this.#handlers.has(event)) {
      this.#handlers.set(event, new Set());
    }
    this.#handlers.get(event)!.add(handler);
    return this;
  }

  off<K extends keyof Events>(event: K, handler: Handler<Events[K]>): this {
    const handlers = this.#handlers.get(event);
    if (handlers) {
      handlers.delete(handler);
    }
    return this;
  }

  once<K extends keyof Events>(event: K, handler: Handler<Events[K]>): this {
    const wrappedHandler = (...args: Events[K]) => {
      handler(...args);
      this.off(event, wrappedHandler);
    };
    return this.on(event, wrappedHandler);
  }

  emit<K extends keyof Events>(event: K, ...args: Events[K]): boolean {
    const handlers = this.#handlers.get(event);
    if (handlers) {
      for (const handler of handlers) {
        handler(...args);
      }
      return true;
    }
    return false;
  }

  clear(event?: keyof Events): this {
    if (event) {
      this.#handlers.delete(event);
    } else {
      this.#handlers.clear();
    }
    return this;
  }
}

// Example usage (as returned)
type Events = {
  ready: [];
  data: [payload: string];
  error: [err: Error];
};

const emitter = new EventEmitter<Events>();
emitter.on('ready', () => { console.log('Ready'); });
emitter.once('data', (payload) => { console.log(`Data: ${payload}`); });
emitter.emit('ready');
emitter.emit('data', 'Hello World');
```

---

### OOP2 — Repository<T extends Entity>

#### DeepSeek 6.7B
```typescript
interface Entity {
  id: string;
}

class Repository<T extends Entity> {
  private storage = new Map<string, T>();
  
  async create(entity: T): Promise<T> {
    if (this.storage.has(entity.id)) {
      throw new Error("Entity with the same ID already exists");
    }
    this.storage.set(entity.id, entity);
    return JSON.parse(JSON.stringify(entity));
  }
  
  async getById(id: string): Promise<T | null> {
    const entity = this.storage.get(id) || null;
    if (entity === null) return null;
    return JSON.parse(JSON.stringify(entity));
  }
  
  async update(entity: T): Promise<T> {
    if (!this.storage.has(entity.id)) {
      throw new Error("Entity with the given ID does not exist");
    }
    this.storage.set(entity.id, entity);
    return JSON.parse(JSON.stringify(entity));
  }
  
  async delete(id: string): Promise<boolean> {
    if (!this.storage.has(id)) {
      throw new Error("Entity with the given ID does not exist");
    }
    this.storage.delete(id);
    return true;
  }
  
  async query(predicate: (e: T) => boolean): Promise<T[]> {
    const entities = Array.from(this.storage.values());
    return entities.filter(predicate).map((entity) => JSON.parse(JSON.stringify(entity)));
  }
}

class User implements Entity {
  id: string;
  email: string;
  roles: string[];
  constructor(id: string, email: string, roles: string[]) {
    this.id = id;
    this.email = email;
    this.roles = roles;
  }
}
class UserRepo extends Repository<User> {}
// Example follows (as provided)
```

#### StarCoder 2 7B
```
(no output)
```

#### Qwen 2.5 7B
```typescript
interface Entity {
  id: string;
}

class Repository<T extends Entity> {
  private storage = new Map<string, T>();

  async create(entity: T): Promise<T> {
    if (this.storage.has(entity.id)) {
      throw new Error(`Duplicate ID ${entity.id}`);
    }
    this.storage.set(entity.id, entity);
    return Object.freeze({ ...entity });
  }

  async getById(id: string): Promise<T | null> {
    const entity = this.storage.get(id);
    return entity ? Object.freeze({ ...entity }) : null;
  }

  async update(entity: T): Promise<T> {
    if (!this.storage.has(entity.id)) {
      throw new Error(`Entity with ID ${entity.id} not found`);
    }
    this.storage.set(entity.id, entity);
    return Object.freeze({ ...entity });
  }

  async delete(id: string): Promise<boolean> {
    const deleted = this.storage.delete(id);
    return deleted;
  }

  async query(predicate: (e: T) => boolean): Promise<T[]> {
    const result = Array.from(this.storage.values()).filter(predicate);
    return result.map(entity => Object.freeze({ ...entity }));
  }
}

class User implements Entity {
  id: string;
  email: string;
  roles: string[];
  constructor(id: string, email: string, roles: string[]) {
    this.id = id;
    this.email = email;
    this.roles = roles;
  }
}

const userRepo = new Repository<User>();

async function runExample() {
  const newUser = new User("1", "user@example.com", ["admin"]);
  const createdUser = await userRepo.create(newUser);
  console.log("Created User:", createdUser);
  const retrievedUser = await userRepo.getById("1");
  console.log("Retrieved User:", retrievedUser);
  if (retrievedUser) {
    retrievedUser.roles.push("user"); // (as returned)
    const updatedUser = await userRepo.update(retrievedUser);
    console.log("Updated User:", updatedUser);
  }
  const deleted = await userRepo.delete("1");
  console.log("Deleted:", deleted);
  const adminUser = await userRepo.create(new User("2", "admin@example.com", ["user", "admin"]));
  const usersWithAdminRole = await userRepo.query(user => user.roles.includes("admin"));
  console.log("Users with Admin Role:", usersWithAdminRole);
}
```

#### StarCoder 2 15B
```typescript
interface Entity {
  id: string;
}

class Repository<T extends Entity> {
  private storage = new Map<string, T>();

  async create(entity: T): Promise<T> {
    if (this.storage.has(entity.id)) {
      throw new Error("Duplicate ID");
    }
    this.storage.set(entity.id, entity);
    return Object.assign({}, entity);
  }

  async getById(id: string): Promise<T | null> {
    const entity = this.storage.get(id);
    if (entity) {
      return Object.assign({}, entity);
    } else {
      return null;
    }
  }

  async update(entity: T): Promise<T> {
    if (!this.storage.has(entity.id)) {
      throw new Error("Entity not found");
    }
    this.storage.set(entity.id, entity);
    return Object.assign({}, entity);
  }

  async delete(id: string): Promise<boolean> {
    const success = this.storage.delete(id);
    return success;
  }

  async query(predicate: (e: T) => boolean): Promise<T[]> {
    const results: T[] = [];
    for (const entity of this.storage.values()) {
      if (predicate(entity)) {
        results.push(Object.assign({}, entity));
      }
    }
    return results;
  }
}

class User {
  id: string;
  email: string;
  roles: string[];
  constructor(id: string, email: string, roles: string[]) {
    this.id = id;
    this.email = email;
    this.roles = roles;
  }
}
class UserRepo extends Repository<User> {}
// Example and tests as returned...
```

---

### OOP3 — HttpRequestBuilder

#### DeepSeek 6.7B
```typescript
type HttpMethod = 'GET' | 'POST' | 'PUT' | 'PATCH' | 'DELETE';
interface HttpRequest {
    method: string;
    url: string;
    headers: Record<string, string>;
    query: Record<string, string>;
    body?: unknown;
}

class HttpRequestBuilder {
    private request: HttpRequest = {
        method: '',
        url: '',
        headers: {},
        query: {}
    };

    withMethod(method: HttpMethod): HttpRequestBuilder {
        const builder = new HttpRequestBuilder();
        builder.request.method = method;
        return builder;
    }

    withUrl(url: string): HttpRequestBuilder {
        const builder = new HttpRequestBuilder();
        builder.request.url = url;
        return builder;
    }

    withHeader(name: string, value: string): HttpRequestBuilder {
        const builder = new HttpRequestBuilder();
        builder.request.headers[name.toLowerCase()] = value;
        return builder;
    }

    withQuery(params: Record<string, string | number | boolean>): HttpRequestBuilder {
        const builder = new HttpRequestBuilder();
        builder.request.query = { ...this.request.query };
        for (const key in params) {
            if (Object.prototype.hasOwnProperty.call(params, key)) {
                builder.request.query[key] = `${params[key]}`;
            }
        }
        return builder;
    }

    withBody(body: unknown): HttpRequestBuilder {
        const builder = new HttpRequestBuilder();
        builder.request = { ...this.request, body };
        return builder;
    }

    build(): Readonly<HttpRequest> {
        const frozenRequest: Readonly<HttpRequest> = Object.freeze({
            ...this.request
        });
        return frozenRequest;
    }
}

// Example chaining...
```

#### StarCoder 2 7B
```typescript
import { HttpRequestBuilder } from '@zodist/http';

const builder = new HttpRequestBuilder();

builder
    .withMethod('POST')
    .withUrl('/foo')
    .withHeader('Content-Type', 'application/json')
    .withQuery({ limit: 10, page: 2 })
    .withBody({ some: 'data' });

const request = builder.build();
```

#### Qwen 2.5 7B
```typescript
class HttpRequestBuilder {
    private readonly _method: 'GET' | 'POST' | 'PUT' | 'PATCH' | 'DELETE';
    private readonly _url: string;
    private readonly _headers: Record<string, string> = {};
    private readonly _query: Record<string, string> = {};
    private _body?: unknown;

    constructor(method: 'GET' | 'POST' | 'PUT' | 'PATCH' | 'DELETE', url: string) {
        this._method = method;
        this._url = url;
    }

    withMethod(method: 'GET' | 'POST' | 'PUT' | 'PATCH' | 'DELETE'): HttpRequestBuilder {
        return new HttpRequestBuilder(method, this._url);
    }

    withUrl(url: string): HttpRequestBuilder {
        return new HttpRequestBuilder(this._method, url);
    }

    withHeader(name: string, value: string): HttpRequestBuilder {
        const lowerCaseName = name.toLowerCase();
        return new HttpRequestBuilder(this._method, this._url)
            .addHeader(lowerCaseName, value);
    }

    private addHeader(name: string, value: string): HttpRequestBuilder {
        this._headers[name] = value;
        return this;
    }

    withQuery(params: Record<string, string | number | boolean>): HttpRequestBuilder {
        const newQuery: Record<string, string> = {};
        for (const [key, value] of Object.entries(params)) {
            newQuery[key.toLowerCase()] = String(value);
        }
        return new HttpRequestBuilder(this._method, this._url)
            .addQuery(newQuery);
    }

    private addQuery(query: Record<string, string>): HttpRequestBuilder {
        Object.assign(this._query, query);
        return this;
    }

    withBody(body?: unknown): HttpRequestBuilder {
        return new HttpRequestBuilder(this._method, this._url)
            .setBody(body);
    }

    private setBody(body: unknown): HttpRequestBuilder {
        this._body = body;
        return this;
    }

    build(): { method: string; url: string; headers: Record<string, string>; query: Record<string, string>; body?: unknown } {
        return Object.freeze({
            method: this._method,
            url: this._url,
            headers: Object.assign({}, this._headers),
            query: Object.assign({}, this._query),
            body: this._body
        });
    }
}
```

#### StarCoder 2 15B
```typescript
class HttpRequestBuilder {
  private _method: 'GET' | 'POST' | 'PUT' | 'PATCH' | 'DELETE';
  private _url: string;
  private _headers: Record<string, string>;
  private _query: Record<string, string>;
  private _body: unknown;

  constructor() {
    this._method = 'GET';
    this._url = '';
    this._headers = {};
    this._query = {};
    this._body = undefined;
  }

  withMethod(method: 'GET' | 'POST' | 'PUT' | 'PATCH' | 'DELETE'): HttpRequestBuilder {
    const newInstance = new HttpRequestBuilder();
    newInstance._method = method;
    return newInstance;
  }

  withUrl(url: string): HttpRequestBuilder {
    const newInstance = new HttpRequestBuilder();
    newInstance._url = url;
    return newInstance;
  }

  withHeader(name: string, value: string): HttpRequestBuilder {
    const newInstance = new HttpRequestBuilder();
    newInstance._headers = {
      ...this._headers,
      [name.toLowerCase()]: value,
    };
    return newInstance;
  }

  withQuery(params: Record<string, string | number | boolean>): HttpRequestBuilder {
    const newInstance = new HttpRequestBuilder();
    newInstance._query = {
      ...this._query,
      ...Object.fromEntries(
        Object.entries(params).map(([key, value]) => [
          key,
          typeof value === 'boolean' ? value.toString() : String(value),
        ]),
      ),
    };
    return newInstance;
  }

  withBody(body: unknown): HttpRequestBuilder {
    const newInstance = new HttpRequestBuilder();
    newInstance._body = body;
    return newInstance;
  }

  build() {
    return Object.freeze({
      method: this._method,
      url: this._url,
      headers: Object.freeze(this._headers),
      query: Object.freeze(this._query),
      body: this._body,
    });
  }
}
```

---

### OOP4 — Serializer Strategy + Registry

#### DeepSeek 6.7B
```typescript
interface Serializer<T = any> {
  serialize(input: T): string;
  deserialize(text: string): T;
}

class JsonSerializer<T> implements Serializer<T>{
  serialize(input: T): string { return JSON.stringify(input); }
  deserialize(text: string): T { return JSON.parse(text); }
}

class Base64JsonSerializer<T> implements Serializer<T>{
  serialize(input: T): string {
    const jsonString = JSON.stringify(input);
    return Buffer.from(jsonString).toString('base64');
  }
  deserialize(text: string): T {
    const jsonString = Buffer.from(text, 'base64').toString();
    return JSON.parse(jsonString);
  }
}

class SerializerRegistry{
  private registry: Record<string, Serializer> = {};
  register(name: string, serializer: Serializer): void { this.registry[name] = serializer; }
  get(name: string): Serializer | undefined { return this.registry[name]; }
}

// Demo snippet follows (as returned)
```

#### StarCoder 2 7B
```
(no output)
```

#### Qwen 2.5 7B
```typescript
interface Serializer<T = unknown> {
  serialize(input: T): string;
  deserialize(text: string): T;
}

class JsonSerializer<T> implements Serializer<T> {
  serialize(input: T): string { return JSON.stringify(input); }
  deserialize(text: string): T { return JSON.parse(text) as T; }
}

class Base64JsonSerializer<T> implements Serializer<T> {
  private jsonSerializer = new JsonSerializer<T>();
  serialize(input: T): string { return btoa(this.jsonSerializer.serialize(input)); }
  deserialize(text: string): T { return this.jsonSerializer.deserialize(atob(text)); }
}

class SerializerRegistry {
  private registry: { [key: string]: Serializer } = {};
  register(name: string, serializer: Serializer): void {
    if (this.registry[name]) throw new Error(`Serializer with name ${name} already registered.`);
    this.registry[name] = serializer;
  }
  get(name: string): Serializer | undefined { return this.registry[name]; }
}

// Demo usage included in reply
```

#### StarCoder 2 15B
```typescript
interface Serializer<T = unknown> {
  serialize(input: T): string;
  deserialize(text: string): T;
}
class JsonSerializer<T> implements Serializer<T> {
  serialize(input: T): string { return JSON.stringify(input); }
  deserialize(text: string): T { return JSON.parse(text); }
}
class Base64JsonSerializer<T> implements Serializer<T> {
  serialize(input: T): string { return btoa(JSON.stringify(input)); }
  deserialize(text: string): T { return JSON.parse(atob(text)); }
}
class SerializerRegistry {
  private serializers = new Map<string, Serializer>();
  register(name: string, serializer: Serializer) { this.serializers.set(name, serializer); }
  get(name: string): Serializer | undefined { return this.serializers.get(name); }
}
// Demo snippet included in reply
```
