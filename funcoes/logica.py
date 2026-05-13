import random

from funcoes.constantes import OPERADORES_BINARIOS, PROPOSICOES


def sortear_proposicoes(quantidade):
    proposicoes = {}

    for nome in PROPOSICOES[:quantidade]:
        proposicoes[nome] = random.choice([True, False])

    return proposicoes


def criar_expressao_aleatoria(nomes):
    termos = []
    operadores = []
    partes_expressao = []
    operadores_disponiveis = list(OPERADORES_BINARIOS.keys())

    for indice, nome in enumerate(nomes):
        negado = random.choice([True, False])
        texto = nome

        if negado:
            texto = f"NAO {nome}"

        termos.append((nome, negado))
        partes_expressao.append(texto)

        if indice < len(nomes) - 1:
            operador = random.choice(operadores_disponiveis)
            operadores.append(operador)
            partes_expressao.append(OPERADORES_BINARIOS[operador])

    expressao = " ".join(partes_expressao)

    return expressao, termos, operadores


def criar_opcoes_aleatorias(nomes, quantidade_opcoes):
    opcoes = []
    expressoes_usadas = []
    tentativas = 0

    while len(opcoes) < quantidade_opcoes and tentativas < 100:
        expressao, termos, operadores = criar_expressao_aleatoria(nomes)
        tentativas += 1

        if expressao in expressoes_usadas:
            continue

        verdadeiros, total = calcular_chance_verdadeira(nomes, termos, operadores)
        multiplicador = calcular_multiplicador(verdadeiros, total)

        opcoes.append(
            {
                "expressao": expressao,
                "termos": termos,
                "operadores": operadores,
                "verdadeiros": verdadeiros,
                "total": total,
                "multiplicador": multiplicador,
            }
        )
        expressoes_usadas.append(expressao)

    return opcoes


def aplicar_nao(valor):
    return not valor


def aplicar_operador(operador, esquerda, direita):
    if operador == "E":
        return esquerda and direita

    if operador == "OU":
        return esquerda or direita

    if operador == "SE":
        return (not esquerda) or direita

    if operador == "SSE":
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


def calcular_rodada(saldo, aposta, resultado, multiplicador, quantidade_proposicoes):
    jackpot = resultado and multiplicador > 1

    if resultado:
        multiplicador_final = multiplicador

        if jackpot:
            multiplicador_jackpot = calcular_multiplicador_jackpot(quantidade_proposicoes)
            multiplicador_final = multiplicador * multiplicador_jackpot

        ganho = round(aposta * (multiplicador_final - 1))
        return saldo + ganho, ganho, multiplicador_final, jackpot

    return saldo - aposta, -aposta, multiplicador, jackpot
