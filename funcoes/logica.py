import random

from funcoes.constantes import OPERADORES_BINARIOS, PROPOSICOES


def sortear_proposicoes(quantidade):
    proposicoes = {}

    for nome in PROPOSICOES[:quantidade]:
        proposicoes[nome] = random.choice([True, False])

    return proposicoes


def aplicar_nao(valor):
    return not valor


def aplicar_operador(operador, esquerda, direita):
    if operador in ("E", "∧"):
        return esquerda and direita

    if operador in ("OU", "∨"):
        return esquerda or direita

    if operador in ("SE", "->", "→"):
        return (not esquerda) or direita

    if operador in ("SSE", "<->", "↔"):
        return esquerda == direita

    raise ValueError(f"Operador invalido: {operador}")


def avaliar_expressao(valores, operadores):
    if not valores:
        raise ValueError("A expressao precisa ter pelo menos um valor.")

    if len(operadores) != len(valores) - 1:
        raise ValueError("Quantidade de operadores incompativel com os valores.")

    resultado = valores[0]

    for indice, operador in enumerate(operadores):
        resultado = aplicar_operador(operador, resultado, valores[indice + 1])

    return resultado


def avaliar_expressao_com_proposicoes(termos, operadores, proposicoes):
    valores = []

    for nome, negado in termos:
        valor = proposicoes[nome]

        if negado:
            valor = aplicar_nao(valor)

        valores.append(valor)

    return avaliar_expressao(valores, operadores)


def calcular_chance_verdadeira(nomes, termos, operadores):
    total = 0
    verdadeiros = 0
    quantidade_combinacoes = 2 ** len(nomes)

    for numero in range(quantidade_combinacoes):
        proposicoes = {}

        for indice, nome in enumerate(nomes):
            proposicoes[nome] = (numero // (2 ** indice)) % 2 == 1

        resultado = avaliar_expressao_com_proposicoes(termos, operadores, proposicoes)

        total += 1
        if resultado:
            verdadeiros += 1

    return verdadeiros, total


def calcular_multiplicador(verdadeiros, total):
    if verdadeiros == 0:
        return 0

    return total / verdadeiros


def calcular_multiplicador_jackpot(quantidade_proposicoes):
    if quantidade_proposicoes <= 0:
        return 1

    return quantidade_proposicoes


def todas_proposicoes_verdadeiras(proposicoes):
    return all(proposicoes.values())


def calcular_rodada(saldo, aposta, resultado, multiplicador, quantidade_proposicoes, proposicoes):
    jackpot = resultado and todas_proposicoes_verdadeiras(proposicoes)

    if resultado:
        multiplicador_final = multiplicador

        if jackpot:
            multiplicador_jackpot = calcular_multiplicador_jackpot(quantidade_proposicoes)
            multiplicador_final = multiplicador * multiplicador_jackpot

        ganho = round(aposta * (multiplicador_final - 1))
        return saldo + ganho, ganho, multiplicador_final, jackpot

    return saldo - aposta, -aposta, multiplicador, jackpot
