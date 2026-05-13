from funcoes.constantes import OPERADORES_BINARIOS


def ler_inteiro(mensagem, minimo=None, maximo=None):
    while True:
        entrada = input(mensagem).strip()

        try:
            numero = int(entrada)
        except ValueError:
            print("Digite um numero inteiro valido.")
            continue

        if minimo is not None and numero < minimo:
            print(f"O valor minimo permitido e {minimo}.")
            continue

        if maximo is not None and numero > maximo:
            print(f"O valor maximo permitido e {maximo}.")
            continue

        return numero


def ler_sim_nao(mensagem):
    while True:
        entrada = input(mensagem).strip().upper()

        if entrada in ("S", "SIM"):
            return True
        if entrada in ("N", "NAO"):
            return False

        print("Digite S para sim ou N para nao.")


def ler_operador():
    opcoes = ", ".join(OPERADORES_BINARIOS.keys())

    while True:
        operador = input(f"Escolha o operador ({opcoes}): ").strip().upper()

        if operador in OPERADORES_BINARIOS:
            return operador

        print("Operador invalido. Use E, OU, SE ou SSE.")
