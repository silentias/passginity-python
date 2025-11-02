# passginity — Secure Password Generator

A simple and secure password generator for Python. Supports custom character sets, exclusion of ambiguous characters, and cryptographically strong randomness.

Features:
- Uses `secrets` module — cryptographically secure
- Enable/disable letters, digits, and symbols
- Option to exclude confusing characters: `0/O`, `1/I/l`
- Clean and intuitive API

---

## Installation

```bash
pip install passginity
```

---

## Quick Start

```python
from passginity import pass_generate

# Generate a 12-character password
password = pass_generate()
print(password)  # e.g., Kx9$mRt7qW#p

# Exclude ambiguous characters (safe for manual input)
password = pass_generate(exclude_ambiguous=True)
print(password)  # e.g., Hb8n$Ef6vX!s

# Letters and digits only (no symbols)
password = pass_generate(sym_alp=False)
print(password)  # e.g., mK9xRt7qWp2n
```

---

## Function: pass_generate

```python
pass_generate(
    length: int = 12,
    eng_alp: bool = True,
    num_alp: bool = True,
    sym_alp: bool = True,
    exclude_ambiguous: bool = False
) -> str
```

Parameters:
- length — password length (default: 12)
- eng_alp — include Latin letters (a-z, A-Z)
- num_alp — include digits (0-9)
- sym_alp — include special symbols (!@#$%^&*...)
- exclude_ambiguous — exclude easily confused characters: 0, O, 1, I, l

Returns:
- A randomly generated password as a string.

Raises:
- ValueError — if length < 1 or all character sets are disabled.

---

## License

MIT — free to use in personal and commercial projects.
