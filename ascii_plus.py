#!/usr/bin/env python3
"""
ASCII+: The Next Generation of ASCII.
An interactive and feature-rich CLI for generating, converting, and playing with next-gen block-based, colorized ASCII+ art.
Includes full high-fidelity Markdown support.
"""

import sys
import os
import re
import argparse
import time
import math

VERSION = "2.0.0-final (Farewell Edition)"

# --- ANSI Escapes for Colors & Styles ---
RESET = "\033[0m"
BOLD = "\033[1m"
FAINT = "\033[2m"
ITALIC = "\033[3m"
UNDERLINE = "\033[4m"
STRIKETHROUGH = "\033[9m"

# Basic colors
COLORS = {
    "red": "\033[31m",
    "green": "\033[32m",
    "yellow": "\033[33m",
    "blue": "\033[34m",
    "magenta": "\033[35m",
    "cyan": "\033[36m",
    "white": "\033[37m",
    "gray": "\033[90m",
}

# 24-bit RGB Color palette lookup
COLORS_RGB = {
    "magenta": (255, 0, 128),
    "cyan": (0, 240, 255),
    "yellow": (255, 230, 0),
    "green": (0, 255, 100),
    "blue": (0, 100, 255),
    "red": (255, 50, 50),
    "orange": (255, 120, 0),
    "purple": (150, 0, 255),
    "white": (255, 255, 255),
    "gray": (120, 120, 120),
}

# --- Logo Definitions ---

# 1. Standard ASCII Logo (used for comparison if needed, but CLI displays ASCII+)
STANDARD_ASCII_LOGO = r"""
    _      ___    ___   ___  ___     _
   /_\    / __|  / __| |_ _||_ _|  _| |_
  / _ \   \__ \ | (__   | |  | |  |_   _|
 /_/ \_\  |___/  \___| |___||___|   |_|
"""

# 2. ASCII+ Next-Gen Logo (High-fidelity Unicode Block Art with Colorized Gradient)
ASCII_PLUS_LOGO_LINES = [
    "   ▟████▙     ▟██████▙    ▟██████▙    ██████   ██████     ▟█▙    ",
    "  ███▛  ▜██  ███▛  ▜██▛  ███▛  ▜██▛     ██       ██       ███    ",
    "  █████████  ▜██████▙    ███            ██       ██     ▟█████▙  ",
    "  ███▛  ▜██    ▜██████▙  ███            ██       ██     ▜█████▛  ",
    "  ███   ███  ▜██▛  ▟██▛  ███▙  ▟██▛     ██       ██       ███    ",
    "  ███   ███   ▜██████▛    ▜██████▛    ██████   ██████     ▜█▛    ",
]

def get_gradient_color(r1, g1, b1, r2, g2, b2, steps, step):
    """Linearly interpolate RGB colors and return ANSI 24-bit color sequence."""
    if steps <= 1:
        return f"\033[38;2;{r1};{g1};{b1}m"
    ratio = step / (steps - 1)
    r = int(r1 + (r2 - r1) * ratio)
    g = int(g1 + (g2 - g1) * ratio)
    b = int(b1 + (b2 - b1) * ratio)
    return f"\033[38;2;{r};{g};{b}m"

def print_ascii_plus_logo():
    """Prints the beautiful multi-color gradient ASCII+ logo."""
    # Cyberpunk purple/magenta to cyan/blue gradient
    color_start = (255, 0, 128) # Vivid Magenta
    color_end = (0, 240, 255)   # Cyber Cyan

    print("\n" + "="*72)
    for i, line in enumerate(ASCII_PLUS_LOGO_LINES):
        color_ansi = get_gradient_color(
            color_start[0], color_start[1], color_start[2],
            color_end[0], color_end[1], color_end[2],
            len(ASCII_PLUS_LOGO_LINES), i
        )
        print(f" {color_ansi}{line}{RESET}")
    print("="*72)
    print(f" {BOLD}{COLORS['yellow']}▶ ASCII+ CLI Active | Next Gen Text & High-Fidelity Block Art Engine{RESET}")
    print("="*72 + "\n")

