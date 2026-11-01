#!/usr/bin/env python3
"""
Unit and integration tests for ASCII+ features and Markdown support.
"""

import unittest
import os
import tempfile
import subprocess
import sys
import ascii_plus

class TestAsciiPlus(unittest.TestCase):
    def test_banner_generation(self):
        banner_default = ascii_plus.generate_banner("TEST", style="plain")
        self.assertIn("██", banner_default)
        lines = banner_default.splitlines()
        self.assertEqual(len(lines), 5)

        banner_gradient = ascii_plus.generate_banner("HI", style="gradient", start_color="red", end_color="yellow")
        self.assertIn("\033[38;2;", banner_gradient)

    def test_gradient_color_interpolation(self):
        color = ascii_plus.get_gradient_color(255, 0, 0, 0, 255, 0, 5, 0)
        self.assertEqual(color, "\033[38;2;255;0;0m")
        color_mid = ascii_plus.get_gradient_color(0, 0, 0, 100, 100, 100, 3, 1)
        self.assertEqual(color_mid, "\033[38;2;50;50;50m")

    def test_strip_ansi(self):
        styled = f"{ascii_plus.BOLD}{ascii_plus.COLORS['cyan']}Hello World{ascii_plus.RESET}"
        cleaned = ascii_plus._strip_ansi(styled)
        self.assertEqual(cleaned, "Hello World")

    def test_inline_formatting(self):
        bold_text = ascii_plus._apply_inline_formatting("**Bold Text**")
        self.assertIn(ascii_plus.BOLD, bold_text)
        self.assertEqual(ascii_plus._strip_ansi(bold_text), "Bold Text")

        italic_text = ascii_plus._apply_inline_formatting("*Italic Text*")
        self.assertIn(ascii_plus.ITALIC, italic_text)
        self.assertEqual(ascii_plus._strip_ansi(italic_text), "Italic Text")

        code_text = ascii_plus._apply_inline_formatting("`code sample`")
        self.assertIn("code sample", code_text)
        self.assertEqual(ascii_plus._strip_ansi(code_text).strip(), "code sample")

        strike_text = ascii_plus._apply_inline_formatting("~~strikethrough~~")
        self.assertIn(ascii_plus.STRIKETHROUGH, strike_text)
        self.assertEqual(ascii_plus._strip_ansi(strike_text), "strikethrough")

        link_text = ascii_plus._apply_inline_formatting("[Link Title](https://example.com)")
        self.assertIn("Link Title", link_text)
        self.assertIn("https://example.com", link_text)

    def test_render_markdown_elements(self):
        md_sample = (
            "# Title\n"
            "## Subtitle\n"
            "### Section\n"
            "#### Minor\n"
            "> Blockquote test\n"
            "- List item 1\n"
            "  - Nested item\n"
            "1. Numbered item 1\n"
            "2. Numbered item 2\n"
            "---\n"
            "```python\n"
            "print('Hello')\n"
            "```\n"
            "| Col A | Col B |\n"
            "| --- | --- |\n"
            "| Val 1 | Val 2 |\n"
        )
        rendered = ascii_plus.render_markdown(md_sample, style="plain")
        cleaned = ascii_plus._strip_ansi(rendered)

        # Check headings
        self.assertIn("Subtitle", cleaned)
        self.assertIn("Section", cleaned)
        self.assertIn("Minor", cleaned)

        # Check blockquote
        self.assertIn("▌", cleaned)
        self.assertIn("Blockquote test", cleaned)

        # Check list items
        self.assertIn("◆", cleaned)
        self.assertIn("List item 1", cleaned)
        self.assertIn("▸", cleaned)
        self.assertIn("Nested item", cleaned)
        self.assertIn("1.", cleaned)
        self.assertIn("Numbered item 1", cleaned)

        # Check code block border and contents
        self.assertIn("┌──", cleaned)
        self.assertIn("print('Hello')", cleaned)
        self.assertIn("└──", cleaned)

        # Check table
        self.assertIn("╔", cleaned)
        self.assertIn("Col A", cleaned)
        self.assertIn("Val 1", cleaned)
        self.assertIn("╚", cleaned)

    def test_render_markdown_file_and_output(self):
        with tempfile.NamedTemporaryFile("w+", delete=False, suffix=".md") as in_f:
            in_f.write("## Section Heading\n> Test quote\n")
            in_path = in_f.name

        with tempfile.NamedTemporaryFile("w+", delete=False, suffix=".txt") as out_f:
            out_path = out_f.name

        try:
            ascii_plus.render_markdown_file(filepath=in_path, output_filepath=out_path)
            with open(out_path, "r", encoding="utf-8") as f:
                content = f.read()
            self.assertIn("Section Heading", content)
            self.assertIn("Test quote", content)
        finally:
            if os.path.exists(in_path):
                os.remove(in_path)
            if os.path.exists(out_path):
                os.remove(out_path)

    def test_convert_file(self):
        with tempfile.NamedTemporaryFile("w+", delete=False, suffix=".txt") as in_f:
            in_f.write(" .:-*#@ \n")
            in_path = in_f.name

        with tempfile.NamedTemporaryFile("w+", delete=False, suffix=".txt") as out_f:
            out_path = out_f.name

        try:
            ascii_plus.convert_file(in_path, output_filepath=out_path)
            with open(out_path, "r", encoding="utf-8") as f:
                content = f.read()
            self.assertIn("░", content)
            self.assertIn("▒", content)
            self.assertIn("▓", content)
            self.assertIn("█", content)
        finally:
            if os.path.exists(in_path):
                os.remove(in_path)
            if os.path.exists(out_path):
                os.remove(out_path)

    def test_cli_subcommands(self):
        # Test banner CLI
        res = subprocess.run([sys.executable, "ascii_plus.py", "banner", "CLI"], capture_output=True, text=True)
        self.assertEqual(res.returncode, 0)
        self.assertIn("ASCII+ CLI Active", res.stdout)

        # Test markdown CLI with --text
        res = subprocess.run([sys.executable, "ascii_plus.py", "markdown", "--text", "# CLI TEST\n> Quoted"], capture_output=True, text=True)
        self.assertEqual(res.returncode, 0)
        self.assertIn("Quoted", res.stdout)

        # Test table CLI
        res = subprocess.run([sys.executable, "ascii_plus.py", "table"], capture_output=True, text=True)
        self.assertEqual(res.returncode, 0)
        self.assertIn("Standard ASCII (7-bit 0-127)", res.stdout)

        # Test version flag
        res = subprocess.run([sys.executable, "ascii_plus.py", "--version"], capture_output=True, text=True)
        self.assertEqual(res.returncode, 0)
        self.assertIn("ASCII+ CLI", res.stdout)


if __name__ == "__main__":
    unittest.main()
