"""
Structon LLM Module

Handles LLM integration for generating and evolving structons.
"""

from .generator import (
    Generator,
    Evolver,
    LLMProvider,
    AnthropicProvider,
    OpenAIProvider,
    MockProvider
)

from .prompts import (
    GENERATE_PROMPT,
    EVOLVE_PROMPT,
    DECOMPOSE_PROMPT,
    SYNTHESIZE_PROMPT,
    REFLECT_PROMPT,
    VALIDATE_PROMPT
)

__all__ = [
    "Generator",
    "Evolver",
    "LLMProvider",
    "AnthropicProvider",
    "OpenAIProvider",
    "MockProvider",
    "GENERATE_PROMPT",
    "EVOLVE_PROMPT",
    "DECOMPOSE_PROMPT",
    "SYNTHESIZE_PROMPT",
    "REFLECT_PROMPT",
    "VALIDATE_PROMPT"
]