# --- Simple Font System for Banners ---
# Hand-crafted 5-row ASCII+ characters for the `banner` command
FONT = {
    'A': [" ▟██▙ ", "██▛▜██", "██████", "██▛▜██", "██  ██"],
    'B': ["█████▙", "██▛ ▜█", "█████▛", "██▛ ▜█", "█████▛"],
    'C': [" ▟███▙", "██▛  ▜", "██    ", "██▙  ▟", " ▜███▛"],
    'D': ["█████▙", "██▛ ▜█", "██  ██", "██▙ ▟█", "█████▛"],
    'E': ["██████", "██▛   ", "█████ ", "██▛   ", "██████"],
    'F': ["██████", "██▛   ", "█████ ", "██▛   ", "██    "],
    'G': [" ▟███▙", "██▛  ▜", "██ ▟██", "██▙ ▟█", " ▜████"],
    'H': ["██  ██", "██  ██", "██████", "██  ██", "██  ██"],
    'I': ["██████", "  ██  ", "  ██  ", "  ██  ", "██████"],
    'J': ["  ████", "   ██ ", "   ██ ", "▟  ██ ", "▜███▛ "],
    'K': ["██  ██", "██ ▟█▛", "████▙ ", "██▛▜██", "██  ██"],
    'L': ["██    ", "██    ", "██    ", "██▛   ", "██████"],
    'M': ["██  ██", "██▜▞██", "██ ▛ ██", "██   ██", "██   ██"],
    'N': ["██  ██", "███ ██", "██▜███", "██ ▜██", "██  ██"],
    'O': [" ▟██▙ ", "██▛▜██", "██  ██", "██▙▟██", " ▜██▛ "],
    'P': ["█████▙", "██▛ ▜█", "█████▛", "██▛   ", "██    "],
    'Q': [" ▟██▙ ", "██▛▜██", "██  ██", "██▙▟██", " ▜██▛▜"],
    'R': ["█████▙", "██▛ ▜█", "█████▛", "██▛▜██", "██  ██"],
    'S': [" ▟███▙", "██▛   ", "▜████▙", "   ▜██", "▟████▛"],
    'T': ["██████", "  ██  ", "  ██  ", "  ██  ", "  ██  "],
    'U': ["██  ██", "██  ██", "██  ██", "██▙ ▟█", " ▜███▛"],
    'V': ["██  ██", "██  ██", "▜█▙▟█▛", " ▜██▛ ", "  ▜▛  "],
    'W': ["██   ██", "██   ██", "██ ▞ ▜█", "██▜█▙██", "▜▛   ▜▛"],
    'X': ["██  ██", "▜█▙▟█▛", " ▜██▛ ", "▟█▛▜█▙", "██  ██"],
    'Y': ["██  ██", "▜█▙▟█▛", " ▜██▛ ", "  ██  ", "  ██  "],
    'Z': ["██████", "   ▟█▛", "  ▟█▛ ", " ▟█▛  ", "██████"],
    ' ': ["      ", "      ", "      ", "      ", "      "],
    '1': ["  ██  ", " ▟██  ", "  ██  ", "  ██  ", "██████"],
    '2': ["▟████▙", "   ▟█▛", " ▟█▛  ", "▟█▛   ", "██████"],
    '3': ["██████", "   ▟█▛", "  ███▙", "    ██", "█████▛"],
    '4': ["██  ██", "██  ██", "██████", "    ██", "    ██"],
    '5': ["██████", "██▛   ", "██████", "   ▜██", "█████▛"],
    '6': [" ▟███▙", "██▛   ", "█████▙", "██▛ ▜█", "▜████▛"],
    '7': ["██████", "   ▟█▛", "  ▟█▛ ", " ▟█▛  ", " ▟█▛   "],
    '8': ["▟████▙", "██▛▜██", "▜████▛", "██▛▜██", "▜████▛"],
    '9': ["▟████▙", "██▛▜██", "▜█████", "   ▟█▛", "▟███▛ "],
    '0': ["▟████▙", "██▛▜██", "██ ▟██", "██▙▟██", "▜████▛"],
    '+': ["      ", "  ██  ", "██████", "  ██  ", "      "],
    '-': ["      ", "      ", "██████", "      ", "      "],
    '!': ["  ██  ", "  ██  ", "  ██  ", "      ", "  ██  "],
    '?': ["▟████▙", "    ██", "  ▟█▛ ", "      ", "  ██  "],
    '.': ["      ", "      ", "      ", "      ", "  ██  "],
    ':': ["      ", "  ██  ", "      ", "  ██  ", "      "],
    '#': [" █  █ ", "██████", " █  █ ", "██████", " █  █ "],
    '/': ["    ▟█", "   ▟█▛", "  ▟█▛ ", " ▟█▛  ", "▟█▛   "],
    '\\': ["█▙    ", "▜█▙   ", " ▜█▙  ", "  ▜█▙ ", "   ▜█▙"],
}

# --- Command Implementations ---

