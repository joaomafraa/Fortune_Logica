import unittest
import os
from tempfile import TemporaryDirectory

from funcoes.logica import (
    aplicar_nao,
    aplicar_operador,
    avaliar_expressao,
    avaliar_expressao_com_proposicoes,
    calcular_chance_verdadeira,
    calcular_multiplicador,
    calcular_multiplicador_jackpot,
    calcular_rodada,
    criar_expressao_aleatoria,
    criar_opcoes_aleatorias,
)
from funcoes.saldo import carregar_saldo, salvar_saldo


class TestFortuneLogica(unittest.TestCase):
    def test_aplicar_nao_inverte_valor_logico(self):
        self.assertIs(aplicar_nao(True), False)
        self.assertIs(aplicar_nao(False), True)

    def test_operador_e(self):
        self.assertIs(aplicar_operador("E", True, True), True)
        self.assertIs(aplicar_operador("E", True, False), False)

    def test_operador_ou(self):
        self.assertIs(aplicar_operador("OU", False, True), True)
        self.assertIs(aplicar_operador("OU", False, False), False)

    def test_operador_se_implicacao(self):
        self.assertIs(aplicar_operador("SE", True, False), False)
        self.assertIs(aplicar_operador("SE", True, True), True)
        self.assertIs(aplicar_operador("SE", False, False), True)

    def test_operador_sse_bicondicional(self):
        self.assertIs(aplicar_operador("SSE", True, True), True)
        self.assertIs(aplicar_operador("SSE", False, False), True)
        self.assertIs(aplicar_operador("SSE", True, False), False)

    def test_avaliar_expressao_da_esquerda_para_direita(self):
        valores = [True, False, False]
        operadores = ["OU", "E"]

        self.assertIs(avaliar_expressao(valores, operadores), False)

    def test_avaliar_expressao_com_proposicoes_depois_do_sorteio(self):
        termos = [("P", False), ("Q", True)]
        operadores = ["E"]
        proposicoes = {"P": True, "Q": False}

        self.assertIs(
            avaliar_expressao_com_proposicoes(termos, operadores, proposicoes),
            True,
        )

    def test_calcular_chance_verdadeira_por_tabela_verdade(self):
        nomes = ["P", "Q"]
        termos = [("P", False), ("Q", False)]
        operadores = ["E"]

        verdadeiros, total = calcular_chance_verdadeira(nomes, termos, operadores)

        self.assertEqual(verdadeiros, 1)
        self.assertEqual(total, 4)

    def test_calcular_multiplicador_paga_mais_para_menor_chance(self):
        self.assertEqual(calcular_multiplicador(1, 4), 4)
        self.assertEqual(calcular_multiplicador(2, 4), 2)
        self.assertAlmostEqual(calcular_multiplicador(3, 4), 1.3333333333333333)
        self.assertEqual(calcular_multiplicador(4, 4), 1)

    def test_criar_expressao_aleatoria_usa_todas_as_proposicoes(self):
        expressao, termos, operadores = criar_expressao_aleatoria(["P", "Q", "R"])

        self.assertTrue(expressao)
        self.assertEqual(len(termos), 3)
        self.assertEqual(len(operadores), 2)

    def test_criar_opcoes_aleatorias_mostra_multiplicador(self):
        opcoes = criar_opcoes_aleatorias(["P", "Q"], 2)

        self.assertGreaterEqual(len(opcoes), 1)

        for opcao in opcoes:
            self.assertIn("expressao", opcao)
            self.assertIn("multiplicador", opcao)
            self.assertGreater(opcao["multiplicador"], 0)

    def test_multiplicador_jackpot_depende_da_quantidade_de_proposicoes(self):
        self.assertEqual(calcular_multiplicador_jackpot(1), 1)
        self.assertEqual(calcular_multiplicador_jackpot(2), 2)
        self.assertEqual(calcular_multiplicador_jackpot(6), 6)

    def test_vitoria_com_jackpot_multiplica_pela_quantidade_de_proposicoes(self):
        saldo, variacao, multiplicador, jackpot = calcular_rodada(
            100,
            10,
            True,
            2,
            3,
        )

        self.assertEqual(saldo, 150)
        self.assertEqual(variacao, 50)
        self.assertEqual(multiplicador, 6)
        self.assertIs(jackpot, True)

    def test_vitoria_sem_jackpot_nao_dobra_multiplicador(self):
        saldo, variacao, multiplicador, jackpot = calcular_rodada(
            100,
            10,
            True,
            1,
            3,
        )

        self.assertEqual(saldo, 100)
        self.assertEqual(variacao, 0)
        self.assertEqual(multiplicador, 1)
        self.assertIs(jackpot, False)

    def test_derrota_subtrai_aposta(self):
        saldo, variacao, multiplicador, jackpot = calcular_rodada(
            100,
            10,
            False,
            4,
            3,
        )

        self.assertEqual(saldo, 90)
        self.assertEqual(variacao, -10)
        self.assertEqual(multiplicador, 4)
        self.assertIs(jackpot, False)

    def test_operador_invalido_gera_erro(self):
        with self.assertRaises(ValueError):
            aplicar_operador("X", True, False)

    def test_carregar_saldo_cria_arquivo_com_saldo_inicial(self):
        with TemporaryDirectory() as pasta:
            caminho = os.path.join(pasta, "saldo.txt")

            saldo = carregar_saldo(caminho)

            self.assertEqual(saldo, 100)
            with open(caminho, "r", encoding="utf-8") as arquivo:
                self.assertEqual(arquivo.read(), "100")

    def test_salvar_e_carregar_saldo(self):
        with TemporaryDirectory() as pasta:
            caminho = os.path.join(pasta, "saldo.txt")

            salvar_saldo(150, caminho)

            self.assertEqual(carregar_saldo(caminho), 150)

    def test_carregar_saldo_invalido_reinicia_para_saldo_inicial(self):
        with TemporaryDirectory() as pasta:
            caminho = os.path.join(pasta, "saldo.txt")
            with open(caminho, "w", encoding="utf-8") as arquivo:
                arquivo.write("abc")

            saldo = carregar_saldo(caminho)

            self.assertEqual(saldo, 100)
            with open(caminho, "r", encoding="utf-8") as arquivo:
                self.assertEqual(arquivo.read(), "100")


if __name__ == "__main__":
    unittest.main()
