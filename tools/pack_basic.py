#!/usr/bin/env python3
"""
BASIC Code Packer for TRS-80 Model 100
Packs BASIC source code by removing comments, whitespace, and renumbering lines
Merges lines that aren't GOTO/GOSUB targets for maximum compression.

Similar to ROM2/Cleuseau but written in Python for modern systems.

Usage:
    python pack_basic.py input.DO output.DO
    python pack_basic.py src/TSWEEP.DO ascii_packed/TSWEEP.DO
"""

import sys
import re
from pathlib import Path


def remove_comment(line):
    """Remove comments from a BASIC line while preserving strings."""
    in_string = False
    result = []
    i = 0

    while i < len(line):
        char = line[i]

        # Track string state
        if char == '"':
            in_string = not in_string
            result.append(char)
            i += 1
            continue

        # Remove comment if not in string
        if char == "'" and not in_string:
            break

        result.append(char)
        i += 1

    return ''.join(result).rstrip()


def pack_spaces(line):
    """Remove unnecessary spaces while preserving strings and required keyword spacing."""
    in_string = False
    result = []
    i = 0

    while i < len(line):
        char = line[i]

        if char == '"':
            in_string = not in_string
            result.append(char)
            i += 1
            continue

        if in_string:
            result.append(char)
            i += 1
            continue

        # Outside strings - handle spaces carefully
        if char == ' ':
            # Look ahead to see what follows the space
            remaining = line[i+1:].lstrip(' ')
            if not remaining:
                i += 1
                continue

            # Check if next word is AND/OR (need space before)
            if remaining.upper().startswith('AND') or remaining.upper().startswith('OR'):
                # Keep ONE space before AND/OR
                if not result or result[-1] != ' ':
                    result.append(' ')
                i += 1
                continue

            # Otherwise skip the space
            i += 1
            continue

        result.append(char)
        i += 1

    return ''.join(result)


def parse_basic_file(filename):
    """Parse BASIC file and return list of (line_number, code) tuples."""
    lines = []

    with open(filename, 'r') as f:
        for line in f:
            line = line.rstrip('\n\r')

            if not line.strip():
                continue

            match = re.match(r'^(\d+)\s+(.*)', line)
            if match:
                line_num = int(match.group(1))
                code = match.group(2)

                # Skip comment-only lines
                code_stripped = code.strip()
                if code_stripped and not code_stripped.startswith("'"):
                    lines.append((line_num, code))

    return lines


def find_line_targets(lines):
    """Find all line numbers that are targets of GOTO/GOSUB/etc."""
    targets = set()

    for line_num, code in lines:
        # Remove comments and strings
        code_clean = remove_comment(code)

        # Find all line number references
        in_string = False
        i = 0

        while i < len(code_clean):
            if code_clean[i] == '"':
                in_string = not in_string
                i += 1
                continue

            if in_string:
                i += 1
                continue

            # Look for keywords
            remaining = code_clean[i:].upper()

            for keyword in ['GOTO', 'GOSUB', 'THEN', 'ELSE']:
                if remaining.startswith(keyword):
                    i += len(keyword)

                    # Extract line numbers (comma-separated for ON...GOTO)
                    while i < len(code_clean):
                        if code_clean[i].isdigit():
                            num_start = i
                            while i < len(code_clean) and code_clean[i].isdigit():
                                i += 1
                            targets.add(int(code_clean[num_start:i]))
                        elif code_clean[i] in (',', ' ', '\t'):
                            i += 1
                        else:
                            break
                    break
            else:
                i += 1

    return targets