def generate_banner(text, style="gradient", start_color="magenta", end_color="cyan"):
    """Generates ASCII+ stylized block banners with color gradient."""
    text = text.upper()
    lines = ["", "", "", "", ""]

    for char in text:
        if char in FONT:
            char_lines = FONT[char]
        else:
            char_lines = FONT['?']
        for i in range(5):
            lines[i] += char_lines[i] + "  "

    # Style/Color implementation
    styled_lines = []
    if style == "gradient":
        c1 = COLORS_RGB.get(start_color.lower(), COLORS_RGB["magenta"])
        c2 = COLORS_RGB.get(end_color.lower(), COLORS_RGB["cyan"])

        for i, line in enumerate(lines):
            color_ansi = get_gradient_color(c1[0], c1[1], c1[2], c2[0], c2[1], c2[2], 5, i)
            styled_lines.append(f"{color_ansi}{line}{RESET}")
    elif style in COLORS:
        color_ansi = COLORS[style]
        for line in lines:
            styled_lines.append(f"{color_ansi}{line}{RESET}")
    elif style == "bold":
        for line in lines:
            styled_lines.append(f"{BOLD}{line}{RESET}")
    else:
        # plain standard blocks
        styled_lines = lines

    return "\n".join(styled_lines)


def display_table():
    """Renders a beautifully structured side-by-side comparison & reference table."""
    print(f"{BOLD}{COLORS['cyan']}=== ASCII vs. ASCII+ Character Map & Extension Table ==={RESET}\n")
    print(f"| Standard ASCII (7-bit 0-127)      | Next-Gen ASCII+ (Extended Unicode & Gradients) |")
    print(f"|-----------------------------------|------------------------------------------------|")
    print(f"| Standard Text Block:              | High-Fidelity Unicode Block Glyphs:            |")
    print(f"|   [#] [=] [*] [@] [H]             |   [█] Full, [▟] Bottom-Right, [▛] Top-Left      |")
    print(f"|                                   |   [▜] Top-Right, [▙] Bottom-Left                |")
    print(f"|                                   |                                                |")
    print(f"| Standard Grayscale Resolution:    | Smooth Continuous Gradients:                   |")
    print(f"|   . , - ~ : ; = ! * # $ @         |   {COLORS['red']}█{COLORS['yellow']}█{COLORS['green']}█{COLORS['cyan']}█{COLORS['blue']}█{COLORS['magenta']}█ (Truecolor, 24-bit RGB interpolation) {RESET} |")
    print(f"|                                   |                                                |")
    print(f"| Interactive CLI Mode:             | REPL Live-Render Sandbox, File Converter CLI   |")
    print(f"|   Non-existent / Static ASCII     |   Real-time ANSI streaming, Custom Banner Fonts|")
    print(f"|                                   |                                                |")
    print(f"| Markdown Support:                 | ASCII+ High-Fidelity Markdown Parser & Styler  |")
    print(f"|   Plain raw text                  |   Block headers, stylized tables, quotes, code |")
    print(f"|-----------------------------------|------------------------------------------------|")
    print("")

    # Showcase standard colors
    print(f"{BOLD}Supported Named Gradient Anchors:{RESET}")
    for name in ["magenta", "cyan", "yellow", "green", "blue", "red", "orange", "purple", "white"]:
        print(f"  • {name.capitalize()}")
    print("")


