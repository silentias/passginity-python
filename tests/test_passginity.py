import json
import subprocess
import sys
import unittest

from passginity import (
    PRESETS,
    generate_preset,
    pass_generate,
    pass_generate_many,
)


class PasswordGenerationTests(unittest.TestCase):
    def test_default_password_length(self):
        self.assertEqual(len(pass_generate()), 12)

    def test_custom_alphabet_replaces_standard_alphabets(self):
        password = pass_generate(length=30, custom_alphabet="abc")
        self.assertTrue(set(password) <= set("abc"))

    def test_duplicate_custom_alphabet_characters_are_supported(self):
        password = pass_generate(
            length=3,
            custom_alphabet="aaabbc",
            exclude_repeating=True,
        )
        self.assertEqual(set(password), set("abc"))

    def test_exclude_repeating_returns_unique_characters(self):
        password = pass_generate(length=20, exclude_repeating=True)
        self.assertEqual(len(password), len(set(password)))

    def test_unique_password_cannot_exceed_alphabet(self):
        with self.assertRaises(ValueError):
            pass_generate(
                length=4,
                custom_alphabet="abc",
                exclude_repeating=True,
            )

    def test_ambiguous_characters_are_removed_from_custom_alphabet(self):
        password = pass_generate(
            length=20,
            custom_alphabet="0O1Ilxyz",
            exclude_ambiguous=True,
        )
        self.assertTrue(set(password) <= set("xyz"))

    def test_generate_many(self):
        passwords = pass_generate_many(
            count=5,
            length=8,
            custom_alphabet="abcd",
        )
        self.assertEqual(len(passwords), 5)
        self.assertTrue(all(len(password) == 8 for password in passwords))

    def test_invalid_count(self):
        with self.assertRaises(ValueError):
            pass_generate_many(count=0)

    def test_all_presets_generate_expected_length(self):
        for name, preset in PRESETS.items():
            with self.subTest(preset=name):
                password = generate_preset(name)[0]
                self.assertEqual(len(password), preset.length)

    def test_pin_contains_only_digits(self):
        pin = generate_preset("pin")[0]
        self.assertTrue(pin.isdigit())

    def test_unknown_preset(self):
        with self.assertRaises(ValueError):
            generate_preset("unknown")


class CommandLineTests(unittest.TestCase):
    def test_json_output(self):
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "passginity",
                "--preset",
                "pin",
                "--count",
                "3",
                "--json",
            ],
            check=True,
            capture_output=True,
            text=True,
        )
        payload = json.loads(result.stdout)
        self.assertEqual(payload["count"], 3)
        self.assertEqual(payload["preset"], "pin")
        self.assertEqual(len(payload["passwords"]), 3)


if __name__ == "__main__":
    unittest.main()
