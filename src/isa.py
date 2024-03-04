from __future__ import annotations

from enum import Enum


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