def convert_file(input_filepath, output_filepath=None, style="gradient"):
    """
    Reads a standard text or ASCII file, upgrades it to colored high-fidelity ASCII+.
    Upgrading maps light/dark densities to various Unicode high-fidelity density blocks:
    ' ' -> ' '
    '.' -> '░'
    ':' -> '▒'
    'o' -> '▓'
    '8' -> '█'
    '#' -> '█'
    And applies color gradients or specific colors.
    """
    if not os.path.exists(input_filepath):
        print(f"{COLORS['red']}Error: Input file '{input_filepath}' does not exist.{RESET}")
        sys.exit(1)

    with open(input_filepath, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

    # Characters replacement mapping standard dense ASCII to High-Fid Unicode density
    mapping = {
        ' ': ' ',
        '.': '░',
        ',': '░',
        '-': '▒',
        '~': '▒',
        ':': '▒',
        ';': '▓',
        '=': '▓',
        '*': '▓',
        '#': '█',
        '@': '█',
        '$': '█',
        '%': '█',
        'o': '▓',
        'O': '▓',
        '0': '█',
        'H': '█',
    }

    lines = content.splitlines()
    converted_lines = []

    color_start = (0, 240, 255) # Cyan
    color_end = (255, 0, 128)   # Magenta

    for i, line in enumerate(lines):
        new_line = ""
        for char in line:
            new_line += mapping.get(char, char)

        # Apply gradient if specified
        if style == "gradient":
            color_ansi = get_gradient_color(
                color_start[0], color_start[1], color_start[2],
                color_end[0], color_end[1], color_end[2],
                len(lines), i
            )
            converted_lines.append(f"{color_ansi}{new_line}{RESET}")
        elif style in COLORS:
            converted_lines.append(f"{COLORS[style]}{new_line}{RESET}")
        else:
            converted_lines.append(new_line)

    result_art = "\n".join(converted_lines)

    if output_filepath:
        with open(output_filepath, "w", encoding="utf-8") as f:
            clean_lines = []
            for i, line in enumerate(lines):
                new_line = "".join(mapping.get(char, char) for char in line)
                clean_lines.append(new_line)
            f.write("\n".join(clean_lines))
        print(f"{COLORS['green']}Successfully upgraded '{input_filepath}' to ASCII+ format in '{output_filepath}'!{RESET}")
    else:
        print(f"\n{BOLD}{COLORS['cyan']}--- Live Upgraded ASCII+ Preview ---{RESET}\n")
        print(result_art)
        print(f"\n{BOLD}{COLORS['cyan']}------------------------------------{RESET}")


def draw_block_art():
    """Generates a high-fidelity vector block-art using mathematical functions and ASCII+ characters."""
    print(f"{BOLD}{COLORS['yellow']}Generating ASCII+ Procedural High-Fidelity Block-Art...{RESET}\n")

    width, height = 60, 20
    # Create gradient circles or wave lines
    for y in range(height):
        line = ""
        for x in range(width):
            # Normalised coords -1 to 1
            nx = (x - width / 2.0) / (width / 4.0)
            ny = (y - height / 2.0) / (height / 2.0)

            # Mathematical functions (Sines / Spheres)
            val = math.sin(nx**2 + ny**2)
            dist = math.sqrt(nx**2 + ny**2)

            # Select Next-Gen Unicode blocks based on distance and pattern
            if dist < 0.4:
                char = "█"
            elif dist < 0.6:
                char = "▓"
            elif dist < 0.8:
                char = "▒"
            elif dist < 1.0:
                char = "░"
            elif val > 0.5:
                char = "▟"
            elif val < -0.5:
                char = "▛"
            else:
                char = " "

            # Gradient Coloring per pixel based on coordinates
            r = int(127 + 127 * math.sin(nx))
            g = int(127 + 127 * math.sin(ny))
            b = int(127 + 127 * math.cos(nx + ny))
            color_ansi = f"\033[38;2;{r};{g};{b}m"
            line += f"{color_ansi}{char}"
        print(line + RESET)
    print("")


# --- Markdown Rendering Engine ---

def _strip_ansi(text):
    """Remove ANSI escape sequences from text for accurate length calculations."""
    ansi_regex = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    return ansi_regex.sub('', text)

def _apply_inline_formatting(text, default_color=None):
    """
    Applies inline Markdown formatting (bold, italic, strikethrough, inline code)
    and retains default color styling if present.
    """
    base_reset = RESET + (default_color if default_color else "")

    # Inline code: `code`
    def replace_code(m):
        code_text = m.group(1)
        return f"\033[48;5;236m\033[38;5;220m {code_text} {RESET}{base_reset}"
    text = re.sub(r'`([^`]+)`', replace_code, text)

    # Bold & Italic: ***text*** or ___text___
    def replace_bold_italic(m):
        return f"{BOLD}{ITALIC}{m.group(1)}{RESET}{base_reset}"
    text = re.sub(r'\*\*\*([^\*]+)\*\*\*', replace_bold_italic, text)
    text = re.sub(r'___([^_]+)___', replace_bold_italic, text)

    # Bold: **text** or __text__
    def replace_bold(m):
        return f"{BOLD}{m.group(1)}{RESET}{base_reset}"
    text = re.sub(r'\*\*([^\*]+)\*\*', replace_bold, text)
    text = re.sub(r'__([^_]+)__', replace_bold, text)

    # Italic: *text* or _text_
    def replace_italic(m):
        return f"{ITALIC}{m.group(1)}{RESET}{base_reset}"
    text = re.sub(r'\*([^\*]+)\*', replace_italic, text)
    text = re.sub(r'_([^_]+)_', replace_italic, text)

    # Strikethrough: ~~text~~
    def replace_strike(m):
        return f"{STRIKETHROUGH}{m.group(1)}{RESET}{base_reset}"
    text = re.sub(r'~~([^~]+)~~', replace_strike, text)

    # Links: [text](url) -> text (url)
    def replace_link(m):
        link_text = m.group(1)
        url = m.group(2)
        return f"{UNDERLINE}{COLORS['cyan']}{link_text}{RESET}{base_reset} {FAINT}({url}){RESET}{base_reset}"
    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', replace_link, text)

    return text

def _render_ascii_table(rows, style="gradient", start_color="magenta", end_color="cyan"):
    """Renders parsed markdown table rows with high-fidelity Unicode box characters."""
    if not rows:
        return []

    # Calculate column count and column widths
    num_cols = max(len(r) for r in rows)
    col_widths = [0] * num_cols

    cleaned_rows = []
    for row in rows:
        padded = row + [""] * (num_cols - len(row))
        cleaned_cells = [cell.strip() for cell in padded]
        cleaned_rows.append(cleaned_cells)
        for idx, cell in enumerate(cleaned_cells):
            plain_len = len(_strip_ansi(cell))
            if plain_len > col_widths[idx]:
                col_widths[idx] = plain_len

    # Ensure min width of 3 for nice display
    col_widths = [max(w, 3) for w in col_widths]

    # Resolve gradient colors for borders
    c1 = COLORS_RGB.get(start_color.lower(), COLORS_RGB["magenta"])
    c2 = COLORS_RGB.get(end_color.lower(), COLORS_RGB["cyan"])

    border_color = get_gradient_color(c1[0], c1[1], c1[2], c2[0], c2[1], c2[2], 5, 2)
    header_color = f"{BOLD}{COLORS['cyan']}"

    rendered = []

    # Top border: ╔═══╦═══╗
    top_parts = ["═" * (w + 2) for w in col_widths]
    rendered.append(f"{border_color}╔" + "╦".join(top_parts) + f"╗{RESET}")

    for r_idx, row in enumerate(cleaned_rows):
        # Format cells
        cell_strs = []
        is_header = (r_idx == 0)
        for c_idx, cell in enumerate(row):
            formatted_cell = _apply_inline_formatting(cell, default_color=header_color if is_header else None)
            plain_len = len(_strip_ansi(cell))
            padding = " " * (col_widths[c_idx] - plain_len)
            cell_strs.append(f" {formatted_cell}{padding} ")

        rendered.append(f"{border_color}║{RESET}" + f"{border_color}║{RESET}".join(cell_strs) + f"{border_color}║{RESET}")

        if is_header and len(cleaned_rows) > 1:
            # Header separator: ╠═══╬═══╣
            sep_parts = ["═" * (w + 2) for w in col_widths]
            rendered.append(f"{border_color}╠" + "╬".join(sep_parts) + f"╣{RESET}")

    # Bottom border: ╚═══╩═══╝
    bot_parts = ["═" * (w + 2) for w in col_widths]
    rendered.append(f"{border_color}╚" + "╩".join(bot_parts) + f"╝{RESET}")

    return rendered

def render_markdown(markdown_text, style="gradient", start_color="magenta", end_color="cyan", max_width=72):
    """
    Renders Markdown into high-fidelity ASCII+ formatted terminal output.
    Supports headings (with ASCII+ banners / block ribbons), blockquotes,
    code blocks, lists, horizontal rules, tables, and inline typography.
    """
    c1 = COLORS_RGB.get(start_color.lower(), COLORS_RGB["magenta"])
    c2 = COLORS_RGB.get(end_color.lower(), COLORS_RGB["cyan"])

    lines = markdown_text.splitlines()
    output_lines = []
    i = 0
    num_lines = len(lines)

    in_code_block = False
    code_block_lang = ""
    code_block_lines = []

    in_table = False
    table_rows = []

    def flush_table():
        nonlocal in_table, table_rows, output_lines
        if table_rows:
            rendered = _render_ascii_table(table_rows, style=style, start_color=start_color, end_color=end_color)
            output_lines.extend(rendered)
            output_lines.append("")
            table_rows = []
        in_table = False

    while i < num_lines:
        raw_line = lines[i]
        stripped = raw_line.strip()

        # 1. Code blocks: ```
        if stripped.startswith("```"):
            if not in_code_block:
                if in_table:
                    flush_table()
                in_code_block = True
                code_block_lang = stripped[3:].strip()
                code_block_lines = []
                i += 1
                continue
            else:
                # Close code block
                in_code_block = False
                box_width = max(max_width, max((len(l) for l in code_block_lines), default=0) + 6)
                box_width = min(box_width, 80)
                lang_tag = f" {code_block_lang} " if code_block_lang else ""
                border_color = COLORS['blue'] if style != "gradient" else get_gradient_color(c1[0], c1[1], c1[2], c2[0], c2[1], c2[2], 5, 3)

                header_border = f"{border_color}┌──{BOLD}{COLORS['yellow']}{lang_tag}{RESET}{border_color}" + "─" * (box_width - 3 - len(lang_tag)) + f"┐{RESET}"
                output_lines.append(header_border)

                for c_line in code_block_lines:
                    pad = " " * max(0, box_width - 4 - len(c_line))
                    output_lines.append(f"{border_color}│{RESET}  {COLORS['green']}{c_line}{RESET}{pad}{border_color}│{RESET}")

                footer_border = f"{border_color}└──" + "─" * (box_width - 4) + f"┘{RESET}"
                output_lines.append(footer_border)
                output_lines.append("")
                i += 1
                continue

        if in_code_block:
            code_block_lines.append(raw_line)
            i += 1
            continue

        # 2. Tables: lines starting with | or matching markdown table rows
        if stripped.startswith("|") and stripped.endswith("|") and stripped.count("|") >= 2:
            # Check if it's a separator line like |---|---|
            inner = stripped[1:-1].strip()
            is_separator = all(ch in "- |:" for ch in inner)
            if is_separator:
                # Just skip the separator line as _render_ascii_table handles borders
                i += 1
                continue
            cells = [c.strip() for c in stripped[1:-1].split("|")]
            table_rows.append(cells)
            in_table = True
            i += 1
            continue
        elif in_table:
            flush_table()

        # 3. Horizontal Rules: ---, ***, ___
        if re.match(r'^(?:-{3,}|\*{3,}|_{3,})$', stripped):
            hr_parts = []
            steps = min(max_width, 60)
            for s in range(steps):
                col_ansi = get_gradient_color(c1[0], c1[1], c1[2], c2[0], c2[1], c2[2], steps, s)
                hr_parts.append(f"{col_ansi}━")
            output_lines.append("".join(hr_parts) + RESET)
            output_lines.append("")
            i += 1
            continue

        # 4. Headings
        # H1: # Heading
        h1_match = re.match(r'^#\s+(.+)$', stripped)
        if h1_match:
            heading_text = h1_match.group(1).strip()
            # If short enough and alphanumeric, render full ASCII+ banner
            can_banner = len(heading_text) <= 12 and all(ch.upper() in FONT for ch in heading_text)
            if can_banner:
                banner = generate_banner(heading_text, style=style, start_color=start_color, end_color=end_color)
                output_lines.append(banner)
            else:
                bar_len = min(len(heading_text) + 8, max_width)
                top_border = ""
                steps = bar_len
                for s in range(steps):
                    col_ansi = get_gradient_color(c1[0], c1[1], c1[2], c2[0], c2[1], c2[2], steps, s)
                    top_border += f"{col_ansi}█"
                output_lines.append(f"{top_border}{RESET}")
                output_lines.append(f" {BOLD}{COLORS['white']}▟█  {heading_text.upper()}  █▙{RESET}")
                output_lines.append(f"{top_border}{RESET}")
            output_lines.append("")
            i += 1
            continue

        # H2: ## Heading
        h2_match = re.match(r'^##\s+(.+)$', stripped)
        if h2_match:
            heading_text = h2_match.group(1).strip()
            c_accent = get_gradient_color(c1[0], c1[1], c1[2], c2[0], c2[1], c2[2], 5, 1)
            output_lines.append(f"{c_accent}▛██▜{RESET} {BOLD}{COLORS['cyan']}{heading_text}{RESET}")
            output_lines.append(f"{c_accent}▜██▛{RESET} " + f"{FAINT}{'═' * min(len(heading_text) + 4, max_width)}{RESET}")
            output_lines.append("")
            i += 1
            continue

        # H3: ### Heading
        h3_match = re.match(r'^###\s+(.+)$', stripped)
        if h3_match:
            heading_text = h3_match.group(1).strip()
            c_accent = get_gradient_color(c1[0], c1[1], c1[2], c2[0], c2[1], c2[2], 5, 3)
            output_lines.append(f"{c_accent}◆ {BOLD}{COLORS['yellow']}{heading_text}{RESET}")
            output_lines.append("")
            i += 1
            continue

        # H4 - H6: #### Heading
        hx_match = re.match(r'^(#{4,6})\s+(.+)$', stripped)
        if hx_match:
            level = len(hx_match.group(1))
            heading_text = hx_match.group(2).strip()
            glyph = "▸" if level == 4 else "•"
            output_lines.append(f"{COLORS['magenta']}{glyph} {BOLD}{heading_text}{RESET}")
            output_lines.append("")
            i += 1
            continue

        # 5. Blockquotes: > quote
        if stripped.startswith(">"):
            quote_text = stripped.lstrip(">").strip()
            formatted_quote = _apply_inline_formatting(quote_text, default_color=ITALIC + COLORS['cyan'])
            c_bar = get_gradient_color(c1[0], c1[1], c1[2], c2[0], c2[1], c2[2], 5, 2)
            output_lines.append(f"{c_bar}▌{RESET}  {ITALIC}{COLORS['cyan']}{formatted_quote}{RESET}")
            i += 1
            continue

        # 6. Unordered lists: -, *, +
        list_match = re.match(r'^(\s*)[-\*\+]\s+(.+)$', raw_line)
        if list_match:
            indent = list_match.group(1)
            item_text = list_match.group(2)
            bullet = "◆" if len(indent) == 0 else "▸"
            formatted_item = _apply_inline_formatting(item_text)
            c_bullet = get_gradient_color(c1[0], c1[1], c1[2], c2[0], c2[1], c2[2], 5, 1 if len(indent) == 0 else 3)
            output_lines.append(f"{indent}  {c_bullet}{bullet}{RESET} {formatted_item}")
            i += 1
            continue

        # 7. Ordered lists: 1. Item
        num_list_match = re.match(r'^(\s*)(\d+)\.\s+(.+)$', raw_line)
        if num_list_match:
            indent = num_list_match.group(1)
            num = num_list_match.group(2)
            item_text = num_list_match.group(3)
            formatted_item = _apply_inline_formatting(item_text)
            output_lines.append(f"{indent}  {BOLD}{COLORS['yellow']}{num}.{RESET} {formatted_item}")
            i += 1
            continue

        # 8. Regular paragraph / empty line
        if not stripped:
            output_lines.append("")
        else:
            formatted_p = _apply_inline_formatting(stripped)
            output_lines.append(formatted_p)

        i += 1

    # End of loop, check if table pending
    if in_table:
        flush_table()

    return "\n".join(output_lines)


def render_markdown_file(filepath=None, text=None, output_filepath=None, style="gradient", start_color="magenta", end_color="cyan"):
    """Renders Markdown input from a file or raw string, displays it and optionally writes to output file."""
    if filepath:
        if not os.path.exists(filepath):
            print(f"{COLORS['red']}Error: Input Markdown file '{filepath}' does not exist.{RESET}")
            sys.exit(1)
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
    elif text is not None:
        content = text
    else:
        print(f"{COLORS['red']}Error: No Markdown content or file specified.{RESET}")
        return

    rendered = render_markdown(content, style=style, start_color=start_color, end_color=end_color)

    if output_filepath:
        with open(output_filepath, "w", encoding="utf-8") as f:
            f.write(_strip_ansi(rendered))
        print(f"{COLORS['green']}Successfully saved rendered ASCII+ Markdown to '{output_filepath}'!{RESET}")
    else:
        print(f"\n{BOLD}{COLORS['cyan']}=== ASCII+ Markdown Rendered Output ==={RESET}\n")
        print(rendered)
        print(f"\n{BOLD}{COLORS['cyan']}======================================={RESET}\n")


def interactive_play():
    """Interactive Playground REPL mode."""
    print(f"{BOLD}{COLORS['magenta']}Welcome to the ASCII+ Interactive Playground! (v{VERSION}){RESET}")
    print("Type anything and see it converted to beautiful 24-bit Truecolor gradient block-banners.")
    print("Commands:")
    print("  /style <color|gradient> : Change banner coloring style.")
    print("  /md <markdown_text>     : Render high-fidelity ASCII+ Markdown live.")
    print("  /exit                  : Return to terminal.")
    print("-" * 80)

    style = "gradient"
    while True:
        try:
            user_input = input(f"{BOLD}{COLORS['cyan']}ASCII+ > {RESET}").strip()
            if not user_input:
                continue

            if user_input.lower() == "/exit":
                print(f"\n{COLORS['yellow']}Goodbye! Thank you for using ASCII+. Farewell, Jules! 🚀{RESET}")
                break

            if user_input.lower().startswith("/style "):
                parts = user_input.split(maxsplit=1)
                if len(parts) == 2:
                    style = parts[1].strip().lower()
                    print(f"{COLORS['green']}Style changed to: {style}{RESET}")
                continue

            if user_input.lower().startswith("/md "):
                parts = user_input.split(maxsplit=1)
                if len(parts) == 2:
                    rendered_md = render_markdown(parts[1], style=style)
                    print("\n" + rendered_md + "\n")
                continue

            # Generate the live banner
            banner = generate_banner(user_input, style=style)
            print("\n" + banner + "\n")

        except (KeyboardInterrupt, EOFError):
            print(f"\n\n{COLORS['yellow']}Exiting ASCII+ Playground.{RESET}")
            break


# --- Main CLI Entrypoint ---

def main():
    parser = argparse.ArgumentParser(
        description="ASCII+ CLI: Next-Gen block-based stylized and colorized text art generator.",
        add_help=False
    )

    # Subcommands and arguments
    subparsers = parser.add_subparsers(dest="command", help="ASCII+ Subcommands")

    # Banner
    banner_parser = subparsers.add_parser("banner", help="Generate custom ASCII+ stylized banner text.")
    banner_parser.add_argument("text", help="The text to convert to a banner.")
    banner_parser.add_argument("--style", default="gradient", help="Style of coloring: 'gradient' or standard named colors (e.g. red, green, cyan).")
    banner_parser.add_argument("--start", default="magenta", help="Start color of gradient (magenta, cyan, yellow, green, blue, red).")
    banner_parser.add_argument("--end", default="cyan", help="End color of gradient (magenta, cyan, yellow, green, blue, red).")

    # Table
    subparsers.add_parser("table", help="Show side-by-side comparison of standard ASCII vs ASCII+ characters.")

    # Convert
    convert_parser = subparsers.add_parser("convert", help="Upgrade traditional dense ASCII artwork to next-gen ASCII+ Block format.")
    convert_parser.add_argument("file", help="Input traditional ASCII text file path.")
    convert_parser.add_argument("--out", default=None, help="Output upgraded ASCII+ unicode file path (optional).")
    convert_parser.add_argument("--style", default="gradient", help="Gradation styling or color.")

    # Draw
    subparsers.add_parser("draw", help="Generate procedurally synthesized mathematical block art using ASCII+ blocks.")

    # Markdown
    md_parser = subparsers.add_parser("markdown", help="Render Markdown documents into high-fidelity ASCII+ stylized terminal output.")
    md_parser.add_argument("file", nargs="?", default=None, help="Input Markdown file path.")
    md_parser.add_argument("--text", "-t", default=None, help="Direct Markdown string to render.")
    md_parser.add_argument("--out", "-o", default=None, help="Output plain/clean rendered Markdown file path.")
    md_parser.add_argument("--style", default="gradient", help="Color style: 'gradient', 'bold', 'plain', or named color.")
    md_parser.add_argument("--start", default="magenta", help="Start color of gradient anchor.")
    md_parser.add_argument("--end", default="cyan", help="End color of gradient anchor.")

    # Play
    subparsers.add_parser("play", help="Start an interactive live-preview REPL playground.")

    # Global options
    parser.add_argument("-v", "--version", action="version", version=f"ASCII+ CLI {VERSION}", help="Show ASCII+ version.")
    parser.add_argument("-h", "--help", action="store_true", help="Show this help message and exit.")

    # Parse args
    args = parser.parse_args()

    # Display ASCII+ Logo upon execution of any command or when no args are passed
    print_ascii_plus_logo()

    if args.help or not args.command:
        parser.print_help()
        print("\nExamples:")
        print("  python3 ascii_plus.py banner \"Hello World\"")
        print("  python3 ascii_plus.py banner \"Next Gen\" --style green")
        print("  python3 ascii_plus.py markdown README.md")
        print("  python3 ascii_plus.py markdown --text \"# Hello ASCII+\\n> Next-gen text\"")
        print("  python3 ascii_plus.py table")
        print("  python3 ascii_plus.py draw")
        print("  python3 ascii_plus.py play")
        return

    if args.command == "banner":
        banner_art = generate_banner(args.text, style=args.style, start_color=args.start, end_color=args.end)
        print(banner_art)
        print("")
    elif args.command == "table":
        display_table()
    elif args.command == "convert":
        convert_file(args.file, output_filepath=args.out, style=args.style)
    elif args.command == "draw":
        draw_block_art()
    elif args.command == "markdown":
        if not args.file and not args.text:
            print(f"{COLORS['red']}Error: Please specify a markdown file or pass text with --text.{RESET}")
            sys.exit(1)
        render_markdown_file(
            filepath=args.file,
            text=args.text,
            output_filepath=args.out,
            style=args.style,
            start_color=args.start,
            end_color=args.end
        )
    elif args.command == "play":
        interactive_play()


if __name__ == "__main__":
    main()
