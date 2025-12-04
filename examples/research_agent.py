import sys
import os
sys.path.insert(0, os.getcwd())

import json
from datetime import datetime
from src.core import LivingMemory, Structon, Interpreter, Node, Edge, Phase, NodeType
from src.core.atomics import atomic_call_llm

print("=" * 60)
print("MEMORY-AWARE RESEARCH AGENT")
print("=" * 60)

# Initialize
memory = LivingMemory()
memory.load()
interpreter = Interpreter()

# Research topic
TOPIC = "current state of quantum computing in 2024"
TARGET_SCORE = 8
MAX_ITERATIONS = 3

print(f"\n📋 Topic: {TOPIC}")
print(f"🎯 Target: {TARGET_SCORE}/10")

# Step 1: Sense - Load relevant memories
print("\n" + "-" * 60)
print("PHASE 1: SENSE - Loading memories")
print("-" * 60)

memory.sense(TOPIC)
active_memories = memory.activate(top_k=3)

print(f"\n💭 Activated {len(active_memories)} memories:")
for m in active_memories:
    print(f"   - {m.intent}")
    print(f"     Lesson: {m.content.get('lesson', 'N/A')[:60]}...")

# Build context from memories
memory_context = ""
if active_memories:
    memory_context = "\n\nRelevant knowledge from memory:\n"
    for m in active_memories:
        memory_context += f"- {m.content.get('lesson', m.intent)}\n"

# Step 2: Act - Research with self-improvement
print("\n" + "-" * 60)
print("PHASE 2: ACT - Researching with self-improvement")
print("-" * 60)

current_prompt = f"""Write a research summary about: {TOPIC}

Include:
1. Current state and key players
2. Recent breakthroughs
3. Challenges
4. Future outlook
{memory_context}

Write 3-4 paragraphs."""

version = 1
history = []

while version <= MAX_ITERATIONS:
    print(f"\n🔄 Iteration {version}")
    
    # Generate research
    result = atomic_call_llm(TOPIC, {"prompt": current_prompt}, {})
    
    print(f"   Generated {len(result)} chars")
    
    # Evaluate
    eval_prompt = f"""Evaluate this research summary on a scale of 1-10.

Criteria:
- Accuracy and depth
- Coverage of key topics
- Clarity and structure
- Actionable insights

Research:
{result}

Return JSON only: {{"score": <1-10>, "feedback": "<what's missing or could be better>"}}"""

    eval_response = atomic_call_llm(eval_prompt, {"prompt": "{input}"}, {})
    
    try:
        start = eval_response.find("{")
        end = eval_response.rfind("}") + 1
        evaluation = json.loads(eval_response[start:end])
        score = evaluation.get("score", 5)
        feedback = evaluation.get("feedback", "")
    except:
        score = 5
        feedback = "Could not parse evaluation"
    
    print(f"   Score: {score}/10")
    print(f"   Feedback: {feedback[:60]}...")
    
    history.append({
        "version": version,
        "score": score,
        "feedback": feedback,
        "length": len(result)
    })
    
    if score >= TARGET_SCORE:
        print(f"\n✅ Target reached!")
        break
    
    # Improve prompt
    improve_prompt = f"""Improve this research prompt based on feedback.

Current prompt: {current_prompt}

Feedback: {feedback}

Return ONLY the improved prompt."""

    current_prompt = atomic_call_llm(improve_prompt, {"prompt": "{input}"}, {})
    version += 1

# Step 3: Feedback - Learn from experience
print("\n" + "-" * 60)
print("PHASE 3: FEEDBACK - Learning from experience")
print("-" * 60)

# Update memories that were used
if active_memories:
    success = history[-1]["score"] >= TARGET_SCORE
    memory.feedback(active_memories, success)
    print(f"\n📝 Updated {len(active_memories)} memories (success={success})")

# Learn new knowledge
new_memory = memory.learn(
    task=f"Research: {TOPIC}",
    result=f"Achieved {history[-1]['score']}/10 in {version} iterations. Key approach: self-improvement loop.",
    success=history[-1]["score"] >= TARGET_SCORE
)

if new_memory:
    print(f"📚 New memory: {new_memory.intent}")

# Final report
print("\n" + "=" * 60)
print("RESEARCH COMPLETE")
print("=" * 60)

print("\n📊 Progression:")
for h in history:
    bar = "█" * h["score"] + "░" * (10 - h["score"])
    print(f"   v{h['version']}: [{bar}] {h['score']}/10 | {h['length']} chars")

print(f"\n📈 Improvement: {history[0]['score']}/10 → {history[-1]['score']}/10")

print("\n📄 Final Research:")
print("-" * 60)
print(result[:1000] + "..." if len(result) > 1000 else result)
print("-" * 60)

print("\n💾 Memory state:")
memory.list_all()

print("=" * 60)
print("✅ Demo complete!")
print("=" * 60)