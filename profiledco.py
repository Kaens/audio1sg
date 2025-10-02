#!/usr/bin/env python3
import re
import sys
from pathlib import Path

FUNC_RE = re.compile(
    r'''^
        (?P<indent>[ \t]*)           # leading spaces/tabs
        function[ \t]+
        (?P<name>is[A-Za-z0-9_]+)    # function name starting with 'is'
        [ \t]*\(
            [^)]*                    # optional params
        \)[ \t]*\{                   # opening brace on same line
    ''',
    re.VERBOSE
)

def inject_checkpoints(input_path, output_path, min_ms=100):
    with open(input_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    profiled_lines = []
    first_inserted = False

    for i, line in enumerate(lines):
        stripped = line.lstrip()
        # Skip obvious commented lines
        if stripped.startswith('//'):
            profiled_lines.append(line)
            continue

        m = FUNC_RE.match(line)
        if m:
            indent = m.group('indent')
            func_name = m.group('name')

            if not first_inserted:
                # Insert timer init before the first matched function
                init_line = (
                    f"{indent}var timer = new CheckpointTimer(); "
                    f"timer.init({int(min_ms)});\n"
                )
                profiled_lines.append(init_line)
                first_inserted = True
            else:
                # For subsequent functions, insert a named checkpoint
                checkpoint_line = f'{indent}timer.next("{func_name}");\n'
                profiled_lines.append(checkpoint_line)

            # Always append the original function line
            profiled_lines.append(line)
        else:
            profiled_lines.append(line)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.writelines(profiled_lines)


def main():
    if len(sys.argv) < 3 or len(sys.argv) > 4:
        print("Usage: profileco.py <input.js> <output.js> [min_ms]")
        sys.exit(1)

    input_path = Path(sys.argv[1])
    output_path = Path(sys.argv[2])
    min_ms = int(sys.argv[3]) if len(sys.argv) == 4 else 100

    inject_checkpoints(input_path, output_path, min_ms)

if __name__ == '__main__':
    main()
