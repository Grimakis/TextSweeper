#!/usr/bin/env python3
"""
Hex to BASIC DATA Converter
Converts assembled hex machine code to BASIC DATA statements

Usage:
    python hex_to_data.py "21 c0 fc 01 40 01 7E CD 44 4b 23 0B 78 B1 C2 05 F7 C9"
    python hex_to_data.py < hexfile.txt

Input format: Space-separated hex bytes (case insensitive)
Output: BASIC DATA statement ready to paste

Example:
    $ python hex_to_data.py "21 C0 FC"
    DATA 33,192,252
    Bytes: 3
"""

import sys
import re


def hex_to_data(hex_string):
    """Convert hex string to BASIC DATA statement."""
    # Remove all non-hex characters except spaces
    hex_string = re.sub(r'[^0-9a-fA-F\s]', '', hex_string)

    # Split into hex bytes
    hex_bytes = hex_string.split()

    if not hex_bytes:
        return None

    # Convert to decimal
    dec_values = [str(int(hx, 16)) for hx in hex_bytes]

    data_statement = f"DATA {','.join(dec_values)}"

    return {
        'data_statement': data_statement,
        'byte_count': len(dec_values)
    }


def main():
    if len(sys.argv) > 1:
        # Input from command line argument
        hex_input = ' '.join(sys.argv[1:])
    else:
        # Input from stdin
        hex_input = sys.stdin.read()

    result = hex_to_data(hex_input)

    if result:
        print(result['data_statement'])
        print(f"Bytes: {result['byte_count']}", file=sys.stderr)
    else:
        print("Error: No valid hex input found", file=sys.stderr)
        return 1

    return 0


if __name__ == '__main__':
    sys.exit(main())
