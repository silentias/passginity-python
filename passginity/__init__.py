"""Public API for passginity."""

from .passginity import (
    PRESETS,
    PasswordPreset,
    generate_preset,
    pass_generate,
    pass_generate_many,
)

__all__ = [
    "PRESETS",
    "PasswordPreset",
    "generate_preset",
    "pass_generate",
    "pass_generate_many",
]

__version__ = "0.2.0"
