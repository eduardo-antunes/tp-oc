#!/usr/bin/env python3

# Montador simples de assembly RISC-V

def main():
    # Processamento de argumentos de linha de comando
    from sys import stdout
    from contextlib import redirect_stdout
    from argparse import ArgumentParser
    pr = ArgumentParser(
        prog="ras",
        description="Montador simples de assembly RISC-V")
    pr.add_argument("arquivo", help="Arquivo de entrada, escrito em assembly RISC-V")
    pr.add_argument("-o", metavar="saida", help="Arquivo de saída, no qual é escrito o binário resultante")
    args = pr.parse_args()

    # Criação dos objetos de instrução
    lhInst = Instruction(0b0000011, 0b001, instFormat=Format.I)
    shInst = Instruction(0b0100011, 0b001, instFormat=Format.S)
    subInst = Instruction(0b0110011, 0b000, funct7=0b0100000)
    orInst = Instruction(0b0110011, 0b110,  funct7=0b0000000)
    andiInst = Instruction(0b0010011, 0b111, instFormat=Format.I)
    srlInst = Instruction(0b0110011, 0b101, funct7=0b0000000)
    beqInst = Instruction(0b1100111, 0b000, instFormat=Format.SB)

    # Leitura e processamento do arquivo de entrada
    output_file = open(args.o, "w") if args.o else stdout
    with redirect_stdout(output_file):
        with open(args.arquivo) as source_file:
            for i, line in enumerate(source_file):
                # Linhas vem no formato <operação> <dados>
                op, data = line.strip().split(" ", 1)
                data = data.replace(" ", "")
                # Processamento depende da operação em questão
                if op == "lh":
                    rd, rs1, i = parseParens(data)
                    print(lhInst.assemble(rd, rs1, i))
                elif op == "sh":
                    rs1, rs2, i = parseParens(data)
                    print(shInst.assemble(rs1, rs2, i))
                elif op == "sub":
                    rd, rs1, rs2 = parseRegisters(data)
                    print(subInst.assemble(rd, rs1, rs2))
                elif op == "or":
                    rd, rs1, rs2 = parseRegisters(data)
                    print(orInst.assemble(rd, rs1, rs2))
                elif op == "andi":
                    rd, rs1, i = parseImmediate(data)
                    print(andiInst.assemble(rd, rs1, i))
                elif op == "srl":
                    rd, rs1, rs2 = parseRegisters(data)
                    print(srlInst.assemble(rd, rs1, rs2))
                elif op == "beq":
                    rs1, rs2, addr = parseImmediate(data)
                    print(beqInst.assemble(rs1, rs2, addr))
                else:
                    # Instrução inválida
                    from sys import stderr
                    print(f"Instrução inválida na linha {i}: {line}", file=stderr)
    output_file.close()

# Funções para processamento de texto: essas funções recebem uma string que
# corresponde aos argumentos de cada instrução e produzem os valores inteiros
# que serão usados na montagem. Cada um está ligado a um formato em que os
# argumentos podem estar apresentados.

def parseRegisters(text):
    regs = text.split(",")
    rd = int(regs[0][1:])
    rs1 = int(regs[1][1:])
    rs2 = int(regs[2][1:])
    return rd, rs1, rs2

def parseImmediate(text):
    args = text.split(",")
    reg1 = int(args[0][1:])
    reg2 = int(args[1][1:])
    i = int(args[2])
    return reg1, reg2, i

def parseParens(text):
    args = text.split(",")
    reg1 = int(args[0][1:])
    args = args[1][:-1].split("(") # )
    reg2 = int(args[1][1:])
    i = int(args[0])
    return reg1, reg2, i

def rls(x, n):
    return x >> n if x >= 0 else (-x) >> n

from enum import Enum
from dataclasses import dataclass

# Formatos de instrução de fato
class Format(Enum):
    R = 0   # <operação> reg, reg, reg
    I = 1   # <operação> reg, reg, i
    S = 2   # <store>    reg, i(reg)
    SB = 3  # <operação> reg, reg, addr

# Instruções
@dataclass
class Instruction:
    opcode: int
    funct3: int
    funct7: int|None = None
    instFormat: Format = Format.R

    # Montagem baseada no formato
    def assemble(self, *data) -> str:
        match self.instFormat:
            case Format.R:
                rd, rs1, rs2 = data
                return f"{self.funct7:07b}{rs2:05b}{rs1:05b}{self.funct3:03b}{rd:05b}{self.opcode:07b}"
            case Format.I:
                rd, rs1, i = data
                return f"{i:012b}{rs1:05b}{self.funct3:03b}{rd:05b}{self.opcode:07b}"
            case Format.S:
                rs1, rs2, i = data
                part1 = rls(i, 5)
                part2 = i & 0b11111
                return f"{part1:07b}{rs2:05b}{rs1:05b}{self.funct3:03b}{part2:05b}{self.opcode:07b}"
            case Format.SB:
                rs1, rs2, i = data
                part1 = rls(i, 5) & 0b10111111
                part2 = i & 0b11110 | rls(i & (1 << 11), 11)
                return f"{part1:07b}{rs2:05b}{rs1:05b}{self.funct3:03b}{part2:05b}{self.opcode:07b}"

if __name__ == "__main__":
    main()
