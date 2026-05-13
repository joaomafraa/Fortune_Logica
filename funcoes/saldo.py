from funcoes.constantes import ARQUIVO_SALDO, SALDO_INICIAL


def carregar_saldo(caminho=ARQUIVO_SALDO):
    try:
        with open(caminho, "r", encoding="utf-8") as arquivo:
            saldo = int(arquivo.read().strip())
    except FileNotFoundError:
        salvar_saldo(SALDO_INICIAL, caminho)
        return SALDO_INICIAL
    except ValueError:
        salvar_saldo(SALDO_INICIAL, caminho)
        return SALDO_INICIAL

    if saldo < 0:
        salvar_saldo(SALDO_INICIAL, caminho)
        return SALDO_INICIAL

    return saldo


def salvar_saldo(saldo, caminho=ARQUIVO_SALDO):
    with open(caminho, "w", encoding="utf-8") as arquivo:
        arquivo.write(str(saldo))
