# Structon

> The atom of cognition — a self-similar sense-act-feedback loop that nests infinitely, driven by tension, evolved by LLM.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

## What Is Structon?

Structon is a cognitive architecture that gives LLMs:

- **Memory** — persistent across sessions
- **Goals** — tension drives action  
- **Learning** — feedback enables evolution
- **Continuity** — mental state snapshots

## Core Idea

```
One pattern. Infinite complexity.

STRUCTON = {
    sense,      // perceive state
    act,        // take action
    feedback    // learn from result
}

Each phase can contain other structons.
Self-similar at every scale.
Complexity emerges from simplicity.
```

## The Problem

| LLM Alone | Problem |
|-----------|---------|
| Stateless | Forgets everything between calls |
| Passive | No goals, no drive |
| Can't learn | Same mistakes repeated |
| Limited depth | Context window bounds reasoning |

## The Solution

| LLM + Structon | Solution |
|----------------|----------|
| Persistent memory | Structons are saved and loaded |
| Goal-driven | Tension prioritizes what to do |
| Learns | Feedback evolves structons |
| Unlimited depth | Infinite nesting |

## Quick Start

```python
from structon import Structon, Interpreter

# Load a structon
s = Structon.load("my_task.json")

# Run the sense-act-feedback loop
interpreter = Interpreter()
result = interpreter.run(s)

# Structon evolves based on feedback
print(f"Result: {result}")
print(f"New tension: {s.tension}")
```

## The Four Rules

1. **Every structon has: sense → act → feedback**
2. **Every structon can contain structons**
3. **Tension drives what gets processed**
4. **Feedback triggers evolution via LLM**

## Architecture

```
Blueprint (template)
    │
    ▼
LLM (generates structons)
    │
    ▼
Structon (sense → act → feedback)
    │
    ▼
Atomic Functions (execute)
    │
    ▼
Feedback → LLM → Evolved Structon
```

## Self-Similarity (Fractal)

```
SYSTEM:     sense → act → feedback
               │
STRUCTON:   sense → act → feedback
               │
NODE:       sense → act → feedback
               │
ATOMIC:     input → compute → output

Same pattern at every level.
Infinite nesting, same rules.
```

## Tension

Tension (0.0 to 1.0) is the drive force:

- **High tension** = unresolved, urgent, needs attention
- **Low tension** = resolved, complete, can wait

```python
tension = (
    importance × 0.3 +
    urgency × 0.3 +
    unresolved × 0.2 +
    blocking × 0.2
)
```

## Documentation

- [Concept](docs/concept.md) — The full idea and vision
- [Architecture](docs/architecture.md) — Technical design
- [Tutorial](docs/tutorial.md) — Getting started guide
- [Examples](docs/examples/) — Example structons

## Project Structure

```
structon/
├── src/
│   ├── core/           # Schema, interpreter, tension
│   ├── llm/            # LLM integration
│   └── pools/          # Sense, act, feedback pools
├── blueprints/         # Structon templates
├── examples/           # Example code
└── tests/              # Test suite
```

## Installation

```bash
git clone https://github.com/ImagineTask/structon.git
cd structon
pip install -r requirements.txt
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

MIT License — Copyright (c) 2024 ImagineTask

## The Vision

> Structon is not just a framework. It's a format for machine thought.
> 
> DNA has 4 letters → all life.
> Structon has 3 phases → all cognition.
>
> sense → act → feedback (can nest infinitely)
>
> Simple. Complete. Powerful.

---

**Built by [ImagineTask](https://github.com/ImagineTask)**
