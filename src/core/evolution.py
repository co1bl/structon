"""
Structon Evolution System

Enables self-organization and continuous improvement:
- Auto-selection from pools based on intent
- Success tracking and tension updates
- Automatic generation of improved structons
- Pool pruning of low performers
"""

import os
import json
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime

from .factory import (
    load_from_pool,
    list_pool,
    compose_from_pools,
    generate_structon_via_llm,
    save_structon,
    POOL_DIR
)


# =============================================================================
# Success Tracking
# =============================================================================

METRICS_FILE = "./data/evolution_metrics.json"


def load_metrics() -> Dict[str, Any]:
    """Load evolution metrics."""
    os.makedirs(os.path.dirname(METRICS_FILE), exist_ok=True)
    if os.path.exists(METRICS_FILE):
        with open(METRICS_FILE, 'r') as f:
            return json.load(f)
    return {"structons": {}, "history": []}


def save_metrics(metrics: Dict[str, Any]):
    """Save evolution metrics."""
    os.makedirs(os.path.dirname(METRICS_FILE), exist_ok=True)
    with open(METRICS_FILE, 'w') as f:
        json.dump(metrics, f, indent=2)


def track_success(structon_id: str, success: float, task: str):
    """Track success rate for a structon."""
    metrics = load_metrics()
    
    if structon_id not in metrics["structons"]:
        metrics["structons"][structon_id] = {
            "runs": 0,
            "total_success": 0,
            "success_rate": 0.5,
            "last_used": None
        }
    
    s = metrics["structons"][structon_id]
    s["runs"] += 1
    s["total_success"] += success
    s["success_rate"] = s["total_success"] / s["runs"]
    s["last_used"] = datetime.now().isoformat()
    
    # Track history
    metrics["history"].append({
        "structon_id": structon_id,
        "task": task,
        "success": success,
        "timestamp": datetime.now().isoformat()
    })
    
    save_metrics(metrics)
    return s["success_rate"]


def get_success_rate(structon_id: str) -> float:
    """Get success rate for a structon."""
    metrics = load_metrics()
    if structon_id in metrics["structons"]:
        return metrics["structons"][structon_id]["success_rate"]
    return 0.5  # Default


# =============================================================================
# Auto-Selection
# =============================================================================

SELECTION_KEYWORDS = {
    "sense": {
        "get_input": ["input", "get", "receive", "read"],
        "find_memories": ["memory", "remember", "recall", "past"],
        "parse_input": ["parse", "understand", "extract", "analyze input"]
    },
    "act": {
        "summarize_text": ["summarize", "summary", "brief", "short"],
        "analyze_content": ["analyze", "analysis", "examine", "deep"],
        "generate_response": ["generate", "create", "write", "produce"],
        "transform_content": ["transform", "convert", "change", "format"]
    },
    "feedback": {
        "emit_result": ["emit", "output", "return", "simple"],
        "learn_from_experience": ["learn", "remember", "memory", "improve"],
        "evaluate_quality": ["evaluate", "score", "quality", "rate"]
    }
}


def match_score(intent: str, keywords: List[str]) -> int:
    """Score how well intent matches keywords."""
    intent_lower = intent.lower()
    score = 0
    for keyword in keywords:
        if keyword in intent_lower:
            score += 1
    return score


def select_from_pool(pool: str, intent: str) -> str:
    """Select best structon from pool based on intent."""
    available = list_pool(pool)
    if not available:
        return None
    
    # Score each structon
    best = available[0]
    best_score = -1
    
    keywords_map = SELECTION_KEYWORDS.get(pool, {})
    
    for name in available:
        score = 0
        
        # Keyword matching - check base name and full name
        base_name = name.split("_v")[0]  # Remove version suffix
        keywords = keywords_map.get(base_name, keywords_map.get(name, []))
        score += match_score(intent, keywords) * 2
        
        # Also match intent words against structon name
        for word in intent.lower().split():
            if word in name.lower():
                score += 1
        
        # Boost by success rate (0-1 scaled to 0-3)
        success_rate = get_success_rate(f"{pool}/{name}")
        score += success_rate * 3
        
        # Prefer newer versions (v2, v3, etc.)
        if "_v" in name:
            try:
                version = int(name.split("_v")[-1])
                score += version * 0.5  # Slight preference for newer
            except:
                pass
        
        if score > best_score:
            best_score = score
            best = name
    
    return best


