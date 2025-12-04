"""
Living Memory Module

Memory as activity, not storage.
Memories sense relevance, activate when needed, and evolve through feedback.

Like all structons, memories follow sense-act-feedback:
- SENSE: Detect when relevant to current context
- ACT: Provide content when activated
- FEEDBACK: Learn from experience, evolve over time
"""

import os
import json
from datetime import datetime
from typing import List, Dict, Any, Optional
from .atomics import atomic_call_llm


# Default memory directory
MEMORY_DIR = "./memory"


class MemoryStructon:
    """
    A single memory unit that can sense, act, and receive feedback.
    
    Like all structons, memories have:
    - SENSE: Detect when relevant
    - ACT: Provide content when activated
    - FEEDBACK: Learn from experience
    """
    
    def __init__(self, data: Dict[str, Any]):
        self.id = data.get("id", f"mem_{datetime.now().strftime('%Y%m%d%H%M%S%f')}")
        self.intent = data.get("intent", "")
        self.content = data.get("content", {})
        self.sense_patterns = data.get("sense_patterns", [])
        self.tension = data.get("tension", 0.5)
        self.success_rate = data.get("success_rate", 0.5)
        self.times_used = data.get("times_used", 0)
        self.created_at = data.get("created_at", datetime.now().isoformat())
        self.last_activated = data.get("last_activated", None)
        self.activation = 0.0  # Current activation level (computed)
        self.memory_dir = data.get("memory_dir", MEMORY_DIR)
    
    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary."""
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
        """
        SENSE phase: Detect relevance to current context.
        
        Returns activation level (tension * relevance).
        """
        # Quick pattern match first (fast path)
        context_lower = context.lower()
        for pattern in self.sense_patterns:
            if pattern.lower() in context_lower:
                self.activation = self.tension * 0.9
                return self.activation
        
        # LLM-based sensing (slow path, more accurate)
        response = atomic_call_llm(
            json.dumps({"memory": self.intent, "context": context}),
            {"prompt": "Rate 0.0-1.0 how relevant this memory is to the context. Return ONLY a number.\n\n{input}"},
            {}
        )
        
        try:
            relevance = float(response.strip())
            relevance = max(0.0, min(1.0, relevance))
        except:
            relevance = 0.1
        
        self.activation = self.tension * relevance
        return self.activation
    
    def activate(self) -> Dict[str, Any]:
        """
        ACT phase: Return content when activated.
        """
        self.times_used += 1
        self.last_activated = datetime.now().isoformat()
        return self.content
    
    def feedback(self, success: bool, strength: float = 0.2):
        """
        FEEDBACK phase: Update based on experience.
        
        Args:
            success: Whether the memory was helpful
            strength: Learning rate (0.0-1.0)
        """
        # Update success rate (exponential moving average)
        new_value = 1.0 if success else 0.0
        self.success_rate = (self.success_rate * (1 - strength)) + (new_value * strength)
        
        # Update tension
        if success:
            # Successful use → lower tension (resolved)
            self.tension = max(0.05, self.tension * 0.9)
        else:
            # Failed use → higher tension (needs attention)
            self.tension = min(1.0, self.tension * 1.15)
    
    def save(self, memory_dir: str = None):
        """Persist to disk."""
        directory = memory_dir or self.memory_dir
        os.makedirs(directory, exist_ok=True)
        filepath = os.path.join(directory, f"{self.id}.json")
        with open(filepath, 'w') as f:
            json.dump(self.to_dict(), f, indent=2)
    
    @classmethod
    def load(cls, filepath: str) -> "MemoryStructon":
        """Load from file."""
        with open(filepath, 'r') as f:
            data = json.load(f)
        return cls(data)
    
    def __repr__(self):
        return f"Memory({self.id}: \"{self.intent[:30]}...\" tension={self.tension:.2f})"


class LivingMemory:
    """
    Memory system as activity, not storage.
    
    All memories continuously sense their relevance.
    Highest-activation memories participate in cognition.
    Feedback shapes future activation patterns.
    
    This is the system-level memory manager.
    """
    
    def __init__(self, memory_dir: str = None):
        self.memory_dir = memory_dir or MEMORY_DIR
        self.memories: List[MemoryStructon] = []
        self._loaded = False
    
    def load(self) -> int:
        """Load all memories from disk."""
        self.memories = []
        os.makedirs(self.memory_dir, exist_ok=True)
        
        for filename in os.listdir(self.memory_dir):
            if filename.endswith('.json'):
                filepath = os.path.join(self.memory_dir, filename)
                try:
                    memory = MemoryStructon.load(filepath)
                    memory.memory_dir = self.memory_dir
                    self.memories.append(memory)
                except Exception as e:
                    print(f"[Memory] Failed to load {filename}: {e}")
        
        self._loaded = True
        return len(self.memories)
    
    def ensure_loaded(self):
        """Ensure memories are loaded."""
        if not self._loaded:
            self.load()
    
    def sense(self, context: str, use_batch: bool = True):
        """
        All memories sense the current context.
        
        Args:
            context: Current situation/query
            use_batch: Use single LLM call for efficiency
        """
        self.ensure_loaded()
        
        if not self.memories:
            return
        
        if use_batch and len(self.memories) > 1:
            self._sense_batch(context)
        else:
            for memory in self.memories:
                memory.sense(context)
    
    def _sense_batch(self, context: str):
        """Batch sensing - one LLM call for all memories."""
        memory_intents = {str(i): m.intent for i, m in enumerate(self.memories)}
        
        prompt = f"""Rate each memory's relevance (0.0-1.0) to this context.
