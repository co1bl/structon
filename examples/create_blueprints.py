"""Create all blueprints including passthrough variants."""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core import create_structon, create_node
import json

os.makedirs('blueprints', exist_ok=True)

# =============================================================================
# SENSE BLUEPRINTS
# =============================================================================

# Passthrough - just get and emit (no LLM)
sense_passthrough = create_structon(
    intent='INTENT_PLACEHOLDER',
    structure_type='sense',
    structure_id='sense_passthrough_blueprint',
    nodes=[
        create_node('s1', 'get', 'sense', 'input', 'Get input', args={'key': 'input'}, output_var='$input'),
        create_node('f1', 'emit', 'feedback', 'output', 'Emit', input_var='$input', output_var='$output')
    ],
    edges=[{'from': 's1', 'to': 'f1'}]
)

# Process - get, LLM, emit
sense_process = create_structon(
    intent='INTENT_PLACEHOLDER',
    structure_type='sense',
    structure_id='sense_blueprint',
    nodes=[
        create_node('s1', 'get', 'sense', 'input', 'Get input', args={'key': 'input'}, output_var='$input'),
        create_node('a1', 'call_llm', 'act', 'process', 'Process', input_var='$input', args={'prompt': 'PROMPT_PLACEHOLDER: {input}'}, output_var='$result'),
        create_node('f1', 'emit', 'feedback', 'output', 'Emit', input_var='$result', output_var='$output')
    ],
    edges=[{'from': 's1', 'to': 'a1'}, {'from': 'a1', 'to': 'f1'}]
)

# =============================================================================
# ACT BLUEPRINTS
# =============================================================================

# Act always uses LLM
act_blueprint = create_structon(
    intent='INTENT_PLACEHOLDER',
    structure_type='act',
    structure_id='act_blueprint',
    nodes=[
        create_node('s1', 'get', 'sense', 'input', 'Get input', args={'key': 'input'}, output_var='$input'),
        create_node('a1', 'call_llm', 'act', 'process', 'Process', input_var='$input', args={'prompt': 'PROMPT_PLACEHOLDER: {input}'}, output_var='$result'),
        create_node('f1', 'emit', 'feedback', 'output', 'Emit', input_var='$result', output_var='$output')
    ],
    edges=[{'from': 's1', 'to': 'a1'}, {'from': 'a1', 'to': 'f1'}]
)

# =============================================================================
# FEEDBACK BLUEPRINTS
# =============================================================================

# Passthrough - just get and emit (no LLM)
feedback_passthrough = create_structon(
    intent='INTENT_PLACEHOLDER',
    structure_type='feedback',
    structure_id='feedback_passthrough_blueprint',
    nodes=[
        create_node('s1', 'get', 'sense', 'input', 'Get result', args={'key': 'result'}, output_var='$result'),
        create_node('f1', 'emit', 'feedback', 'output', 'Emit', input_var='$result', output_var='$output')
    ],
    edges=[{'from': 's1', 'to': 'f1'}]
)

# Process - get, LLM, emit
feedback_process = create_structon(
    intent='INTENT_PLACEHOLDER',
    structure_type='feedback',
    structure_id='feedback_blueprint',
    nodes=[
        create_node('s1', 'get', 'sense', 'input', 'Get result', args={'key': 'result'}, output_var='$result'),
        create_node('a1', 'call_llm', 'act', 'process', 'Process', input_var='$result', args={'prompt': 'PROMPT_PLACEHOLDER: {result}'}, output_var='$feedback'),
        create_node('f1', 'emit', 'feedback', 'output', 'Emit', input_var='$feedback', output_var='$output')
    ],
    edges=[{'from': 's1', 'to': 'a1'}, {'from': 'a1', 'to': 'f1'}]
)

# Learn - get, learn, emit
feedback_learn = create_structon(
    intent='INTENT_PLACEHOLDER',
    structure_type='feedback',
    structure_id='feedback_learn_blueprint',
    nodes=[
        create_node('s1', 'get', 'sense', 'input', 'Get result', args={'key': 'result'}, output_var='$result'),
        create_node('a1', 'learn_from_experience', 'act', 'process', 'Learn', input_var='$result', args={'task': 'Completed task', 'success': True}, output_var='$memory'),
        create_node('f1', 'emit', 'feedback', 'output', 'Emit', input_var='$result', output_var='$output')
    ],
    edges=[{'from': 's1', 'to': 'a1'}, {'from': 'a1', 'to': 'f1'}]
)

# =============================================================================
# SAVE ALL
# =============================================================================

blueprints = [
    ('sense_passthrough', sense_passthrough),
    ('sense', sense_process),
    ('act', act_blueprint),
    ('feedback_passthrough', feedback_passthrough),
    ('feedback', feedback_process),
    ('feedback_learn', feedback_learn)
]

for name, data in blueprints:
    with open(f'blueprints/{name}_blueprint.json', 'w') as f:
        json.dump(data, f, indent=2)
    print(f'✅ blueprints/{name}_blueprint.json')

print('\n✅ All blueprints created!')