def auto_select(intent: str) -> Dict[str, str]:
    """Auto-select structons from all pools based on intent."""
    return {
        "sense": select_from_pool("sense", intent),
        "act": select_from_pool("act", intent),
        "feedback": select_from_pool("feedback", intent)
    }


def auto_compose(intent: str) -> Dict[str, Any]:
    """Auto-select and compose agent for intent."""
    selections = auto_select(intent)
    return compose_from_pools(
        sense=selections["sense"],
        act=selections["act"],
        feedback=selections["feedback"],
        intent=intent
    )


# =============================================================================
# Tension Management
# =============================================================================

def update_tension(pool: str, name: str, success: float):
    """Update tension based on success."""
    filepath = os.path.join(POOL_DIR, pool, f"{name}.json")
    if not os.path.exists(filepath):
        return
    
    with open(filepath, 'r') as f:
        structon = json.load(f)
    
    current_tension = structon.get("tension", 0.5)
    
    # Success lowers tension (resolved)
    # Failure raises tension (needs attention)
    if success > 0.7:
        new_tension = max(0.1, current_tension - 0.1)
    elif success < 0.3:
        new_tension = min(1.0, current_tension + 0.2)
    else:
        new_tension = current_tension
    
    structon["tension"] = new_tension
    
    with open(filepath, 'w') as f:
        json.dump(structon, f, indent=2)


# =============================================================================
# Evolution
# =============================================================================

def evolve_structon(pool: str, name: str, failure_reason: str = None) -> Dict[str, Any]:
    """Generate improved version of structon."""
    # Load current
    current = load_from_pool(pool, name)
    
    prompt = f"""Improve this {pool} structon.

Current intent: {current.get('intent')}
Current structure: {json.dumps(current, indent=2)[:500]}

{"Failure reason: " + failure_reason if failure_reason else ""}

Create an improved version that handles more cases."""
    
    # Determine blueprint
    if pool == "sense":
        if "memory" in current.get("intent", "").lower():
            blueprint = "sense"
        else:
            blueprint = "sense_passthrough"
    elif pool == "act":
        blueprint = "act"
    else:
        if "learn" in current.get("intent", "").lower():
            blueprint = "feedback_learn"
        elif "evaluat" in current.get("intent", "").lower():
            blueprint = "feedback"
        else:
            blueprint = "feedback_passthrough"
    
    improved = generate_structon_via_llm(
        f"Improved: {current.get('intent')}",
        blueprint_name=blueprint
    )
    improved["structure_type"] = pool
    
    # Save with version suffix
    version = 2
    new_name = f"{name}_v{version}"
    while os.path.exists(os.path.join(POOL_DIR, pool, f"{new_name}.json")):
        version += 1
        new_name = f"{name}_v{version}"
    
    save_structon(improved, f"{new_name}.json", structon_dir=f"{POOL_DIR}/{pool}", validate=False)
    
    return improved


def generate_missing(pool: str, intent: str) -> Dict[str, Any]:
    """Generate a new structon for missing capability."""
    # Determine blueprint
    if pool == "sense":
        blueprint = "sense_passthrough"
    elif pool == "act":
        blueprint = "act"
    else:
        blueprint = "feedback_passthrough"
    
    new_structon = generate_structon_via_llm(intent, blueprint_name=blueprint)
    new_structon["structure_type"] = pool
    
    name = intent.lower().replace(" ", "_")[:20]
    save_structon(new_structon, f"{name}.json", structon_dir=f"{POOL_DIR}/{pool}", validate=False)
    
    print(f"✅ Generated: {pool}/{name}.json")
    return new_structon


# =============================================================================
# Pool Pruning
# =============================================================================

def prune_pool(pool: str, min_success_rate: float = 0.2, min_runs: int = 5):
    """Remove low-performing structons from pool."""
    metrics = load_metrics()
    pruned = []
    
    for name in list_pool(pool):
        structon_id = f"{pool}/{name}"
        if structon_id in metrics["structons"]:
            s = metrics["structons"][structon_id]
            if s["runs"] >= min_runs and s["success_rate"] < min_success_rate:
                filepath = os.path.join(POOL_DIR, pool, f"{name}.json")
                # Don't delete, move to archive
                archive_dir = os.path.join(POOL_DIR, "archive", pool)
                os.makedirs(archive_dir, exist_ok=True)
                os.rename(filepath, os.path.join(archive_dir, f"{name}.json"))
                pruned.append(name)
                print(f"🗑️ Pruned: {pool}/{name} (success_rate: {s['success_rate']:.2f})")
    
    return pruned


