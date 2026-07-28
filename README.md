# ASCII-Plus

```text
   _    ____   ____ ___ ___       _
  / \  / ___| / ___|_ _|_ _|     |_|
 / _ \ \___ \| |    | | | |     _|_|_
/ ___ \ ___) | |___ | | | |      |_|
/_/   \_\____/ \____|___|___|
```

> **The Next Generation of ASCII.** Extending the classic 7-bit standard into a high-fidelity, 24-bit Truecolor block-art ecosystem.

---

## 🌟 Introduction

**ASCII+ (ASCII-Plus)** represents the next evolutionary leap in text-based interface design. While standard 1963 ASCII limited developers to 128 characters of basic 7-bit text, ASCII+ leverages modern Unicode high-fidelity blocks, 24-bit Truecolor ANSI gradients, procedurally synthesized vector styling, and an interactive CLI engine to bring console interfaces into the 21st century.

This repository provides the core ASCII+ CLI tool—a feature-complete text styling, banners, conversion, and interactive engine.

---

## 🚀 Key Features

*   **⚡ Next-Gen ASCII+ Logo**: Renders high-fidelity Unicode block art with beautiful linear RGB gradient interpolation in CLI mode.
*   **🎨 Truecolor Linear Gradients**: Beautiful custom start/end colors (e.g. Cyberpunk Magenta to Cyber Cyan, Sunset Red to Gold Yellow) with custom linear interpolation across rows.
*   **🧱 High-Fidelity Character Resolution**: Hand-crafted 5-row typography characters using specialized Unicode quadrant blocks (`█`, `▟`, `▛`, `▜`, `▙`) for incredibly smooth curves and borders.
*   **♻️ Smart ASCII to ASCII+ Conversion**: Upgrades legacy low-density ASCII text files into highly polished, colored, high-fidelity density maps (` `, `░`, `▒`, `▓`, `█`).
*   **🌀 Procedural Vector Block-Art**: Generates mathematically computed graphic scenes dynamically based on coordinate geometry and color spaces.
*   **🎮 Interactive REPL Playground**: Start a live terminal playground, instantly rendering custom banners with continuous input.

---

## 🛠️ CLI Mode Installation & Quick Start

The ASCII+ CLI is written in zero-dependency, standard library Python 3. It runs out of the box in any modern terminal (macOS, Linux, WSL/Windows Terminal) that supports UTF-8 and ANSI escape codes.

### Running the CLI
```bash
python3 ascii_plus.py --help
```

---

## 📖 CLI Commands Guide

The CLI supports several modes of operation:

### 1. `banner`
Generates high-fidelity colored banners of text.
```bash
python3 ascii_plus.py banner "ASCII-PLUS" --style gradient --start magenta --end cyan
```
**Options:**
*   `--style`: Style of color. Can be `gradient` (default), `bold`, `plain`, or a named color: `red`, `green`, `yellow`, `blue`, `magenta`, `cyan`, `white`.
*   `--start`: Starting color anchor for the linear gradient.
*   `--end`: Ending color anchor for the linear gradient.

Supported named gradient anchors include: `magenta`, `cyan`, `yellow`, `green`, `blue`, `red`, `orange`, `purple`, and `white`.

### 2. `table`
Prints a side-by-side comparison matrix showing how legacy ASCII is upgraded to the high-fidelity features of ASCII+.
```bash
python3 ascii_plus.py table
```

### 3. `convert`
Takes any traditional file containing standard ASCII art and automatically upgrades it to high-fidelity ASCII+ styling.
```bash
# Print upgraded ASCII+ directly to console
python3 ascii_plus.py convert legacy_art.txt

# Save the upgraded high-fidelity plaintext art to a new file
python3 ascii_plus.py convert legacy_art.txt --out ascii_plus_art.txt
```

### 4. `draw`
Generates procedurally synthesized mathematical block art using the ASCII+ coordinate engine.
```bash
python3 ascii_plus.py draw
```

### 5. `play`
Enters the interactive ASCII+ live REPL playground.
```bash
python3 ascii_plus.py play
```
*   Type any text to see it rendered instantly.
*   Use `/style <color_or_gradient>` (e.g. `/style green` or `/style gradient`) to switch color templates dynamically.
*   Type `/exit` to return to your normal terminal shell.

---

## 💎 The ASCII+ Specification Reference

| Parameter / Feature | Standard ASCII (7-bit) | ASCII+ (Next-Gen) |
|---|---|---|
| **Character Set** | Basic ANSI alphanumeric, symbols (0-127) | Extended high-fidelity quadrant block glyphs (`█`, `▟`, `▛`, `▜`, `▙`) |
| **Color Support** | None / Monochrome (terminal default) | 24-bit Truecolor (RGB) linear interpolation gradients |
| **Anti-Aliasing** | None | Smooth boundary curves using sub-character blocks |
| **Interface** | Static raw text stream | Live Interactive REPL Sandbox, upgrade converters, & generators |

---

## 📄 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
