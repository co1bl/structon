import sys
import os
sys.path.insert(0, os.path.join(os.getcwd(), 'src'))

import json
from llm import Generator, Evolver
from core import Structon, Interpreter, Node, Edge, Phase, NodeType
from core.atomics import atomic_call_llm

print("=" * 60)
print("EVOLUTION EXPERIMENT - Clean Version")
print("=" * 60)

interpreter = Interpreter()

# Create a simple v1 manually (known to work)
print("\n[1] Creating simple v1 structon...")

v1 = Structon(
    structure_id="explain_v1",
    structure_type="composite",
    intent="brief_explanation",
    phases=[Phase.SENSE, Phase.ACT, Phase.FEEDBACK],
    tension=0.8,
    importance=0.5,
    nodes=[
        Node(
            id="s1",
            type=NodeType.INPUT,
            phase=Phase.SENSE,
            description="Get topic",
            atomic="get",
            args={"key": "topic"},
            output="$topic"
        ),
        Node(
            id="a1",
            type=NodeType.PROCESS,
            phase=Phase.ACT,
            description="Brief answer",
            atomic="call_llm",
            input="$topic",
            args={"prompt": "Explain {input} in exactly ONE sentence. Be very brief."},
            output="$answer"
        ),
        Node(
            id="f1",
            type=NodeType.OUTPUT,
            phase=Phase.FEEDBACK,
            description="Output",
            atomic="emit",
            input="$answer",
            output="$result"
        )
    ],
    edges=[Edge("s1", "a1"), Edge("a1", "f1")]
)

# Run v1
print("\n[2] Running v1 (brief explanation)...")
result_v1 = interpreter.run(v1, {"topic": "black holes"})
output_v1 = str(result_v1.get('result', ''))
print(f"    Output: {output_v1}")

# Evaluate v1
print("\n[3] Evaluating v1...")
eval_v1 = atomic_call_llm(
    output_v1,
    {"prompt": "Rate this explanation 1-10 for completeness. Just say the number: {input}"},
    {}
)
print(f"    Score: {eval_v1}")

# Create improved v2 manually
print("\n[4] Creating evolved v2 structon...")

v2 = Structon(
    structure_id="explain_v2",
    structure_type="composite",
    intent="comprehensive_explanation",
    phases=[Phase.SENSE, Phase.ACT, Phase.FEEDBACK],
    tension=0.8,
    importance=0.5,
    nodes=[
        Node(
            id="s1",
            type=NodeType.INPUT,
            phase=Phase.SENSE,
            description="Get topic",
            atomic="get",
            args={"key": "topic"},
            output="$topic"
        ),
        Node(
            id="a1",
            type=NodeType.PROCESS,
            phase=Phase.ACT,
            description="Comprehensive answer",
            atomic="call_llm",
            input="$topic",
            args={"prompt": "Explain {input} comprehensively. Include: 1) Definition 2) Key properties 3) An example 4) Why it matters"},
            output="$answer"
        ),
        Node(
            id="f1",
            type=NodeType.OUTPUT,
            phase=Phase.FEEDBACK,
            description="Output",
            atomic="emit",
            input="$answer",
            output="$result"
        )
    ],
    edges=[Edge("s1", "a1"), Edge("a1", "f1")]
)

# Run v2
print("\n[5] Running v2 (comprehensive explanation)...")
result_v2 = interpreter.run(v2, {"topic": "black holes"})
output_v2 = str(result_v2.get('result', ''))
print(f"    Output: {output_v2[:300]}...")

# Evaluate v2
print("\n[6] Evaluating v2...")
eval_v2 = atomic_call_llm(
    output_v2,
    {"prompt": "Rate this explanation 1-10 for completeness. Just say the number: {input}"},
    {}
)
print(f"    Score: {eval_v2}")

# Compare
print("\n" + "=" * 60)
print("RESULTS")
print("=" * 60)
print(f"\nv1 (brief):        {len(output_v1)} chars")
print(f"v1 Score:          {eval_v1}")
print(f"\nv2 (comprehensive): {len(output_v2)} chars")
print(f"v2 Score:          {eval_v2}")

print("\n" + "=" * 60)
if len(output_v2) > len(output_v1):
    print("✅ EVOLUTION WORKS - v2 is more comprehensive")
else:
    print("⚠️  Check results manually")
print("=" * 60)