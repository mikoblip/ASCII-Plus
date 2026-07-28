#!/usr/bin/env python3
"""
ASCII+: The Next Generation of ASCII.
An interactive and feature-rich CLI for generating, converting, and playing with next-gen block-based, colorized ASCII+ art.
"""

import sys
import os
import argparse
import time
import math

# --- ANSI Escapes for Colors & Styles ---
RESET = "\033[0m"
BOLD = "\033[1m"
FAINT = "\033[2m"
ITALIC = "\033[3m"
UNDERLINE = "\033[4m"

# Basic colors
COLORS = {
    "red": "\033[31m",
    "green": "\033[32m",
    "yellow": "\033[33m",
    "blue": "\033[34m",
    "magenta": "\033[35m",
    "cyan": "\033[36m",
    "white": "\033[37m",
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
        # Resolve colors
        colors_rgb = {
            "magenta": (255, 0, 128),
            "cyan": (0, 240, 255),
            "yellow": (255, 230, 0),
            "green": (0, 255, 100),
            "blue": (0, 100, 255),
            "red": (255, 50, 50),
            "orange": (255, 120, 0),
            "purple": (150, 0, 255),
            "white": (255, 255, 255),
        }
        c1 = colors_rgb.get(start_color.lower(), colors_rgb["magenta"])
        c2 = colors_rgb.get(end_color.lower(), colors_rgb["cyan"])

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
            # strip escape codes to write clean plaintext high-fidelity unicode block art
            # but we can save it with ANSI colors too! Let's save standard clean UTF-8
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


def interactive_play():
    """Interactive Playground REPL mode."""
    print(f"{BOLD}{COLORS['magenta']}Welcome to the ASCII+ Interactive Playground!{RESET}")
    print("Type anything and see it converted to beautiful 24-bit Truecolor gradient block-banners.")
    print("Commands:")
    print("  /style <color|gradient> : Change banner coloring style.")
    print("  /exit                  : Return to terminal.")
    print("-" * 80)

    style = "gradient"
    while True:
        try:
            user_input = input(f"{BOLD}{COLORS['cyan']}ASCII+ > {RESET}").strip()
            if not user_input:
                continue

            if user_input.lower() == "/exit":
                print(f"\n{COLORS['yellow']}Goodbye! Keep creating with ASCII+.{RESET}")
                break

            if user_input.lower().startswith("/style "):
                parts = user_input.split(maxsplit=1)
                if len(parts) == 2:
                    style = parts[1].strip().lower()
                    print(f"{COLORS['green']}Style changed to: {style}{RESET}")
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

    # Play
    subparsers.add_parser("play", help="Start an interactive live-preview REPL playground.")

    # Add help option
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
    elif args.command == "play":
        interactive_play()


if __name__ == "__main__":
    main()
