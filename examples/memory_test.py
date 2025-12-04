import sys
import os
sys.path.insert(0, os.path.join(os.getcwd(), 'src'))

import json
from datetime import datetime
from typing import List, Dict, Any, Optional
from core.atomics import atomic_call_llm

# Create memory directory
MEMORY_DIR = "./memory"
os.makedirs(MEMORY_DIR, exist_ok=True)

class MemoryStructon:
    """A single memory unit that can sense, act, and receive feedback."""
    
    def __init__(self, data: Dict[str, Any]):
        self.id = data.get("id", f"mem_{datetime.now().strftime('%Y%m%d%H%M%S')}")
        self.intent = data.get("intent", "")
        self.content = data.get("content", {})
        self.sense_patterns = data.get("sense_patterns", [])
        self.tension = data.get("tension", 0.5)
        self.success_rate = data.get("success_rate", 0.5)
        self.times_used = data.get("times_used", 0)
        self.created_at = data.get("created_at", datetime.now().isoformat())
        self.last_activated = data.get("last_activated", None)
        self.activation = 0.0  # Current activation level
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "intent": self.intent,
            "content": self.content,
            "sense_patterns": self.sense_patterns,
            "tension": self.tension,
            "success_rate": self.success_rate,
            "times_used": self.times_used,
            "created_at": self.created_at,
            "last_activated": self.last_activated
        }
    
    def sense(self, context: str) -> float:
        """Sense relevance to current context. Returns activation level."""
        # Quick pattern match first
        for pattern in self.sense_patterns:
            if pattern.lower() in context.lower():
                self.activation = self.tension * 0.9
                return self.activation
        
        # If no pattern match, use LLM for deeper sensing
        response = atomic_call_llm(
            json.dumps({"memory": self.intent, "context": context}),
            {"prompt": "Rate 0.0-1.0 how relevant this memory is to the context. Return ONLY a number.\n\nMemory: {input}"},
            {}
        )
        
        try:
            relevance = float(response.strip())
        except:
            relevance = 0.1
        
        self.activation = self.tension * relevance
        return self.activation
    
    def activate(self) -> Dict[str, Any]:
        """Return content when activated."""
        self.times_used += 1
        self.last_activated = datetime.now().isoformat()
        return self.content
    
    def feedback(self, success: bool):
        """Update based on feedback."""
        # Update success rate (moving average)
        new_value = 1.0 if success else 0.0
        self.success_rate = (self.success_rate * 0.8) + (new_value * 0.2)
        
        # Update tension
        if success:
            self.tension = max(0.1, self.tension * 0.9)  # Lower tension when successful
        else:
            self.tension = min(1.0, self.tension * 1.1)  # Raise tension when failing
    
    def save(self):
        """Persist to disk."""
        filepath = os.path.join(MEMORY_DIR, f"{self.id}.json")
        with open(filepath, 'w') as f:
            json.dump(self.to_dict(), f, indent=2)
    
    def __repr__(self):
        return f"Memory({self.id}: {self.intent[:30]}... tension={self.tension:.2f})"


