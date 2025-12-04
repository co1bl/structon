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
print("TEST: Can AI Build AI?")
print("=" * 60)

# Step 1: Describe what you want
intent = "Summarize text and identify key points"

print(f"\n📝 Intent: {intent}")
print("\n⏳ Generating agent...")

# Step 2: AI generates the agent
agent_data = generate_structon_via_llm(intent)

if agent_data:
    print(f"\n✅ Agent generated!")
    print(f"   ID: {agent_data.get('structure_id')}")
    print(f"   Nodes: {len(agent_data.get('nodes', []))}")
    
    # Show structure
    print(f"\n📊 Structure:")
    for node in agent_data.get("nodes", []):
        print(f"   {node.get('id')}: {node.get('atomic')} - {node.get('description', '')[:40]}")
    
    # Step 3: Run it
    print("\n⏳ Running agent...")
    
    try:
        agent = Structon.from_dict(agent_data)
        result = interpreter.run(agent, {"input": "Quantum computing uses qubits which can be 0 and 1 simultaneously. This enables parallel processing. Major players include IBM and Google."})
        
        print(f"\n✅ Agent ran!")
        print(f"   Output: {str(result.get('result', ''))[:200]}...")
        
        # Step 4: Save it
        filepath = save_structon(agent_data, "generated_agent.json")
        print(f"\n💾 Saved to: {filepath}")
        
        print("\n" + "=" * 60)
        print("✅ AI BUILT AI - FEASIBLE!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Run failed: {e}")
        print("   Need to fix generated structure")
else:
    print("\n❌ Generation failed")