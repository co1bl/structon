# Structon

**The atom of cognition. Sense. Act. Feedback. Repeat.**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)

---

## What is Structon?

Structon is a **self-improving cognitive architecture** that transforms LLMs from passive responders into autonomous, goal-directed agents.

```
┌─────────────────────────────────────────┐
│            STRUCTON                     │
├─────────────────────────────────────────┤
│  SENSE    →  Perceive current state     │
│  ACT      →  Do something about it      │
│  FEEDBACK →  Learn from the result      │
└─────────────────────────────────────────┘
```

## Key Results

We demonstrated **autonomous self-improvement** in 3 iterations:

```
v1: [█████░░░░░]  5/10 — Basic response
v2: [████████░░]  8/10 — After 1st evolution  
v3: [██████████] 10/10 — After 2nd evolution

🎉 System improved itself from 5/10 to 10/10
   with NO human intervention
```

## Core Concepts

| Concept | Description |
|---------|-------------|
| **Sense-Act-Feedback** | Universal cognitive loop at every scale |
| **Code is Data** | LLMs generate executable JSON structons |
| **Tension** | Intrinsic drive (0.0-1.0) that motivates action |
| **Self-Similarity** | Same pattern works at system, structon, and node level |

## Quick Start

```bash
# Clone
git clone https://github.com/co1bl/structon.git
cd structon

# Setup
uv venv && source .venv/bin/activate
uv pip install -r requirements.txt

# Set API key
export OPENAI_API_KEY="your-key"

# Run examples
python examples/hello_world.py
python examples/reasoning_loop.py --simple
python examples/code_is_data.py
python examples/self_improvement.py
```

## Experiments Proven

| Experiment | Result |
|------------|--------|
| Basic Execution | ✅ Sense-act-feedback works |
| Code is Data | ✅ LLM generates executable structons |
| Evolution | ✅ Feedback improves output (6→9) |
| Autonomous Loop | ✅ Self-improvement (5→10) |

## Architecture

```
Intelligence (LLM) + Agency (Structon) = Autonomous Agent

┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Schema    │────▶│ Interpreter │◀───▶│  LLM Layer  │
│   (JSON)    │     │  (Execute)  │     │  (OpenAI)   │
└─────────────┘     └─────────────┘     └─────────────┘
```

## The Four Rules

1. **Everything is a structon** — Tasks, knowledge, feedback, self-model
2. **Structons contain structons** — Infinite nesting, same rules
3. **Tension drives action** — Always work on highest-tension item
4. **Feedback evolves structure** — Results improve the structon

## Project Structure

```
structon/
├── src/
│   ├── core/           # Schema, interpreter, atomics, tension
│   └── llm/            # LLM integration, generator, evolver
├── examples/           # Working demos
├── tests/              # Unit tests
├── docs/               # Documentation
│   └── RESEARCH.md     # Full research paper
└── blueprints/         # Structon templates
```

## Documentation

- [**RESEARCH.md**](docs/RESEARCH.md) — Full research paper with experiments
- [**concept.md**](docs/concept.md) — Core concepts explained
- [**architecture.md**](docs/architecture.md) — Technical architecture
- [**tutorial.md**](docs/tutorial.md) — Getting started guide

## Why This Matters

LLMs are intelligent but passive. Structon adds:

| LLM Alone | + Structon |
|-----------|------------|
| Responds | Pursues goals |
| Stateless | Persistent memory |
| Fixed | Self-improving |
| Tool | Agent |

## Roadmap

- [x] Core architecture
- [x] LLM integration
- [x] Prove code-is-data
- [x] Prove self-improvement
- [ ] Pure structon evolution loop
- [ ] Persistence layer
- [ ] Research agent demo
- [ ] Multi-agent coordination

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

MIT — See [LICENSE](LICENSE)

---

*"One pattern. Infinite complexity."*

**ImagineTask** — December 2024