# =============================================================================
# Evaluation
# =============================================================================

def evaluate_result(result: Any, expected: Any = None, task: str = None) -> float:
    """Evaluate success of a result."""
    # If expected provided, compare
    if expected is not None:
        if isinstance(expected, str) and isinstance(result, str):
            # Simple string similarity
            if expected.lower() in result.lower():
                return 1.0
            elif any(word in result.lower() for word in expected.lower().split()):
                return 0.7
            else:
                return 0.3
        elif result == expected:
            return 1.0
        else:
            return 0.5
    
    # Heuristic evaluation
    if result is None:
        return 0.0
    
    if isinstance(result, str):
        # Check for error indicators
        error_phrases = ["error", "failed", "cannot", "unable", "sorry", "please provide"]
        for phrase in error_phrases:
            if phrase in result.lower():
                return 0.3
        
        # Check for substance
        if len(result) < 10:
            return 0.4
        elif len(result) > 50:
            return 0.8
        else:
            return 0.6
    
    return 0.5


# =============================================================================
# Evolution Loop
# =============================================================================

def evolution_step(task: Dict[str, Any], interpreter) -> Dict[str, Any]:
    """Run one evolution step."""
    from .schema import Structon
    
    intent = task.get("intent", "Process input")
    input_data = task.get("input", {})
    expected = task.get("expected", None)
    
    # Auto-select and compose
    selections = auto_select(intent)
    agent_data = compose_from_pools(
        sense=selections["sense"],
        act=selections["act"],
        feedback=selections["feedback"],
        intent=intent
    )
    
    # Run
    agent = Structon.from_dict(agent_data)
    result = interpreter.run(agent, input_data)
    output = result.get("result", None)
    
    # Evaluate
    success = evaluate_result(output, expected, intent)
    
    # Track
    for pool, name in selections.items():
        if name:
            track_success(f"{pool}/{name}", success, intent)
            update_tension(pool, name, success)
    
    # Evolve if needed
    evolved = None
    if success < 0.4:
        # Find weakest component
        weakest_pool = min(selections.keys(), key=lambda p: get_success_rate(f"{p}/{selections[p]}"))
        weakest_name = selections[weakest_pool]
        if weakest_name:
            evolved = evolve_structon(weakest_pool, weakest_name, f"Low success on: {intent}")
            print(f"🔄 Evolved: {weakest_pool}/{weakest_name}")
    
    return {
        "intent": intent,
        "selections": selections,
        "output": output,
        "success": success,
        "evolved": evolved is not None
    }


def evolution_loop(tasks: List[Dict[str, Any]], interpreter, rounds: int = 1) -> Dict[str, Any]:
    """Run evolution loop over tasks."""
    all_results = []
    
    for round_num in range(rounds):
        print(f"\n{'='*50}")
        print(f"EVOLUTION ROUND {round_num + 1}")
        print(f"{'='*50}")
        
        round_results = []
        for i, task in enumerate(tasks):
            print(f"\n📋 Task {i+1}/{len(tasks)}: {task.get('intent', 'Unknown')}")
            result = evolution_step(task, interpreter)
            round_results.append(result)
            print(f"   Success: {result['success']:.2f} {'✅' if result['success'] > 0.6 else '❌'}")
            if result['evolved']:
                print(f"   🔄 Evolved weak component")
        
        # Calculate round stats
        avg_success = sum(r["success"] for r in round_results) / len(round_results)
        print(f"\n📊 Round {round_num + 1} Average Success: {avg_success:.2f}")
        
        all_results.append({
            "round": round_num + 1,
            "results": round_results,
            "avg_success": avg_success
        })
    
    # Final stats
    if len(all_results) > 1:
        first_avg = all_results[0]["avg_success"]
        last_avg = all_results[-1]["avg_success"]
        improvement = last_avg - first_avg
        print(f"\n{'='*50}")
        print(f"EVOLUTION COMPLETE")
        print(f"{'='*50}")
        print(f"First round: {first_avg:.2f}")
        print(f"Last round:  {last_avg:.2f}")
        print(f"Improvement: {improvement:+.2f} {'📈' if improvement > 0 else '📉'}")
    
    return {
        "rounds": all_results,
        "total_tasks": len(tasks) * rounds,
        "improvement": all_results[-1]["avg_success"] - all_results[0]["avg_success"] if len(all_results) > 1 else 0
    }
