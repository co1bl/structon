"""Evolution Experiment - Prove the system learns."""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core import (
    Interpreter,
    set_interpreter,
    evolution_loop,
    list_pool
)

# Setup
interpreter = Interpreter()
set_interpreter(interpreter)

print("🧬 STRUCTON EVOLUTION EXPERIMENT")
print("=" * 50)
print(f"Sense pool: {list_pool('sense')}")
print(f"Act pool: {list_pool('act')}")
print(f"Feedback pool: {list_pool('feedback')}")

# Define test tasks
tasks = [
    {
        "intent": "Summarize this text",
        "input": {"input": "Quantum computing uses qubits which can exist in superposition, allowing parallel computation. IBM and Google lead this field."},
        "expected": "quantum"
    },
    {
        "intent": "Analyze this content",
        "input": {"input": "The stock market fell 5% today due to inflation fears and rising interest rates."},
        "expected": "market"
    },
    {
        "intent": "Generate a response",
        "input": {"input": "Write a haiku about programming."},
        "expected": "code"
    },
    {
        "intent": "Summarize and remember",
        "input": {"input": "Machine learning models learn patterns from data. Deep learning uses neural networks with many layers."},
        "expected": "learning"
    },
    {
        "intent": "Parse and analyze input",
        "input": {"input": "The user wants to book a flight from NYC to LA on December 25th."},
        "expected": "flight"
    }
]

# Run evolution loop (3 rounds)
print("\n🚀 Starting Evolution Loop...")
results = evolution_loop(tasks, interpreter, rounds=3)

# Summary
print("\n" + "=" * 50)
print("📊 EXPERIMENT RESULTS")
print("=" * 50)
print(f"Total tasks: {results['total_tasks']}")
print(f"Improvement: {results['improvement']:+.2f}")

if results['improvement'] > 0:
    print("\n✅ SYSTEM IMPROVED WITHOUT RETRAINING LLM!")
else:
    print("\n⚠️ No improvement detected (may need more rounds)")
