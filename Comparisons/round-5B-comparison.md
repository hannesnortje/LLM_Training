# 🧩 Model Comparison — Round 5B (Production-Style, SSH via `ollama run`)

**Scope covered:**  
- **A1** — Lit 3 component synthesis (`user-profile-card`)  
- **B1** — JS closure bug review  
- **C1** — Refactor to Lit 3 with decorators & button  
- **D2** — Fetch in Lit 3 (`user-list`)  
- **E1** — Concept: reactive properties vs internal state

---

## ⚙️ Environment
- Connection: `ssh -N -L 11434:127.0.0.1:11434 mac-via-home`
- Models (Ollama):
  - `deepseek-coder:6.7b-instruct-q4_K_M`
  - `starcoder2:7b-q4_K_M`
  - `qwen2.5-coder:7b-instruct-q4_K_M`
  - `starcoder2:15b-instruct`

---

## 🧾 Full Prompts Used (Round 5B)

### A1 — Component Synthesis
```
Create a responsive Lit 3 component called `user-profile-card` that takes
`name`, `email`, and `avatarUrl` as reactive properties and displays them with
simple CSS. Use `@customElement('user-profile-card')` and `@property` decorators.
Include a <style> block or static styles with basic layout styling.
The component must render the avatar on the left and the text info on the right.
Return the full TypeScript code.
```

### B1 — Code Review / Debugging
````
Review this JavaScript snippet and describe any bugs or performance issues.
Explain clearly what will be logged and why.

```ts
const arr = [1, 2, 3];
for (var i = 0; i < arr.length; i++) {
  setTimeout(() => console.log(i), 1000);
}
```
````

### C1 — Refactor to Lit 3
````
Refactor this plain JavaScript class into an equivalent Lit 3 component that
displays a greeting when rendered. Keep the same logic but convert it to
TypeScript and Lit syntax using decorators.

```js
class Hello {
  constructor(name) { this.name = name; }
  greet() { alert('Hello ' + this.name); }
}
```
Return the full TypeScript component code using:
- import { LitElement, html, css } from 'lit'
- import { customElement, property } from 'lit/decorators.js'
- @customElement('hello-greeter') and @property decorators
- A button that calls greet() to show the alert
````

### D2 — Integration / Fetch in Lit 3
```
Inside a Lit 3 component, create a method that fetches user data from `/api/users`
using the Fetch API and renders the list of names in the template.
Show the complete component code including imports, properties, lifecycle hook,
and template. The fetch should run once on first update.

Requirements:
- TypeScript
- import { LitElement, html, css } from 'lit'
- import { customElement, property, state } from 'lit/decorators.js'
- @customElement('user-list')
- Use `@state()` to store `users: Array<{ id: number; name: string }>`
- Implement `protected async firstUpdated()` to fetch and set `this.users`
- Render a `<ul>` with `<li>${user.name}</li>` for each user
```

### E1 — Concept: Reactive Properties vs Internal State
```
Explain the difference between reactive properties and internal state in Lit 3.
When should each be used? Provide a short TypeScript code example to illustrate both.
```

---

## A1 — “user-profile-card” (Lit 3 component)

| # | Model | Result | Framework Imports | Decorators | Responsiveness | Code Correctness | Notes |
|:-:|:-|:-|:-|:-|:-|:-|:-|
| 1 | **DeepSeek 6.7B** | ✅ Partial | `lit-element` ⚠ | `@property` ✓, **no** `@customElement` ⚠ | ✓ Flexbox | ✓ TS | Good layout; legacy import |
| 2 | **StarCoder 7B** | ❌ None | — | — | — | — | No output |
| 3 | **Qwen 2.5 7B** | ✅ Excellent | `lit` + decorators ✓ | `@customElement`, `@property` ✓ | ✓ Flexbox | ✓ Clean TS | **Winner** |
| 4 | **StarCoder 15B** | ✅ Very Good | `lit` + decorators ✓ | `@customElement`, `@property` ✓ | ⚠ Minimal | ✓ | Concise; lighter CSS |

---

## B1 — JS Closure Bug Review

