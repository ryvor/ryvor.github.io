#!/usr/bin/env python3

import sys
import os
import glob

try:
    import readline
    HAS_READLINE = True
except ImportError:
    HAS_READLINE = False

try:
    import tty
    import termios
    import select as _select
    HAS_TTY = True
except ImportError:
    HAS_TTY = False

try:
    from PIL import Image
except ImportError:
    print("Pillow is required. Install it with: pip install Pillow")
    sys.exit(1)

# (width, height, filename suffix)
SIZES = [
    (2560, 1440, ""),
    (1920, 1080, "@1x"),
    (960,  540,  "@0.5x"),
    (480,  270,  "@0.25x"),
]

FORMATS = [
    ("original", "Keep original format"),
    ("jpeg",     "Convert to JPEG"),
]

BOLD  = "\033[1m"
DIM   = "\033[2m"
RESET = "\033[0m"

# ---------------------------------------------------------------------------
# Path completion
# ---------------------------------------------------------------------------

def _make_path_completer(dirs_only=False):
    def completer(text, state):
        expanded = os.path.expanduser(text)
        matches = []
        for m in sorted(glob.glob(expanded + "*")):
            if os.path.isdir(m):
                matches.append(m + os.sep)
            elif not dirs_only:
                matches.append(m)
        if text.startswith("~") and not expanded.startswith("~"):
            home = os.path.expanduser("~")
            matches = [
                "~" + m[len(home):] if m.startswith(home) else m
                for m in matches
            ]
        return matches[state] if state < len(matches) else None
    return completer

def _setup_readline(completer):
    if not HAS_READLINE:
        return
    readline.set_completer(completer)
    readline.set_completer_delims(" \t\n")
    readline.parse_and_bind("tab: complete")

def _teardown_readline():
    if not HAS_READLINE:
        return
    readline.set_completer(None)
    readline.set_completer_delims(" \t\n\"\\'`@$><=;|&{(")

# ---------------------------------------------------------------------------
# Raw key reading
# ---------------------------------------------------------------------------

def read_key():
    """Read one keypress in raw mode; returns a string token."""
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        b = os.read(fd, 1)
        if b == b'\x1b':
            ready, _, _ = _select.select([fd], [], [], 0.15)
            if ready:
                seq = os.read(fd, 2)
                if seq == b'[A': return 'up'
                if seq == b'[B': return 'down'
                if seq == b'[C': return 'right'
                if seq == b'[D': return 'left'
            return 'esc'
        return b.decode('utf-8', errors='replace')
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)

# ---------------------------------------------------------------------------
# Menu
# ---------------------------------------------------------------------------

def _clear(lines):
    sys.stdout.write(f"\033[{lines}A\033[J")
    sys.stdout.flush()

def _render(title, hint, items, cursor, selected, multi, error=False):
    """Print the menu. Lines printed = len(items) + 4."""
    err = f"  {DIM}select at least one{RESET}" if error else ""
    print(title)
    print(f"{DIM}{hint}{RESET}{err}")
    print()
    for i, label in enumerate(items):
        is_cur = (i == cursor)
        if multi:
            box = f"[{'x' if i in selected else ' '}]"
        else:
            box = f"({'●' if i == selected else ' '})"
        marker = "▶" if is_cur else " "
        line = f"  {marker} {box} {i + 1}. {label}"
        print(f"{BOLD}{line}{RESET}" if is_cur else line)
    print()


def run_menu(title, items, multi=True):
    """
    Interactive menu with arrow-key navigation.
    multi=True  → checkbox (space toggles, returns sorted list of indices)
    multi=False → radio    (space/arrows move selection, returns single index)
    Falls back to line-based input when stdin is not a tty.
    """
    n = len(items)
    cursor = 0
    selected = set(range(n)) if multi else 0

    if multi:
        hint = "↑↓ navigate   Space=toggle   a=all   1-9 jump   Enter=confirm"
    else:
        hint = "↑↓ navigate   Space=select   1-9 jump   Enter=confirm"

    total = n + 4  # title + hint + blank + n items + blank

    if not HAS_TTY or not sys.stdin.isatty():
        return _fallback(title, hint, items, multi, selected)

    _render(title, hint, items, cursor, selected, multi)
    error = False

    while True:
        key = read_key()
        error = False

        if key == '\x03':                           # Ctrl-C
            print()
            sys.exit(0)

        elif key == 'up':
            cursor = (cursor - 1) % n

        elif key == 'down':
            cursor = (cursor + 1) % n

        elif key == ' ':
            if multi:
                selected.discard(cursor) if cursor in selected else selected.add(cursor)
            else:
                selected = cursor

        elif key in '123456789':
            idx = int(key) - 1
            if 0 <= idx < n:
                cursor = idx                        # jump; space still needed to toggle/select

        elif key == 'a' and multi:
            if len(selected) == n:
                selected.clear()
            else:
                selected.update(range(n))

        elif key in ('\r', '\n'):
            if multi and not selected:
                error = True
            else:
                break

        _clear(total)
        _render(title, hint, items, cursor, selected, multi, error=error)

    return sorted(selected) if multi else selected


