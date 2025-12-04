import sys
import os
sys.path.insert(0, os.path.join(os.getcwd(), 'src'))

import json
from core import Structon, Interpreter, Node, Edge, Phase, NodeType
from core.atomics import atomic_call_llm
from llm import Evolver

print("=" * 60)
print("AUTOMATIC EVOLUTION LOOP - HARD MODE")
print("=" * 60)

# Harder configuration
MAX_ITERATIONS = 5
TARGET_SCORE = 9  # Stricter
TOPIC = "quantum entanglement"

interpreter = Interpreter()

def create_structon(version: int, prompt: str) -> Structon:
    return Structon(
        structure_id=f"explain_v{version}",
        structure_type="composite",
        intent="explain_topic",
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
                description="Generate explanation",
                atomic="call_llm",
                input="$topic",
                args={"prompt": prompt},
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

def evaluate(output: str) -> dict:
    """Strict evaluation."""
    response = atomic_call_llm(
        output,
        {"prompt": """You are a strict physics professor. Evaluate this explanation of quantum entanglement.

Requirements for high scores:
- Must mention Einstein (EPR paradox)
- Must explain "spooky action at a distance"
- Must mention Bell's theorem or Bell tests
- Must give a concrete example
- Must explain why it matters (applications)

Score 9-10: All requirements met
Score 7-8: Most requirements met
Score 5-6: Basic explanation only
Score 1-4: Incomplete or wrong

Return JSON only: {"score": <1-10>, "missing": "<what's missing>"}

Explanation to evaluate: {input}"""},
        {}
    )
    
    try:
        start = response.find("{")
        end = response.rfind("}") + 1
        if start >= 0 and end > start:
            result = json.loads(response[start:end])
            return {"score": result.get("score", 5), "feedback": result.get("missing", "")}
    except:
        pass
    
    return {"score": 5, "feedback": "Parse error"}

def evolve_prompt(current_prompt: str, feedback: str) -> str:
    """Evolve prompt based on what's missing."""
    response = atomic_call_llm(
        json.dumps({"prompt": current_prompt, "missing": feedback}),
        {"prompt": """The current prompt is missing key elements. 
Improve it to address what's missing.
Return ONLY the improved prompt, nothing else.

Current: {input}"""},
        {}
    )
    return response.strip().strip('"')

# Start VERY weak
current_prompt = "What is {input}? Answer in 2-3 sentences max."
version = 1
history = []

print(f"\nTopic: {TOPIC}")
print(f"Target Score: {TARGET_SCORE}/10 (strict physics professor)")
print(f"Max Iterations: {MAX_ITERATIONS}")
print("\n" + "-" * 60)

while version <= MAX_ITERATIONS:
    print(f"\n🔄 ITERATION {version}")
    print(f"   Prompt: {current_prompt[:70]}...")
    
    structon = create_structon(version, current_prompt)
    result = interpreter.run(structon, {"topic": TOPIC})
    output = str(result.get("result", ""))
    
    print(f"   Output: {output[:120]}...")
    print(f"   Length: {len(output)} chars")
    
    evaluation = evaluate(output)
    score = evaluation.get("score", 0)
    feedback = evaluation.get("feedback", "")
    
    print(f"   Score: {score}/10")
    print(f"   Missing: {feedback[:100]}...")
    
    history.append({
        "version": version,
        "prompt": current_prompt[:50],
        "output_length": len(output),
        "score": score,
        "feedback": feedback[:50]
    })
    
    if score >= TARGET_SCORE:
        print(f"\n✅ TARGET REACHED! Score {score} >= {TARGET_SCORE}")
        break
    
    print(f"   📈 Evolving prompt...")
    current_prompt = evolve_prompt(current_prompt, feedback)
    version += 1

# Report
print("\n" + "=" * 60)
print("EVOLUTION COMPLETE")
print("=" * 60)

print("\n📊 Progression:")
for h in history:
    bar = "█" * h["score"] + "░" * (10 - h["score"])
    print(f"  v{h['version']}: [{bar}] {h['score']}/10 | {h['output_length']:4} chars | {h['feedback'][:30]}...")

first = history[0]['score']
last = history[-1]['score']
improvement = last - first

print(f"\n📈 Improvement: {first}/10 → {last}/10 (+{improvement})")

if last >= TARGET_SCORE:
    print("\n🎉 SELF-IMPROVEMENT SUCCESSFUL!")
    print(f"   System evolved from {first}/10 to {last}/10")
elif last > first:
    print(f"\n✅ EVOLUTION WORKING - improved by {improvement} points")
else:
    print("\n⚠️  No improvement detected")

print("\n📝 Final evolved prompt:")
print(f"   {current_prompt[:200]}...")
print("=" * 60)