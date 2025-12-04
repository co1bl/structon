import sys
import os
sys.path.insert(0, os.getcwd())

from src.core import LivingMemory

memory = LivingMemory()
memory.load()

# Clear old test memories (optional)
# memory.clear()

# Test learning
new_mem = memory.learn(
    task="Explain quantum entanglement to a student",
    result="Used the entangled gloves analogy - student understood immediately",
    success=True
)

if new_mem:
    print(f"✅ Intent: {new_mem.intent}")
    print(f"   Lesson: {new_mem.content['lesson']}")
    print(f"   Triggers: {new_mem.sense_patterns}")

memory.list_all()