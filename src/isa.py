from __future__ import annotations

import struct
from enum import Enum
from typing import IO


class OpcodeParamType(str, Enum):
    CONST = "const"
    ADDR = "addr"
    UNDEFINED = "undefined"
    ADDR_REL = "addr_rel"

    def __str__(self):
        return str(self.value)


class OpcodeParam:
    def __init__(self, param_type: OpcodeParamType, value: any):
        self.param_type = param_type
        self.value = value

    def __str__(self):
        return str(self.value)


class OpcodeType(str, Enum):
    DROP = "drop"  # 1
    MUL = "mul"
    DIV = "div"
    SUB = "sub"
    ADD = "add"
    MOD = "mod"
    SWAP = "swap"  # ?
    OVER = "over"
    DUP = "dup"  # 1
    EQ = "eq"
    GR = "gr"
    LS = "ls"
    DI = "di"  # 0
    EI = "ei"  # 0
    OMIT = "omit"  # 1
    READ = "read"  # 0 -> 1

    # not used in source code, compile-generated
    STORE = "store"
    LOAD = "load"
    PUSH = "push"
    RPOP = "rpop"  # move from return stack to data stack
    POP = "pop"  # move from data stack to return stack
    JMP = "jmp"
    ZJMP = "zjmp"
    CALL = "call"
    RET = "ret"
    HALT = "halt"

    def __str__(self):
        return str(self.value)


opcode_types = [opcode_type for opcode_type in OpcodeType]
opcode_types_with_one_param = [OpcodeType.PUSH, OpcodeType.JMP, OpcodeType.ZJMP, OpcodeType.CALL]


class Opcode:
    def __init__(self, opcode_type: OpcodeType, params: list[OpcodeParam]):
        assert len(params) <= 1, "Maximum available operation params is 1"
        self.opcode_type = opcode_type
        self.params = params

    def __str__(self):
        params_str = "" if len(self.params) == 0 else self.params[0].__str__()
        return self.opcode_type.value + " " + params_str


class TermType(Enum):
    (
        # Term --> Opcode
        DI,
        EI,
        DUP,
        ADD,
        SUB,
        MUL,
        DIV,
        MOD,
        OMIT,
        SWAP,
        DROP,
        OVER,
        EQ,
        LS,
        GR,
        READ,
        # Term !-> Opcode
        VARIABLE,
        ALLOT,
        STORE,
        LOAD,
        IF,
        ELSE,
        THEN,
        PRINT,
        DEF,
        RET,
        DEF_INTR,
        DO,
        LOOP,
        BEGIN,
        UNTIL,
        LOOP_CNT,
        CALL,
        STRING,
        ENTRYPOINT,
    ) = range(35)


def get_bin_args(opcode: Opcode) -> tuple[bytes, str]:
    if len(opcode.params) == 0:
        return struct.pack("xx"), format(0, "06x")

    arg = int(opcode.params[0].value)
    return struct.pack(">H", arg), format(arg, "04x")


def convert_to_binary(opcodes: list[Opcode]) -> tuple[list[bytes], list[str]]:
    bin_code: list[bytes] = []
    debug_code: list[str] = []

    for index, opcode in enumerate(opcodes):
        debug_line = ""

        operation = opcode.opcode_type

        idx = opcode_types.index(operation)
        bin_code.append(struct.pack("B", idx))
        debug_line += format(index, "05") + " - " + format(idx, "02x")

        args_bytes, args_format = get_bin_args(opcode)
        bin_code.append(args_bytes)
        debug_line += args_format
        debug_code.append(debug_line + " - " + opcode.__str__() + "\n")

    return bin_code, debug_code


def convert_from_binary(bin_code_file: IO):
    opcodes = []
    while len(bin_instruction := bin_code_file.read(3)) != 0:
        opcode_idx, arg = struct.unpack('>BH', bin_instruction)

        opcode_type = OpcodeType(opcode_types[opcode_idx])
        opcode_params = [OpcodeParam(OpcodeParamType.CONST, arg)] if opcode_type in opcode_types_with_one_param else []

        opcodes.append(Opcode(opcode_type, opcode_params))
    print(len(opcodes))
    return opcodes