def _fallback(title, hint, items, multi, initial):
    """Line-based fallback for piped / non-tty input."""
    n = len(items)
    selected = set(initial) if multi else initial

    def show():
        for i, label in enumerate(items):
            if multi:
                box = f"[{'x' if i in selected else ' '}]"
            else:
                box = f"({'●' if i == selected else ' '})"
            print(f"  {box} {i + 1}. {label}")
        print()

    print(f"{title}\n{hint}\n")
    show()

    while True:
        try:
            sys.stdout.write("Choice: ")
            sys.stdout.flush()
            raw = input().strip().lower()
        except EOFError:
            break

        if not raw:
            if multi and not selected:
                print("  (select at least one)")
                continue
            break

        if raw == 'a' and multi:
            if len(selected) == n:
                selected = set()
            else:
                selected = set(range(n))
        else:
            try:
                idx = int(raw) - 1
                if 0 <= idx < n:
                    if multi:
                        selected.discard(idx) if idx in selected else selected.add(idx)
                    else:
                        selected = idx
            except ValueError:
                pass

        show()

    return sorted(selected) if multi else selected

# ---------------------------------------------------------------------------
# Prompts
# ---------------------------------------------------------------------------

def prompt_path(label, default=None, dirs_only=False):
    suffix = f" [{default}]" if default else ""
    hint = " (Tab to complete)" if HAS_READLINE else ""
    _setup_readline(_make_path_completer(dirs_only=dirs_only))
    try:
        value = input(f"{label}{hint}{suffix}: ").strip()
    finally:
        _teardown_readline()
    value = os.path.expanduser(value or (default or ""))
    return value or None


def prompt_quality():
    while True:
        raw = input("JPEG quality [1-95, default 85]: ").strip()
        if not raw:
            return 85
        try:
            q = int(raw)
            if 1 <= q <= 95:
                return q
            print("  (enter a value between 1 and 95)")
        except ValueError:
            print("  (enter a number between 1 and 95)")

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    print("\n  Image Resizer\n" + "-" * 30)

    if len(sys.argv) >= 2:
        image_path = os.path.expanduser(sys.argv[1])
    else:
        image_path = prompt_path("Image path")

    if not image_path or not os.path.isfile(image_path):
        print(f"Error: file not found: {image_path}")
        sys.exit(1)

    if len(sys.argv) >= 3:
        output_dir = os.path.expanduser(sys.argv[2])
    else:
        default_out = os.path.dirname(os.path.abspath(image_path))
        output_dir = prompt_path("Output folder", default=default_out, dirs_only=True)

    if not output_dir:
        print("Error: no output folder specified.")
        sys.exit(1)

    os.makedirs(output_dir, exist_ok=True)
    print()

    format_idx = run_menu(
        "Output format",
        [label for _, label in FORMATS],
        multi=False,
    )
    chosen_format = FORMATS[format_idx][0]

    quality = None
    if chosen_format == "jpeg":
        quality = prompt_quality()

    print()

    size_items = []
    for w, h, suffix in SIZES:
        display = suffix if suffix else " (base)"
        size_items.append(f"{w}x{h:<12} → " + "{base}" + display)

    chosen_sizes = run_menu("Select sizes to export", size_items)

    base, src_ext = os.path.splitext(os.path.basename(image_path))
    out_ext = ".jpg" if chosen_format == "jpeg" else (src_ext or ".png")

    print(f"\nResizing {os.path.basename(image_path)}...\n")

    with Image.open(image_path) as img:
        for idx in chosen_sizes:
            w, h, suffix = SIZES[idx]
            resized = img.resize((w, h), Image.LANCZOS)

            if out_ext.lower() in (".jpg", ".jpeg") and resized.mode in ("RGBA", "P", "LA"):
                resized = resized.convert("RGB")

            out_name = f"{base}{suffix}{out_ext}"
            out_path = os.path.join(output_dir, out_name)

            save_kwargs = {}
            if out_ext.lower() in (".jpg", ".jpeg"):
                save_kwargs["quality"] = quality
                save_kwargs["optimize"] = True
            elif out_ext.lower() == ".webp" and quality is not None:
                save_kwargs["quality"] = quality

            resized.save(out_path, **save_kwargs)
            size_kb = os.path.getsize(out_path) / 1024
            print(f"  Saved  {w}x{h}  →  {out_name}  ({size_kb:.1f} KB)")

    print(f"\nDone. {len(chosen_sizes)} file(s) saved to {output_dir}\n")


if __name__ == "__main__":
    main()
