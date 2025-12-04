"""Create pool structons using appropriate blueprints."""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core import generate_structon_via_llm, save_structon

os.makedirs('structons/sense', exist_ok=True)
os.makedirs('structons/act', exist_ok=True)
os.makedirs('structons/feedback', exist_ok=True)

# =============================================================================
# SENSE POOL
# =============================================================================
print('=== SENSE POOL ===')

# Simple passthrough operations
for intent in ["Get input from context"]:
    print(f'⏳ {intent} (passthrough)')
    structon = generate_structon_via_llm(intent, blueprint_name="sense_passthrough")
    structon['structure_type'] = 'sense'
    name = intent.lower().replace(" ", "_")[:20]
    save_structon(structon, f"{name}.json", structon_dir="structons/sense", validate=False)
    print(f'✅ sense/{name}.json')

# Complex operations with LLM
for intent in ["Find relevant memories", "Parse user input"]:
    print(f'⏳ {intent} (with LLM)')
    structon = generate_structon_via_llm(intent, blueprint_name="sense")
    structon['structure_type'] = 'sense'
    name = intent.lower().replace(" ", "_")[:20]
    save_structon(structon, f"{name}.json", structon_dir="structons/sense", validate=False)
    print(f'✅ sense/{name}.json')

# =============================================================================
# ACT POOL - All use LLM
# =============================================================================
print('\n=== ACT POOL ===')

for intent in ["Summarize text", "Analyze content", "Generate response"]:
    print(f'⏳ {intent}')
    structon = generate_structon_via_llm(intent, blueprint_name="act")
    structon['structure_type'] = 'act'
    name = intent.lower().replace(" ", "_")[:20]
    save_structon(structon, f"{name}.json", structon_dir="structons/act", validate=False)
    print(f'✅ act/{name}.json')

# =============================================================================
# FEEDBACK POOL
# =============================================================================
print('\n=== FEEDBACK POOL ===')

# Simple passthrough
for intent in ["Emit result"]:
    print(f'⏳ {intent} (passthrough)')
    structon = generate_structon_via_llm(intent, blueprint_name="feedback_passthrough")
    structon['structure_type'] = 'feedback'
    name = intent.lower().replace(" ", "_")[:20]
    save_structon(structon, f"{name}.json", structon_dir="structons/feedback", validate=False)
    print(f'✅ feedback/{name}.json')

# Learn operation
for intent in ["Learn from experience"]:
    print(f'⏳ {intent} (learn)')
    structon = generate_structon_via_llm(intent, blueprint_name="feedback_learn")
    structon['structure_type'] = 'feedback'
    name = intent.lower().replace(" ", "_")[:20]
    save_structon(structon, f"{name}.json", structon_dir="structons/feedback", validate=False)
    print(f'✅ feedback/{name}.json')

# Complex with LLM
for intent in ["Evaluate quality"]:
    print(f'⏳ {intent} (with LLM)')
    structon = generate_structon_via_llm(intent, blueprint_name="feedback")
    structon['structure_type'] = 'feedback'
    name = intent.lower().replace(" ", "_")[:20]
    save_structon(structon, f"{name}.json", structon_dir="structons/feedback", validate=False)
    print(f'✅ feedback/{name}.json')

print('\n✅ All pools created!')