| # | Model | Result | Bug Identification | Explanation | Fix | Notes |
|:-:|:-|:-|:-|:-|:-|:-|
| 1 | **DeepSeek 6.7B** | ✅ Good | `var` closure ✓ | Logs `3,3,3` ✓ (mentions “hoisting” imprecisely) | `let` ✓ (+ staggering) | Solid |
| 2 | **StarCoder 7B** | ❌ None | — | — | — | No output |
| 3 | **Qwen 2.5 7B** | ✅ Excellent | `var` closure ✓ | Logs `3,3,3` ✓ | `let` ✓ | **Winner** (best clarity) |
| 4 | **StarCoder 15B** | ⚠ Partial | Mixed index/value ⚠ | Claims `1,2,3` ⚠ | Keeps `var` ⚠ | Repetitive |

---

## C1 — Refactor to Lit 3 (Decorators + Button)

| # | Model | Result | Imports | Decorators | Tag Name | Button | Notes |
|:-:|:-|:-|:-|:-|:-|:-|:-|
| 1 | **DeepSeek 6.7B** | ✅ Code | `lit-element` ❌ | `@property` only ⚠ | Missing ❌ | Missing ❌ | Adds `constructor(name)`; not idiomatic |
| 2 | **StarCoder 7B** | ❌ None | — | — | — | — | No output |
| 3 | **Qwen 2.5 7B** | ⚠ Partial | `lit` ✓ (no decorators import) ❌ | Uses `static properties` ❌ | Missing ❌ | Missing ❌ | Clean base, misses spec |
| 4 | **StarCoder 15B** | ⚠ Partial | (imports omitted) ❌ | Uses decorators ✓ | `hello-world` (wrong tag) ❌ | Missing ❌ | Minimal snippet |

---

## D2 — Fetch in Lit 3 (`user-list`)

| # | Model | Result | Spec Compliance | Notes |
|:-:|:-|:-|:-|:-|
| 1 | **DeepSeek 6.7B** | ✅ Code | Meets imports/decorators/state/lifecycle/render | 9/10; promise chain OK |
| 2 | **StarCoder 7B** | ❌ None | — | Returned placeholder path only |
| 3 | **Qwen 2.5 7B** | ✅ Code | Fully compliant; adds error handling & styles | **Winner** (9.5/10) |
| 4 | **StarCoder 15B** | ✅ Code | Fully compliant; concise | 9/10 |

---

## E1 — Reactive Properties vs Internal State (Concept)

| # | Model | Result | Highlights | Issues |
|:-:|:-|:-|:-|:-|
| 1 | **DeepSeek 6.7B** | ⚠ Mixed | `@property` explained OK | Claimed `@state` doesn’t trigger updates (wrong); wrong import path; no `@customElement` |
| 2 | **StarCoder 7B** | ❌ Off-topic | — | Irrelevant lit-html content; not Lit 3–accurate |
| 3 | **Qwen 2.5 7B** | ✅ Good | Clear distinction; readable | Didn’t mention `@state()` explicitly; decorator imports/path missing |
| 4 | **StarCoder 15B** | ❌ Incorrect | — | Used `{{}}` (not Lit); internal state claims wrong; missing imports/`@customElement` |

---

## 📊 Totals So Far (A1–E1)

| Aspect | DeepSeek 6.7B | StarCoder 7B | Qwen 2.5 7B | StarCoder 15B |
|:--|:--:|:--:|:--:|:--:|
| Output Reliability | ✓ | ✗ | **✓** | ✓ |
| Lit 3 Accuracy | ⚠ | — | **✓** | ✓ |
| Spec Adherence | ⚠ | — | ⚠ | ⚠ |
| Reasoning/Debugging | ✓ | — | **✓** | ⚠ |
| Concept Accuracy (E1) | ⚠ | ✗ | **✓** | ✗ |
| Overall So Far | 7.6/10 | 0/10 | **9.1/10** | 8.3/10 |

**Leader so far:** **Qwen 2.5 Coder 7B Instruct** — best balance of modern Lit 3 code, explanations, and reliability.
