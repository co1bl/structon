"""
Code is Data - Proof of Concept

LLM generates a structon → Structon executes → Result is correct
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import json
from llm import Generator
from core import Structon, Interpreter

print("=" * 60)
print("CODE IS DATA - Full Proof")
print("=" * 60)

# Step 1: LLM generates code (structon)
print("\n[1] LLM Generating Structon...")
generator = Generator()
structon_dict = generator.generate(
    "Create a structon that takes a topic and returns 3 fun facts"
)

print("\nGenerated JSON:")
print(json.dumps(structon_dict, indent=2)[:500] + "...")

# Step 2: Data becomes executable code
print("\n[2] Converting Data to Executable...")
try:
    structon = Structon.from_dict(structon_dict)
    print(f"✅ Created: {structon.structure_id}")
except Exception as e:
    print(f"❌ Failed: {e}")
    print("\nFull structon for debugging:")
    print(json.dumps(structon_dict, indent=2))
    exit()

# Step 3: Execute the generated code
print("\n[3] Executing Generated Structon...")
interpreter = Interpreter()
result = interpreter.run(structon, {"topic": "honey bees"})

print("\n" + "=" * 60)
if result['success']:
    print("✅ CODE IS DATA - PROVEN!")
    print("=" * 60)
    print(f"\nResult:\n{result['result']}")
else:
    print("❌ Execution failed")
    print(f"Errors: {result['errors']}")

print("=" * 60)
