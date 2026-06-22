# passginity — Secure Password Generator

`passginity` is a configurable password generator for Python. It uses the
standard-library `secrets` module, making every generated password suitable
for security-sensitive use.

## Features

- cryptographically secure randomness;
- built-in letters, digits, and symbols;
- custom alphabets;
- optional removal of ambiguous characters (`0/O`, `1/I/l`);
- optional prevention of repeated characters;
- generation of multiple passwords at once;
- built-in `pin`, `wifi`, `high_security`, and `memorable` presets;
- command-line interface with plain-text and JSON output;
- no runtime dependencies.

## Installation

Install from PyPI:

```bash
pip install passginity
```

Install the current project locally:

```bash
pip install -e .
```

The package requires Python 3.8 or newer.

## Quick start

```python
from passginity import pass_generate

password = pass_generate()
print(password)  # e.g. Kx9$mRt7qW#p
```

### Exclude repeated characters

Every character in the result is unique:

```python
password = pass_generate(length=16, exclude_repeating=True)
```

If the requested length is greater than the number of unique available
characters, `ValueError` is raised.

### Use a custom alphabet

When `custom_alphabet` is supplied, it replaces the built-in letters, digits,
and symbols:

```python
password = pass_generate(
    length=10,
    custom_alphabet="ABCDEF012345",
)
```

Duplicate characters in a custom alphabet are removed automatically. The
`exclude_ambiguous` option also applies to custom alphabets.

### Generate multiple passwords

```python
from passginity import pass_generate_many

passwords = pass_generate_many(
    count=5,
    length=20,
    exclude_ambiguous=True,
)
```

`pass_generate_many()` accepts the same generation options as
`pass_generate()`.

## Presets

```python
from passginity import generate_preset

pins = generate_preset("pin", count=3)
wifi_password = generate_preset("wifi")[0]
secure_password = generate_preset("high_security")[0]
memorable_password = generate_preset("memorable")[0]
```

| Preset | Length | Character set | Purpose |
| --- | ---: | --- | --- |
| `pin` | 6 | digits | Numeric access codes |
| `wifi` | 20 | letters and digits without ambiguous characters | Easy manual entry |
| `high_security` | 32 | letters, digits, and symbols | Maximum-strength credentials |
| `memorable` | 14 | lowercase letters and digits without ambiguous characters | Easier reading and dictation |

Preset length and repeated-character behavior can be overridden:

```python
passwords = generate_preset(
    "high_security",
    count=2,
    length=40,
    exclude_repeating=True,
)
```

Available presets can also be inspected through the public `PRESETS`
dictionary.

## API

### `pass_generate`

```python
pass_generate(
    length: int = 12,
    eng_alp: bool = True,
    num_alp: bool = True,
    sym_alp: bool = True,
    exclude_ambiguous: bool = False,
    exclude_repeating: bool = False,
    custom_alphabet: Optional[str] = None,
) -> str
```

### `pass_generate_many`

```python
pass_generate_many(count: int = 1, **options) -> List[str]
```

### `generate_preset`

```python
generate_preset(
    name: str,
    count: int = 1,
    length: Optional[int] = None,
    exclude_repeating: Optional[bool] = None,
) -> List[str]
```

## Command-line interface

After installation, use the `passginity` command:

```bash
passginity --length 20
passginity --count 5 --exclude-ambiguous
passginity --custom-alphabet ABCDEF012345 --length 12
passginity --length 20 --exclude-repeating
```

The module form works without installing a console script:

```bash
python -m passginity --preset wifi
```

### Presets in the CLI

```bash
passginity --preset pin --count 3
passginity --preset high_security
passginity --preset memorable --length 20
```

### JSON output

Use `--json` for scripts, APIs, or other automated consumers:

```bash
passginity --preset pin --count 3 --json
```

Example output:

```json
{
  "count": 3,
  "preset": "pin",
  "passwords": ["482901", "137640", "925183"]
}
```

Without `--json`, each generated password is printed on a separate line.

### CLI options

```text
--preset {pin,wifi,high_security,memorable}
-n, --count NUMBER
-l, --length NUMBER
--custom-alphabet CHARACTERS
--exclude-ambiguous
--exclude-repeating
--no-letters
--no-digits
--no-symbols
--json
--version
```

Alphabet selection options cannot be combined with a preset. `--length` and
`--exclude-repeating` are valid preset overrides.

## Error handling

The library raises:

- `TypeError` when `length`, `count`, or `custom_alphabet` has an invalid type;
- `ValueError` when length or count is less than one;
- `ValueError` when the resulting alphabet is empty;
- `ValueError` when a unique password is longer than its alphabet;
- `ValueError` when an unknown preset is requested.

## Development

Run the test suite with the Python standard library:

```bash
python -m unittest discover -s tests -v
```

## License

MIT — free to use in personal and commercial projects.