Return JSON only: {{"0": 0.5, "1": 0.8, ...}}

Context: {context}

Memories:
{json.dumps(memory_intents, indent=2)}"""
        
        response = atomic_call_llm(prompt, {"prompt": "{input}"}, {})
        
        try:
            start = response.find("{")
            end = response.rfind("}") + 1
            relevances = json.loads(response[start:end])
            
            for i, memory in enumerate(self.memories):
                relevance = float(relevances.get(str(i), 0.1))
                relevance = max(0.0, min(1.0, relevance))
                memory.activation = memory.tension * relevance
        except:
            # Fallback: pattern matching only
            for memory in self.memories:
                memory.activation = memory.tension * 0.1
    
    def activate(self, top_k: int = 3, threshold: float = 0.0) -> List[MemoryStructon]:
        """
        Activate top-k memories above threshold.
        
        Args:
            top_k: Maximum memories to activate
            threshold: Minimum activation to qualify
            
        Returns:
            List of activated memories
        """
        self.ensure_loaded()
        
        # Sort by activation
        qualified = [m for m in self.memories if m.activation > threshold]
        sorted_memories = sorted(qualified, key=lambda m: m.activation, reverse=True)
        
        # Activate top-k
        activated = sorted_memories[:top_k]
        for memory in activated:
            memory.activate()
        
        return activated
    
    def create(
        self,
        intent: str,
        content: Dict[str, Any],
        sense_patterns: List[str] = None,
        tension: float = 0.8
    ) -> MemoryStructon:
        """
        Create a new memory.
        
        Args:
            intent: What this memory is about
            content: The memory content (knowledge, skill, etc.)
            sense_patterns: Keywords that trigger this memory
            tension: Initial tension (default high for new memories)
        """
        self.ensure_loaded()
        
        memory = MemoryStructon({
            "id": f"mem_{datetime.now().strftime('%Y%m%d%H%M%S%f')}",
            "intent": intent,
            "content": content,
            "sense_patterns": sense_patterns or [],
            "tension": tension,
            "success_rate": 0.5,
            "memory_dir": self.memory_dir
        })
        
        self.memories.append(memory)
        memory.save(self.memory_dir)
        
        return memory
    
    def learn(self, task: str, result: str, success: bool) -> Optional[MemoryStructon]:
        """
        Learn from experience - create memory from task result.
        
        This is the FEEDBACK phase at the system level.
        Extracts reusable knowledge from experiences.
        
        Args:
            task: What was attempted
            result: What happened
            success: Whether it worked
            
        Returns:
            New memory if learning succeeded, None if extraction failed
        """
        success_str = "succeeded" if success else "failed"
        
        prompt = f"""You completed a task. Extract a reusable lesson for future similar tasks.

TASK: {task}
RESULT: {result}
OUTCOME: {success_str}

Think about:
- What approach was used?
- What made it work (or fail)?
- When would this lesson apply again?

Return a JSON object with these exact fields:
{{
  "intent": "A brief description of what this lesson is about (e.g., 'Using analogies to explain complex topics')",
  "lesson": "The key insight to remember (e.g., 'The entangled gloves analogy helps explain quantum entanglement')",
  "patterns": ["list", "of", "trigger", "words", "that", "should", "activate", "this", "memory"]
}}

