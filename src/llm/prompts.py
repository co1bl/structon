"""
LLM Prompts Module

Contains prompt templates for structon generation and evolution.
"""

GENERATE_PROMPT = """You are generating a structon - a self-similar cognitive unit.

A structon has three phases: SENSE (perceive), ACT (do), FEEDBACK (learn).
Each phase can contain other structons, enabling infinite nesting.

BLUEPRINT (follow this schema):
{blueprint}

TASK:
{task}

CONTEXT:
{context}

AVAILABLE ATOMIC FUNCTIONS:
{atomics}

REQUIREMENTS:
1. Follow the blueprint schema exactly
2. Include nodes for sense, act, and feedback phases
3. Set appropriate tension values (0.0-1.0, higher = more urgent)
4. Set appropriate importance values (0.0-1.0)
5. Use available atomic functions in nodes
6. Connect nodes with edges (from → to)
7. Output ONLY valid JSON, no explanation

EXAMPLE NODE:
{{
  "id": "s1",
  "type": "input",
  "phase": "sense",
  "description": "Load current state",
  "atomic": "get",
  "args": {{"key": "state"}},
  "output": "$state"
}}

Generate the structon now:
"""

EVOLVE_PROMPT = """You are evolving a structon based on execution feedback.

ORIGINAL STRUCTON:
{structon}

EXECUTION FEEDBACK:
{feedback}

ERROR (if any): {error}

REQUIREMENTS:
1. Analyze what went wrong (if anything)
2. Improve the structon to address issues
3. Keep the same structure_id but increment version
4. Maintain valid schema
5. Output ONLY valid JSON

EVOLUTION STRATEGIES:
- If nodes failed: adjust atomic functions or args
- If tension too high: add more decomposition
- If tension too low: consolidate nodes
- If error occurred: add error handling nodes
- If slow: optimize node order or remove redundancy

Generate the evolved structon now:
"""

DECOMPOSE_PROMPT = """Break down this task into sub-structons.

TASK: {task}
CONTEXT: {context}

Create 2-5 sub-structons, each handling part of the task.
Each sub-structon should have sense, act, feedback phases.

Output as JSON array of structons.
"""

SYNTHESIZE_PROMPT = """Synthesize results from multiple structons.

RESULTS:
{results}

ORIGINAL GOAL: {goal}

Create a final answer that:
1. Combines insights from all results
2. Addresses the original goal
3. Notes any conflicts or uncertainties

Output your synthesis:
"""

REFLECT_PROMPT = """Reflect on structon execution.

STRUCTON: {structon}
RESULT: {result}
DURATION: {duration}ms

Questions to consider:
1. Was the goal achieved?
2. What worked well?
3. What could be improved?
4. What should the system learn?

Provide reflection as JSON:
{{
  "goal_achieved": true/false,
  "success_factors": [...],
  "improvement_areas": [...],
  "learnings": [...]
}}
"""

VALIDATE_PROMPT = """Validate this structon for correctness.

STRUCTON:
{structon}

Check for:
1. All required fields present
2. Valid node types and phases
3. Valid atomic function references
4. Correct edge connections (no cycles, no dangling)
5. Reasonable tension/importance values

Output validation result as JSON:
{{
  "valid": true/false,
  "errors": [...],
  "warnings": [...],
  "suggestions": [...]
}}
"""

WORLD_MODEL_UPDATE_PROMPT = """Update world model based on observation.

CURRENT WORLD MODEL:
{world_model}

NEW OBSERVATION:
{observation}

Update the world model to incorporate this observation.
Maintain consistency with existing beliefs.
Flag any conflicts.

Output updated world model as JSON.
"""

META_REASONING_PROMPT = """Analyze current cognitive state.

ACTIVE STRUCTONS: {active_count}
HIGHEST TENSION: {max_tension}
RECENT HISTORY: {history}

Questions:
1. Am I making progress toward goals?
2. Am I stuck in loops?
3. Should I change strategy?
4. What should I focus on next?

Output meta-analysis as JSON:
{{
  "making_progress": true/false,
  "stuck": true/false,
  "strategy_change_needed": true/false,
  "next_focus": "...",
  "reasoning": "..."
}}
"""
