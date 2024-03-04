from __future__ import annotations

import sys

from isa import convert_from_binary


def main(code_path: str, token_path: str | None) -> None:
    code = convert_from_binary(open(code_path, 'rb'))
    print([opcode.__str__() for opcode in code])


if __name__ == "__main__":
    assert 2 <= len(sys.argv) <= 3, "Wrong arguments: machine.py <code_file> [<input_file>]"
    if len(sys.argv) == 3:
        _, code_file, input_file = sys.argv
    else:
        _, code_file = sys.argv
        input_file = None
    main(code_file, input_file)
