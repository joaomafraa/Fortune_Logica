def valor_para_texto(valor):
    return "V" if valor else "F"


def formatar_multiplicador(multiplicador):
    if multiplicador == int(multiplicador):
        return f"x{int(multiplicador)}"

    return f"x{multiplicador:.2f}"


def exibir_cabecalho():
    print()
    print("=" * 44)
    print("        FORTUNE LOGICA - JACKPOT")
    print("=" * 44)
    print("Monte expressoes logicas e teste sua sorte!")
    print()


def exibir_proposicoes(proposicoes):
    print()
    print("Proposicoes sorteadas:")

    for nome, valor in proposicoes.items():
        print(f"  {nome} = {valor_para_texto(valor)}")


def exibir_chance(verdadeiros, total, multiplicador):
    chance = (verdadeiros / total) * 100

    print()
    print(f"Chance da expressao dar verdadeiro: {verdadeiros}/{total} ({chance:.2f}%)")
    print(f"Multiplicador definido: {formatar_multiplicador(multiplicador)}")


def exibir_resultado(expressao, resultado, saldo, variacao, multiplicador, jackpot):
    print()
    print("-" * 44)
    print(f"Expressao: {expressao}")
    print(f"Resultado: {valor_para_texto(resultado)}")

    if resultado:
        if jackpot:
            print("JACKPOT! O multiplicador aumentou pela dificuldade de cair!")
        print(f"Multiplicador: {formatar_multiplicador(multiplicador)}")
        print(f"Lucro: {variacao} moedas.")
    else:
        print(f"Voce perdeu {-variacao} moedas.")

    print(f"Saldo atualizado: {saldo} moedas")
    print("-" * 44)
