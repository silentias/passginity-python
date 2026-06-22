"""Command-line interface for passginity."""

import argparse
import json
from typing import List, Optional

from . import PRESETS, __version__, generate_preset, pass_generate_many


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="passginity",
        description="Generate cryptographically secure passwords.",
    )
    parser.add_argument("--version", action="version", version=__version__)
    parser.add_argument(
        "--preset",
        choices=PRESETS,
        help="Use a built-in generation preset.",
    )
    parser.add_argument("-n", "--count", type=int, default=1)
    parser.add_argument("-l", "--length", type=int)
    parser.add_argument("--custom-alphabet")
    parser.add_argument("--exclude-ambiguous", action="store_true")
    parser.add_argument("--exclude-repeating", action="store_true")
    parser.add_argument("--no-letters", action="store_true")
    parser.add_argument("--no-digits", action="store_true")
    parser.add_argument("--no-symbols", action="store_true")
    parser.add_argument("--json", action="store_true", dest="as_json")
    return parser


def main(argv: Optional[List[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        if args.preset:
            conflicting = (
                args.custom_alphabet is not None
                or args.exclude_ambiguous
                or args.no_letters
                or args.no_digits
                or args.no_symbols
            )
            if conflicting:
                parser.error(
                    "--preset cannot be combined with alphabet selection options"
                )
            passwords = generate_preset(
                name=args.preset,
                count=args.count,
                length=args.length,
                exclude_repeating=(
                    True if args.exclude_repeating else None
                ),
            )
        else:
            passwords = pass_generate_many(
                count=args.count,
                length=12 if args.length is None else args.length,
                eng_alp=not args.no_letters,
                num_alp=not args.no_digits,
                sym_alp=not args.no_symbols,
                exclude_ambiguous=args.exclude_ambiguous,
                exclude_repeating=args.exclude_repeating,
                custom_alphabet=args.custom_alphabet,
            )
    except (TypeError, ValueError) as error:
        parser.error(str(error))

    if args.as_json:
        payload = {
            "count": len(passwords),
            "preset": args.preset,
            "passwords": passwords,
        }
        print(json.dumps(payload, ensure_ascii=False))
    else:
        print("\n".join(passwords))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
