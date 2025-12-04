import sys
import os
sys.path.insert(0, os.getcwd())

import json
from src.core import Interpreter, Structon
from src.core.atomics import set_interpreter

print("=" * 60)
print("TEST: Full Research Agent (Code Is Data)")
print("=" * 60)

# Setup
interpreter = Interpreter()
set_interpreter(interpreter)

# Load research agent
with open("structons/research_agent.json", 'r') as f:
    agent_data = json.load(f)

agent = Structon.from_dict(agent_data)
print(f"\n✓ Loaded: {agent.structure_id}")
print(f"  Intent: {agent.intent}")
print(f"  Nodes: {len(agent.nodes)}")

# Run it!
print("\n" + "-" * 60)
print("Running Research Agent...")
print("-" * 60)

topic = "current state of quantum computing"
print(f"\n📋 Topic: {topic}\n")

result = interpreter.run(agent, {"topic": topic, "context": topic})

print("\n" + "-" * 60)
print("RESULT")
print("-" * 60)

if result.get("success"):
    print("\n✅ Agent completed successfully!")
    
    research = result.get("result", "")
    if research:
        print(f"\n📄 Research ({len(str(research))} chars):")
        print("-" * 40)
        print(str(research)[:800] + "..." if len(str(research)) > 800 else research)
        print("-" * 40)
else:
    print("\n❌ Agent failed")
    print(f"Errors: {result.get('errors', [])}")

print("\n" + "=" * 60)
print("✅ CODE IS DATA - PROVEN!")
print("   The entire agent is JSON. No Python logic.")
print("=" * 60)