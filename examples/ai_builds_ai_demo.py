import sys
import os
sys.path.insert(0, os.getcwd())

from src.core import (
    generate_structon_via_llm,
    Structon,
    Interpreter,
    set_interpreter,
    save_structon
)

interpreter = Interpreter()
set_interpreter(interpreter)

print("=" * 60)
print("AI BUILDS AI — FULL DEMO")
print("=" * 60)

# Step 1: Describe what you want
intent = "Summarize text and identify key points"
print(f"\n📝 Intent: {intent}")

# Step 2: Generate agent
print("\n⏳ Generating agent...")
agent_data = generate_structon_via_llm(intent)

print(f"\n✅ Agent created with {len(agent_data['nodes'])} nodes")
for node in agent_data["nodes"]:
    print(f"   {node['id']}: {node['atomic']}")

# Step 3: Find what input key agent expects
input_key = "input"
for node in agent_data["nodes"]:
    if node["atomic"] == "get":
        input_key = node["args"].get("key", "input")
        break

# Step 4: Run with actual input
test_input = """
Quantum computing represents a revolutionary approach to computation. 
Unlike classical computers that use bits (0 or 1), quantum computers use qubits 
that can exist in multiple states simultaneously through superposition. 
Major players include IBM, Google, and IonQ. 
Key challenges include error correction and maintaining quantum coherence.
The technology could revolutionize cryptography, drug discovery, and optimization.
"""

print(f"\n🔑 Agent expects input key: '{input_key}'")
print(f"📄 Test input: {test_input[:100]}...")

print("\n⏳ Running agent...")
agent = Structon.from_dict(agent_data)
result = interpreter.run(agent, {input_key: test_input})

print(f"\n✅ Result:")
print("-" * 40)
print(result.get("result", "No output"))
print("-" * 40)

# Step 5: Save
filepath = save_structon(agent_data, "summarizer_agent.json")
print(f"\n💾 Saved to: {filepath}")

print("\n" + "=" * 60)
print("🚀 AI BUILT A WORKING AI IN SECONDS")
print("=" * 60)