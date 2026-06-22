"""Cryptographically secure password generation utilities."""

from dataclasses import dataclass
import secrets
from typing import Dict, List, Optional


ENG_ALPHABET = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
NUM_ALPHABET = "0123456789"
SYM_ALPHABET = "!@#$%^&*()_+-=[]{};':,.<>/?"
AMBIGUOUS = frozenset("0O1Il")


@dataclass(frozen=True)
class PasswordPreset:
    """A named collection of password generation settings."""

    length: int
    eng_alp: bool = True
    num_alp: bool = True
    sym_alp: bool = True
    exclude_ambiguous: bool = False
    exclude_repeating: bool = False
    custom_alphabet: Optional[str] = None


PRESETS: Dict[str, PasswordPreset] = {
    "pin": PasswordPreset(
        length=6,
        eng_alp=False,
        num_alp=True,
        sym_alp=False,
    ),
    "wifi": PasswordPreset(
        length=20,
        eng_alp=True,
        num_alp=True,
        sym_alp=False,
        exclude_ambiguous=True,
    ),
    "high_security": PasswordPreset(
        length=32,
        eng_alp=True,
        num_alp=True,
        sym_alp=True,
    ),
    "memorable": PasswordPreset(
        length=14,
        eng_alp=False,
        num_alp=False,
        sym_alp=False,
        exclude_ambiguous=True,
        custom_alphabet="abcdefghjkmnpqrstuvwxyz23456789",
    ),
}


def _unique_characters(value: str) -> str:
    """Return characters in their original order without duplicates."""

    return "".join(dict.fromkeys(value))


def _build_alphabet(
    eng_alp: bool,
    num_alp: bool,
    sym_alp: bool,
    exclude_ambiguous: bool,
    custom_alphabet: Optional[str],
) -> str:
    if custom_alphabet is not None:
        if not isinstance(custom_alphabet, str):
            raise TypeError("custom_alphabet must be a string.")
        alphabet = custom_alphabet
    else:
        alphabet = ""
        if eng_alp:
            alphabet += ENG_ALPHABET
        if num_alp:
            alphabet += NUM_ALPHABET
        if sym_alp:
            alphabet += SYM_ALPHABET

    if exclude_ambiguous:
        alphabet = "".join(char for char in alphabet if char not in AMBIGUOUS)

    alphabet = _unique_characters(alphabet)
    if not alphabet:
        raise ValueError(
            "The resulting alphabet is empty. Enable a character set or "
            "provide a non-empty custom alphabet."
        )
    return alphabet


def pass_generate(
    length: int = 12,
    eng_alp: bool = True,
    num_alp: bool = True,
    sym_alp: bool = True,
    exclude_ambiguous: bool = False,
    exclude_repeating: bool = False,
    custom_alphabet: Optional[str] = None,
) -> str:
    """Generate one cryptographically secure password.

    ``custom_alphabet`` replaces the built-in character sets when supplied.
    ``exclude_repeating`` prevents a character from appearing more than once.
    """

    if not isinstance(length, int) or isinstance(length, bool):
        raise TypeError("length must be an integer.")
    if length < 1:
        raise ValueError("The password length must be at least 1.")

    alphabet = _build_alphabet(
        eng_alp=eng_alp,
        num_alp=num_alp,
        sym_alp=sym_alp,
        exclude_ambiguous=exclude_ambiguous,
        custom_alphabet=custom_alphabet,
    )

    if exclude_repeating:
        if length > len(alphabet):
            raise ValueError(
                "Password length cannot exceed alphabet size when "
                "exclude_repeating=True."
            )
        return "".join(secrets.SystemRandom().sample(alphabet, length))

    return "".join(secrets.choice(alphabet) for _ in range(length))


def pass_generate_many(count: int = 1, **options: object) -> List[str]:
    """Generate ``count`` passwords using the same options."""

    if not isinstance(count, int) or isinstance(count, bool):
        raise TypeError("count must be an integer.")
    if count < 1:
        raise ValueError("count must be at least 1.")
    return [pass_generate(**options) for _ in range(count)]


def generate_preset(
    name: str,
    count: int = 1,
    length: Optional[int] = None,
    exclude_repeating: Optional[bool] = None,
) -> List[str]:
    """Generate passwords from a named preset.

    ``length`` and ``exclude_repeating`` may override the preset values.
    """

    try:
        preset = PRESETS[name]
    except KeyError as error:
        available = ", ".join(PRESETS)
        raise ValueError(
            f"Unknown preset {name!r}. Available presets: {available}."
        ) from error

    options = {
        "length": preset.length if length is None else length,
        "eng_alp": preset.eng_alp,
        "num_alp": preset.num_alp,
        "sym_alp": preset.sym_alp,
        "exclude_ambiguous": preset.exclude_ambiguous,
        "exclude_repeating": (
            preset.exclude_repeating
            if exclude_repeating is None
            else exclude_repeating
        ),
        "custom_alphabet": preset.custom_alphabet,
    }
    return pass_generate_many(count=count, **options)
