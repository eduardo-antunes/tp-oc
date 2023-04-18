#!/usr/bin/env python3

# Funções de montagem: as funções abaixo realizam a montagem de cada
# instrução, utilizando os valores dados como argumentos

def assemble_sub(rd, rs1, rs2):
    print("sub", rd, rs1, rs2)

def assemble_or(rd, rs1, rs2):
    print("or", rd, rs1, rs2)

def assemble_andi(rd, rs1, imm):
    print("andi", rd, rs1, imm)

# Funções de processamento de texto: os argumentos no arquivo fonte são
# dados em forma textual e vêm em diferentes formatos. Para cada formato,
# temos uma função para converter os argumentos em seus valores numéricos

# RRR: reg, reg, reg
def get_registers(args):
    reg_numbers = []
    registers = args.split(',')
    for reg in registers:
        reg_numbers.append(int(reg[1:]))
    return reg_numbers

# RRI: reg, reg, imediato
def get_rri(args):
    rri = args.split(',')
    rd = int(rri[0][1:])
    rs1 = int(rri[1][1:])
    imm = int(rri[2])
    return (rd, rs1, imm)

# Função principal:

def main(argv):
    # Tratamento de argumentos
    from sys import exit
    if len(argv) != 2:
        print(f"Uso: {argv[0]} <entrada.asm>")
        exit(1)

    # Recebemos um arquivo de entrada
    with open(argv[1]) as source_file:
        for line in source_file:
            parts = line.strip().split(" ")
            # Linhas vem no formato "<instrução> <outros>"
            instruction = parts[0]
            others = ''.join(list(filter(None, parts[1:])))

            if instruction == "lh":
                # lh: Load Half-word, passa 16 bits da RAM para um registrador
                pass

            elif instruction == "sh":
                # sh: Store Half-word, passa 16 bits de um registrador para RAM
                pass

            elif instruction == "sub":
                # sub: Subtract, subtrai rs2 de rs1 e coloca o resultado em rd
                data = get_registers(others)
                assemble_sub(*data)

            elif instruction == "or":
                # or: Or, faz um or bit a bit entre rs1 e rs2 e coloca o resultado em rd
                data = get_registers(others)
                assemble_or(*data)

            elif instruction == "andi":
                # andi: And Immediate, faz um and bit a bit entre rs1 e um valor
                # imediato e coloca o resultado em rd
                data = get_rri(others)
                assemble_andi(*data)

            elif instruction == "srl":
                # srl: Shift Right (Logic), desloca os bits de rs1 uma certa quantidade
                # de casas para a direita (deslocamento lógico)
                pass

            elif instruction == "beq":
                # beq: Branch if EQual, pula para o endereço dado se rs1 e rs2 forem iguais
                pass

            else:
                # Instrução inválida
                print("Instrução inválida na linha tal")

if __name__ == "__main__":
    from sys import argv
    main(argv)