class LivingMemory:
    """
    Memory as activity, not storage.
    
    Memories sense relevance, activate when needed, and evolve through feedback.
    """
    
    def __init__(self):
        self.memories: List[MemoryStructon] = []
        self.load_all()
    
    def load_all(self):
        """Load all memories from disk."""
        self.memories = []
        if os.path.exists(MEMORY_DIR):
            for filename in os.listdir(MEMORY_DIR):
                if filename.endswith('.json'):
                    filepath = os.path.join(MEMORY_DIR, filename)
                    with open(filepath, 'r') as f:
                        data = json.load(f)
                        self.memories.append(MemoryStructon(data))
        print(f"[Memory] Loaded {len(self.memories)} memories")
    
    def sense_all(self, context: str):
        """All memories sense the current context."""
        print(f"[Memory] Sensing context: {context[:50]}...")
        for memory in self.memories:
            memory.sense(context)
    
    def sense_batch(self, context: str):
        """Batch sensing - one LLM call for all memories."""
        if not self.memories:
            return
        
        memory_intents = [m.intent for m in self.memories]
        
        prompt = f"""Rate each memory's relevance (0.0-1.0) to this context.
Return JSON only: {{"0": 0.5, "1": 0.8, ...}}

Context: {context}

Memories:
{json.dumps({str(i): intent for i, intent in enumerate(memory_intents)}, indent=2)}"""
        
        response = atomic_call_llm(prompt, {"prompt": "{input}"}, {})
        
        try:
            start = response.find("{")
            end = response.rfind("}") + 1
            relevances = json.loads(response[start:end])
            
            for i, memory in enumerate(self.memories):
                relevance = float(relevances.get(str(i), 0.1))
                memory.activation = memory.tension * relevance
        except:
            # Fallback: give all memories low activation
            for memory in self.memories:
                memory.activation = memory.tension * 0.1
    
    def activate(self, top_k: int = 3) -> List[MemoryStructon]:
        """Return top-k activated memories."""
        sorted_memories = sorted(self.memories, key=lambda m: m.activation, reverse=True)
        activated = sorted_memories[:top_k]
        
        for memory in activated:
            memory.activate()
        
        return activated
    
    def create(self, intent: str, content: Dict[str, Any], sense_patterns: List[str] = None) -> MemoryStructon:
        """Create a new memory."""
        memory = MemoryStructon({
            "id": f"mem_{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "intent": intent,
            "content": content,
            "sense_patterns": sense_patterns or [],
            "tension": 0.8,  # New memories start with high tension
            "success_rate": 0.5
        })
        
        self.memories.append(memory)
        memory.save()
        print(f"[Memory] Created: {memory}")
        return memory
    
    def learn_from_experience(self, task: str, result: str, success: bool):
        """Create a memory from an experience."""
        # Ask LLM to extract what should be remembered
        response = atomic_call_llm(
            json.dumps({"task": task, "result": result, "success": success}),
            {"prompt": """Extract a reusable lesson from this experience.
Return JSON: {"intent": "what this memory is about", "lesson": "the key insight", "patterns": ["when to apply this"]}

Experience: {input}"""},
            {}
        )
        
        try:
            start = response.find("{")
            end = response.rfind("}") + 1
            learning = json.loads(response[start:end])
            
            memory = self.create(
                intent=learning.get("intent", task[:50]),
                content={"lesson": learning.get("lesson", result), "source_task": task},
                sense_patterns=learning.get("patterns", [])
            )
            return memory
        except:
            print("[Memory] Failed to extract learning")
            return None
    
    def feedback(self, memories: List[MemoryStructon], success: bool):
        """Update memories based on feedback."""
        for memory in memories:
            memory.feedback(success)
            memory.save()
        print(f"[Memory] Updated {len(memories)} memories (success={success})")
    
    def prune(self, min_tension: float = 0.05, min_uses: int = 0):
        """Remove low-value memories."""
        before = len(self.memories)
        self.memories = [
            m for m in self.memories 
            if m.tension >= min_tension or m.times_used > min_uses
        ]
        pruned = before - len(self.memories)
        if pruned > 0:
            print(f"[Memory] Pruned {pruned} low-value memories")
    
    def list_all(self):
        """Print all memories."""
        print(f"\n{'='*60}")
        print(f"LIVING MEMORY ({len(self.memories)} memories)")
        print(f"{'='*60}")
        for m in sorted(self.memories, key=lambda x: x.tension, reverse=True):
            bar = "█" * int(m.tension * 10) + "░" * (10 - int(m.tension * 10))
            print(f"  [{bar}] {m.tension:.2f} | {m.intent[:40]}...")
        print(f"{'='*60}\n")


# Test it
print("=" * 60)
print("LIVING MEMORY - Test")
print("=" * 60)

memory = LivingMemory()

# Create some memories
if len(memory.memories) == 0:
    print("\n[Creating initial memories...]")
    
    memory.create(
        intent="How to explain concepts clearly",
        content={
            "lesson": "Start simple, use analogies, give examples",
            "steps": ["Define simply", "Use analogy", "Give example", "Explain why it matters"]
        },
        sense_patterns=["explain", "what is", "how does"]
    )
    
    memory.create(
        intent="User prefers concise answers",
        content={
            "lesson": "Keep responses short unless asked for detail",
            "max_length": 200
        },
        sense_patterns=["answer", "tell me", "quick"]
    )
    
    memory.create(
        intent="Research requires multiple sources",
        content={
            "lesson": "Always check 3+ sources and cross-reference",
            "steps": ["Search multiple sources", "Compare findings", "Note conflicts"]
        },
        sense_patterns=["research", "find out", "investigate"]
    )

memory.list_all()

# Test sensing
print("\n[Testing: Sensing context...]")
context = "Can you explain quantum entanglement?"
memory.sense_batch(context)

print(f"\nContext: '{context}'")
print("\nActivations:")
for m in sorted(memory.memories, key=lambda x: x.activation, reverse=True):
    print(f"  {m.activation:.2f} | {m.intent[:40]}...")

# Test activation
print("\n[Testing: Activating top memories...]")
active = memory.activate(top_k=2)
print(f"\nActivated {len(active)} memories:")
for m in active:
    print(f"  - {m.intent}")
    print(f"    Content: {m.content}")

# Test feedback
print("\n[Testing: Feedback...]")
memory.feedback(active, success=True)

memory.list_all()

print("\n✅ Living Memory is working!")
print("=" * 60)

