#!/usr/bin/env python3

def rshift(val, n):
    return val >> n if val >= 0 else -val >> n

# Funções de montagem: as funções abaixo realizam a montagem de cada
# instrução, utilizando os valores dados como argumentos

def assemble_rtype(opcode, funct3, funct7, rd, rs1, rs2):
    # Formato R (registradores)
    print(f"R: {funct7:07b} {rs2:05b} {rs1:05b} {funct3:03b} {rd:05b} {opcode:07b}")

def assemble_itype(opcode, funct3, rd, rs1, number):
    # Formato I (imediato)
    print(f"I: {number:012b} {rs1:05b} {funct3:03b} {rd:05b} {opcode:07b}")

def assemble_stype(opcode, funct3, rs1, rs2, number):
    # Formato S (store)
    front = number & 0b11111
    back = rshift(number, 5)
    print(f"S: {back:07b} {rs2:05b} {rs1:05b} {funct3:03b} {front:05b} {opcode:07b}")

def assemble_sbtype(opcode, funct3, rs1, rs2, number):
    # Formato SB (desvios condicionais)
    front = (number & 0b0100000011110) >> 1
    back = rshift(number, 5) & 0b10111111
    print(f"SB: {back:07b} {rs2:05b} {rs1:05b} {funct3:03b} {front:05b} {opcode:07b}")


# Funções de processamento de texto: os argumentos no arquivo fonte são
# dados em forma textual e vêm em diferentes formatos. Para cada formato,
# temos uma função para converter os argumentos em seus valores numéricos

# RRR: reg, reg, reg
def get_registers(args):
    registers = args.split(',')
    rd = int(registers[0][1:])
    rs1 = int(registers[1][1:])
    rs2 = int(registers[2][1:])
    return rd, rs1, rs2

# RRI: reg, reg, imediato
def get_rri(args):
    rri = args.split(',')
    rd = int(rri[0][1:])
    rs1 = int(rri[1][1:])
    imm = int(rri[2])
    return rd, rs1, imm

# RRS: reg, imediato(reg)
def get_rrs(args):
    parts = args.split(',')
    rs1 = int(parts[0][1:])
    others = parts[1][:-1].split('(')
    imm = int(others[0])
    rs2 = int(others[1][1:])
    return rs1, rs2, imm

# Função principal:

def main(argv):
    # Tratamento de argumentos
    from sys import stdout, stderr, exit
    if len(argv) == 4 and argv[2] == '-o':
        out = open(argv[3], "w")
        oflag = True
    elif len(argv) == 2:
        out = stdout
        oflag = False
    else:
        print(f"uso: {argv[0]} <entrada.asm> [-o <saida.txt>]", file=stderr)
        exit(1)

    # Recebemos um arquivo de entrada
    from contextlib import redirect_stdout
    with open(argv[1]) as source_file:
        with redirect_stdout(out):
            for line in source_file:
                print(line, end="")
                parts = line.strip().split(" ")
                # Linhas vem no formato "<instrução> <outros>"
                instruction = parts[0]
                others = ''.join(list(filter(None, parts[1:])))

                if instruction == "lh":
                    # lh: Load Half-word, passa 16 bits da RAM para um registrador
                    funct3 = 0b001
                    opcode = 0b0000011
                    rd, rs1, number = get_rrs(others)
                    assemble_itype(opcode, funct3, rd, rs1, number)

                elif instruction == "sh":
                    # sh: Store Half-word, passa 16 bits de um registrador para RAM
                    funct3 = 0b001
                    opcode = 0b0100011
                    rs1, rs2, number = get_rrs(others)
                    assemble_stype(opcode, funct3, rs1, rs2, number)

                elif instruction == "sub":
                    # sub: Subtract, subtrai rs2 de rs1 e coloca o resultado em rd
                    funct3 = 0b000
                    funct7 = 0b0100000
                    opcode = 0b0110011
                    rd, rs1, rs2 = get_registers(others)
                    assemble_rtype(opcode, funct3, funct7, rd, rs1, rs2)

                elif instruction == "or":
                    # or: Or, faz um or bit a bit entre rs1 e rs2 e coloca o resultado em rd
                    funct3 = 0b110
                    funct7 = 0b0000000
                    opcode = 0b0110011
                    rd, rs1, rs2 = get_registers(others)
                    assemble_rtype(opcode, funct3, funct7, rd, rs1, rs2)

                elif instruction == "andi":
                    # andi: And Immediate, faz um and bit a bit entre rs1 e um valor
                    # imediato e coloca o resultado em rd
                    funct3 = 0b111
                    opcode = 0b0010011
                    rd, rs1, number = get_rri(others)
                    assemble_itype(opcode, funct3, rd, rs1, number)

                elif instruction == "srl":
                    # srl: Shift Right (Logic), desloca os bits de rs1 uma certa quantidade
                    # de casas para a direita (deslocamento lógico)
                    funct3 = 0b101
                    funct7 = 0b0000000
                    opcode = 0b0110011
                    rd, rs1, rs2 = get_registers(others)
                    assemble_rtype(opcode, funct3, funct7, rd, rs1, rs2)

                elif instruction == "beq":
                    # beq: Branch if EQual, pula para o endereço dado se rs1 e rs2 forem iguais
                    funct3 = 0b000
                    opcode = 0b1100111
                    rs1, rs2, addr = get_rri(others)
                    assemble_sbtype(opcode, funct3, rs1, rs2, addr)

                else:
                    # Instrução inválida
                    print("Instrução inválida na linha tal")
    if oflag: out.close()

if __name__ == "__main__":
    from sys import argv
    main(argv)
