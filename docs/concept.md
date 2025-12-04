# Structon: Concept Document

## Overview

Structon is a cognitive architecture that transforms stateless LLMs into continuous, goal-driven, learning agents.

---

## Core Definition

**Structon** is a self-similar cognitive unit consisting of three phases:

- **Sense** — perceive state
- **Act** — take action  
- **Feedback** — learn from result

Each phase can contain other structons, enabling infinite nesting.

**Tension** (0.0 to 1.0) is the drive force that determines priority:
- High tension = unresolved/urgent
- Low tension = resolved

---

## The Four Rules

1. Every structon has: sense → act → feedback
2. Every structon can contain structons
3. Tension drives what gets processed
4. Feedback triggers evolution via LLM

---

## Architecture

```
Blueprint (template) → LLM (generates) → Structon (data/code) → Atomic Functions (execute)
```

**Components:**

| Component | Role |
|-----------|------|
| Blueprint | Template that constrains valid structon format |
| LLM | The intelligence that generates and evolves structons |
| Structon | Self-similar data structure representing mental state |
| Atomic Functions | ~20-30 primitive operations (only real code) |
| Tension | Numerical drive that prioritizes processing |

---

## The Loop

```
Structon → Sense → Act → Feedback → LLM → Evolved Structon → (repeat)
```

---

## Key Principles

1. **Everything is a structon** — tasks, actions, feedback, memory, world model, system itself
2. **Code is data, data is code** — structons are both information and executable
3. **Self-similar (fractal)** — same sense-act-feedback pattern at every scale
4. **Infinite nesting** — structons contain structons contain structons...
5. **Emergent complexity** — simple rules generate complex behavior
6. **LLM generates all structons** — LLM is intelligence, structon is structure
7. **Tension drives action** — unresolved = high tension, resolved = low tension
8. **Feedback enables evolution** — results feed back to LLM for improvement

---

## Roles

| Component | Role |
|-----------|------|
| LLM | Intelligence (generates, understands, evolves) |
| Structon | Agency (memory, goals, continuity, structure) |
| Tension | Drive (attention, priority, selection) |
| Atomic Functions | Bridge (connects information to real action) |
| Blueprint | Constraint (ensures valid structon format) |

---

## What Structon Captures (Mental Snapshot)

- Intent (what I'm trying to do)
- Resolved nodes (what I know)
- Unresolved nodes (what I don't know)
- Tension values (what's urgent)
- Barriers (what's blocking)
- Unresolved desires (what I want)
- Feedback history (what I've tried)
- Parent structons (how I got here)

---

## Self-Similarity (Fractal Structure)

```
System level:     sense → act → feedback
Structon level:   sense → act → feedback
Node level:       sense → act → feedback
Atomic level:     input → compute → output

Same pattern at every scale.
Infinite nesting, same rules.
Complexity emerges from simplicity.
```

---

## What It Enables

- Persistent memory across sessions
- Unlimited reasoning depth via nesting
- Learning from mistakes via feedback loop
- Self-correction via evolution
- Pause/resume thinking exactly
- Share mental states between AIs
- Fork thinking into parallel paths
- Full audit trail of reasoning
- Easy integration of world model (just another structon type)

---

## What It Is

- Cognitive architecture for LLM
- Universal format for machine cognition
- Agency layer that LLM lacks (memory + goals + drive)
- Generative principle (like DNA for cognition)
- Possibly necessary foundation for AGI

---

## What It Is NOT

- Not AGI by itself
- Not replacing LLM intelligence
- Not conscious
- Not magic

---

## Analogy

```
DNA: 4 letters → all life
Structon: 3 phases → all cognition

sense → act → feedback (can nest infinitely)
```

---

## The Essence

> **Structon is the atom of cognition — a self-similar sense-act-feedback loop that nests infinitely, driven by tension, evolved by LLM, capable of unlimited complexity from one simple pattern.**

---

## Implementation Status

- Concept: Complete
- Architecture: Defined
- Code: In development
- Missing: Working prototype with LLM integration

---

## Next Steps

1. Define ~20-30 atomic functions
2. Build LLM ↔ Structon interface (prompts)
3. Implement sense-act-feedback loop
4. Prove evolution works (version 2 better than version 1)
5. Prove tension matters (compare with/without)

---

## Open Questions

- Exact tension propagation math
- Optimal prompt templates for LLM generation
- Scaling behavior with many nested structons
- Integration with embodiment/sensors