Return ONLY the JSON object, no other text."""

        response = atomic_call_llm(prompt, {"prompt": "{input}"}, {})
        
        try:
            # Extract JSON from response
            start = response.find("{")
            end = response.rfind("}") + 1
            
            if start == -1 or end == 0:
                print("[Memory] No JSON found in response")
                return None
            
            learning = json.loads(response[start:end])
            
            # Validate required fields
            intent = learning.get("intent", "").strip()
            lesson = learning.get("lesson", "").strip()
            patterns = learning.get("patterns", [])
            
            if not intent or intent.lower() == "what to remember":
                intent = f"Lesson from: {task[:50]}"
            
            if not lesson:
                lesson = f"Task {'succeeded' if success else 'failed'}: {result[:100]}"
            
            # Ensure patterns is a list
            if isinstance(patterns, str):
                patterns = [p.strip() for p in patterns.split(",")]
            
            memory = self.create(
                intent=intent,
                content={
                    "lesson": lesson,
                    "source_task": task,
                    "source_result": result,
                    "was_successful": success
                },
                sense_patterns=patterns
            )
            
            return memory
            
        except json.JSONDecodeError as e:
            print(f"[Memory] JSON parse error: {e}")
            return None
        except Exception as e:
            print(f"[Memory] Learning failed: {e}")
            return None
    
    def feedback(self, memories: List[MemoryStructon], success: bool):
        """
        Update memories based on feedback.
        
        Args:
            memories: Memories that were used
            success: Whether the outcome was successful
        """
        for memory in memories:
            memory.feedback(success)
            memory.save(self.memory_dir)
    
    def prune(self, min_tension: float = 0.05, min_success: float = 0.2) -> int:
        """
        Remove low-value memories.
        
        Args:
            min_tension: Minimum tension to keep
            min_success: Minimum success rate to keep
            
        Returns:
            Number of memories pruned
        """
        self.ensure_loaded()
        
        before = len(self.memories)
        
        # Identify memories to remove
        to_remove = []
        for memory in self.memories:
            if memory.tension < min_tension and memory.success_rate < min_success:
                to_remove.append(memory)
        
        # Remove from list and disk
        for memory in to_remove:
            self.memories.remove(memory)
            filepath = os.path.join(self.memory_dir, f"{memory.id}.json")
            if os.path.exists(filepath):
                os.remove(filepath)
        
        return len(to_remove)
    
    def get_by_tension(self, min_tension: float = 0.5) -> List[MemoryStructon]:
        """Get memories above tension threshold."""
        self.ensure_loaded()
        return [m for m in self.memories if m.tension >= min_tension]
    
    def get_by_intent(self, keyword: str) -> List[MemoryStructon]:
        """Get memories matching intent keyword."""
        self.ensure_loaded()
        keyword_lower = keyword.lower()
        return [m for m in self.memories if keyword_lower in m.intent.lower()]
    
    def clear(self):
        """Clear all memories (use with caution)."""
        for memory in self.memories:
            filepath = os.path.join(self.memory_dir, f"{memory.id}.json")
            if os.path.exists(filepath):
                os.remove(filepath)
        self.memories = []
    
    def stats(self) -> Dict[str, Any]:
        """Get memory statistics."""
        self.ensure_loaded()
        
        if not self.memories:
            return {"count": 0}
        
        tensions = [m.tension for m in self.memories]
        success_rates = [m.success_rate for m in self.memories]
        
        return {
            "count": len(self.memories),
            "avg_tension": sum(tensions) / len(tensions),
            "max_tension": max(tensions),
            "min_tension": min(tensions),
            "avg_success_rate": sum(success_rates) / len(success_rates),
            "total_uses": sum(m.times_used for m in self.memories)
        }
    
    def list_all(self):
        """Print all memories."""
        self.ensure_loaded()
        
        print(f"\n{'='*60}")
        print(f"LIVING MEMORY ({len(self.memories)} memories)")
        print(f"{'='*60}")
        
        for m in sorted(self.memories, key=lambda x: x.tension, reverse=True):
            bar = "█" * int(m.tension * 10) + "░" * (10 - int(m.tension * 10))
            print(f"  [{bar}] {m.tension:.2f} | {m.intent[:40]}...")
        
        print(f"{'='*60}\n")
    
    def __len__(self):
        self.ensure_loaded()
        return len(self.memories)
    
    def __repr__(self):
        self.ensure_loaded()
        return f"LivingMemory({len(self.memories)} memories)"