def merge_lines(lines, targets, max_line_length=255):
    """Merge consecutive lines that aren't GOTO/GOSUB targets."""
    merged = []
    current_start_line = None
    current_code = []

    def flush_current(start_line):
        """Flush accumulated code, respecting max line length."""
        nonlocal current_start_line

        if not current_code:
            return

        combined = ':'.join(current_code)

        # Check if combined line exceeds max length
        # Account for line number + space (e.g., "123 ")
        max_code_length = max_line_length - len(str(start_line)) - 1

        if len(combined) <= max_code_length:
            # Fits in one line
            merged.append((start_line, combined))
        else:
            # Too long - need to split it
            # Add first segment with the target line number
            merged.append((start_line, current_code[0]))

            # Add remaining segments with None (will get renumbered)
            for seg in current_code[1:]:
                merged.append((None, seg))

    for line_num, code in lines:
        if line_num in targets:
            # This line is a target - must start a new merged line
            if current_start_line is not None:
                flush_current(current_start_line)

            current_start_line = line_num
            current_code = [code]
        else:
            # Not a target - can be merged if it fits
            if current_start_line is None:
                current_start_line = line_num

            # Check if adding this would exceed max length
            test_combined = ':'.join(current_code + [code])
            max_code_length = max_line_length - len(str(current_start_line)) - 1

            if len(test_combined) <= max_code_length:
                # Fits - add it
                current_code.append(code)
            else:
                # Doesn't fit - flush current and start new
                flush_current(current_start_line)
                current_start_line = line_num
                current_code = [code]

    # Flush final accumulated code
    if current_start_line is not None:
        flush_current(current_start_line)

    return merged


def update_line_references(code, line_map):
    """Update all line number references to new line numbers."""
    in_string = False
    result = []
    i = 0

    while i < len(code):
        char = code[i]

        if char == '"':
            in_string = not in_string
            result.append(char)
            i += 1
            continue

        if in_string:
            result.append(char)
            i += 1
            continue

        remaining = code[i:].upper()
        keyword_found = False

        for keyword in ['GOTO', 'GOSUB', 'THEN', 'ELSE']:
            if remaining.startswith(keyword):
                result.extend(code[i:i+len(keyword)])
                i += len(keyword)
                keyword_found = True

                while i < len(code):
                    if code[i].isdigit():
                        num_start = i
                        while i < len(code) and code[i].isdigit():
                            i += 1

                        old_line = int(code[num_start:i])
                        new_line = line_map.get(old_line, old_line)
                        result.append(str(new_line))
                    elif code[i] in (',', ' ', '\t'):
                        result.append(code[i])
                        i += 1
                    else:
                        break
                break

        if not keyword_found:
            result.append(char)
            i += 1

    return ''.join(result)


def pack_basic_file(input_file, output_file):
    """Pack BASIC file with full ROM2/Cleuseau-style compression."""
    # Parse input
    lines = parse_basic_file(input_file)
    print(f"Parsed {len(lines)} non-comment lines")

    # Pack each line (remove spaces/comments)
    packed = [(num, pack_spaces(remove_comment(code))) for num, code in lines]

    # Find GOTO/GOSUB targets
    targets = find_line_targets(packed)
    print(f"Found {len(targets)} line number targets")

    # Merge non-target lines
    merged = merge_lines(packed, targets)
    print(f"Merged into {len(merged)} lines")

    # Build line number mapping (handle None for split lines)
    line_map = {}
    new_line_num = 1

    for old_line_num, code in merged:
        if old_line_num is not None and old_line_num not in line_map:
            line_map[old_line_num] = new_line_num
        new_line_num += 1

    # Update line references and assign new numbers
    final_lines = []
    current_new_num = 1
    for old_line_num, code in merged:
        updated_code = update_line_references(code, line_map)

        if old_line_num is not None:
            new_line_num = line_map[old_line_num]
        else:
            new_line_num = current_new_num

        final_lines.append((new_line_num, updated_code))
        current_new_num = new_line_num + 1

    # Write output
    with open(output_file, 'w') as f:
        for line_num, code in final_lines:
            f.write(f"{line_num} {code}\n")

    print(f"\nLine number range: {lines[0][0]}-{lines[-1][0]} -> 1-{len(final_lines)}")

    # Calculate space savings
    old_line_num_chars = sum(len(str(old)) for old, _ in lines)
    new_line_num_chars = sum(len(str(new)) for new, _ in final_lines)
    print(f"Line number bytes saved: {old_line_num_chars} -> {new_line_num_chars} ({old_line_num_chars - new_line_num_chars} bytes)")

    print(f"\nPacked: {input_file} -> {output_file}")


def main():
    if len(sys.argv) != 3:
        print(__doc__)
        return 1

    input_file = Path(sys.argv[1])
    output_file = Path(sys.argv[2])

    if not input_file.exists():
        print(f"Error: Input file not found: {input_file}")
        return 1

    try:
        pack_basic_file(input_file, output_file)
        return 0
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
