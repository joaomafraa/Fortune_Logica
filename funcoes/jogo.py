from funcoes.constantes import OPERADORES_BINARIOS, PROPOSICOES
from funcoes.entrada import ler_inteiro, ler_operador, ler_sim_nao
from funcoes.interface import (
    exibir_cabecalho,
    exibir_chance,
    exibir_proposicoes,
    exibir_resultado,
)
from funcoes.logica import (
    avaliar_expressao_com_proposicoes,
    calcular_chance_verdadeira,
    calcular_multiplicador,
    calcular_rodada,
    sortear_proposicoes,
)
from funcoes.saldo import carregar_saldo, salvar_saldo


def montar_expressao(nomes):
    partes_expressao = []
    termos = []
    operadores = []

    print()
    print("Agora monte sua expressao antes do sorteio:")

    for indice, nome in enumerate(nomes):
        negar = ler_sim_nao(f"Deseja usar NAO antes de {nome}? (S/N): ")
        texto = nome

        if negar:
            texto = f"NAO {nome}"

        partes_expressao.append(texto)
        termos.append((nome, negar))

        if indice < len(nomes) - 1:
            operador = ler_operador()
            operadores.append(operador)
            partes_expressao.append(OPERADORES_BINARIOS[operador])

    expressao = " ".join(partes_expressao)

    return expressao, termos, operadores


def escolher_expressao(nomes):
    while True:
        expressao, termos, operadores = montar_expressao(nomes)
        verdadeiros, total = calcular_chance_verdadeira(nomes, termos, operadores)
        multiplicador = calcular_multiplicador(verdadeiros, total)
        print()
        print(f"Expressao montada: {expressao}")
        exibir_chance(verdadeiros, total, multiplicador)

        if ler_sim_nao("Deseja apostar nessa probabilidade e multiplicador? (S/N): "):
            return expressao, termos, operadores, verdadeiros, total, multiplicador

        print()
        print("Tudo bem. Monte outra expressao.")


def jogar_rodada(saldo):
    print(f"Saldo atual: {saldo} moedas")

    quantidade = ler_inteiro("Quantidade de proposicoes (1 a 6): ", 1, 6)
    aposta = ler_inteiro(f"Valor da aposta (1 a {saldo}): ", 1, saldo)
    nomes = PROPOSICOES[:quantidade]

    print()
    print("Proposicoes disponiveis: " + ", ".join(nomes))
    expressao, termos, operadores, verdadeiros, total, multiplicador = escolher_expressao(nomes)

    proposicoes = sortear_proposicoes(quantidade)
    exibir_proposicoes(proposicoes)

    resultado = avaliar_expressao_com_proposicoes(termos, operadores, proposicoes)
    novo_saldo, variacao, multiplicador, jackpot = calcular_rodada(
        saldo,
        aposta,
        resultado,
        multiplicador,
        quantidade,
        proposicoes,
    )
    exibir_resultado(expressao, resultado, novo_saldo, variacao, multiplicador, jackpot)

    return novo_saldo


def main():
    saldo = carregar_saldo()
    exibir_cabecalho()

    while saldo > 0:
        saldo = jogar_rodada(saldo)
        salvar_saldo(saldo)

        if saldo <= 0:
            print()
            print("Fim de jogo! Seu saldo chegou a 0 moedas.")
            break

        if not ler_sim_nao("Deseja jogar outra rodada? (S/N): "):
            print()
            print(f"Obrigado por jogar Fortune Logica! Saldo final: {saldo} moedas.")
            salvar_saldo(saldo)
            break
