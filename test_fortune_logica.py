import os
import unittest
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
    todas_proposicoes_verdadeiras,
)
from funcoes.interface_pygame import analisar_tokens, calcular_preview, formatar_expressao
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
        self.assertIs(aplicar_operador("SE", False, True), True)
        self.assertIs(aplicar_operador("->", True, False), False)

    def test_operador_sse_bicondicional(self):
        self.assertIs(aplicar_operador("SSE", True, True), True)
        self.assertIs(aplicar_operador("SSE", False, False), True)
        self.assertIs(aplicar_operador("SSE", True, False), False)
        self.assertIs(aplicar_operador("SSE", False, True), False)
        self.assertIs(aplicar_operador("<->", True, True), True)

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

    def test_multiplicador_jackpot_depende_da_quantidade_de_proposicoes(self):
        self.assertEqual(calcular_multiplicador_jackpot(1), 1)
        self.assertEqual(calcular_multiplicador_jackpot(2), 2)
        self.assertEqual(calcular_multiplicador_jackpot(6), 6)

    def test_todas_proposicoes_verdadeiras(self):
        self.assertTrue(todas_proposicoes_verdadeiras({"P": True, "Q": True}))
        self.assertFalse(todas_proposicoes_verdadeiras({"P": True, "Q": False}))

    def test_vitoria_com_jackpot_somente_quando_todas_proposicoes_sao_verdadeiras(self):
        saldo, variacao, multiplicador, jackpot = calcular_rodada(
            100,
            10,
            True,
            2,
            3,
            {"P": True, "Q": True, "R": True},
        )

        self.assertEqual(saldo, 150)
        self.assertEqual(variacao, 50)
        self.assertEqual(multiplicador, 6)
        self.assertIs(jackpot, True)

    def test_vitoria_sem_jackpot_quando_alguma_proposicao_e_falsa(self):
        saldo, variacao, multiplicador, jackpot = calcular_rodada(
            100,
            10,
            True,
            2,
            3,
            {"P": True, "Q": False, "R": True},
        )

        self.assertEqual(saldo, 110)
        self.assertEqual(variacao, 10)
        self.assertEqual(multiplicador, 2)
        self.assertIs(jackpot, False)

    def test_derrota_subtrai_aposta(self):
        saldo, variacao, multiplicador, jackpot = calcular_rodada(
            100,
            10,
            False,
            4,
            3,
            {"P": True, "Q": True, "R": True},
        )

        self.assertEqual(saldo, 90)
        self.assertEqual(variacao, -10)
        self.assertEqual(multiplicador, 4)
        self.assertIs(jackpot, False)

    def test_analisar_tokens_validos(self):
        dados, mensagem = analisar_tokens(["NAO", "P", "E", "Q"], ["P", "Q"])

        self.assertEqual(mensagem, "Expressao valida.")
        self.assertEqual(dados["expressao"], "NAO P E Q")
        self.assertEqual(dados["termos"], [("P", True), ("Q", False)])
        self.assertEqual(dados["operadores"], ["E"])

    def test_analisar_tokens_invalidos(self):
        dados, mensagem = analisar_tokens(["P", "Q"], ["P", "Q"])

        self.assertIsNone(dados)
        self.assertEqual(mensagem, "Escolha um operador antes da proxima proposicao.")

    def test_calcular_preview_valido(self):
        preview = calcular_preview(["P", "E", "Q"], ["P", "Q"])

        self.assertTrue(preview["valida"])
        self.assertEqual(preview["verdadeiros"], 1)
        self.assertEqual(preview["total"], 4)
        self.assertEqual(preview["multiplicador"], 4)

    def test_formatar_expressao_vazia(self):
        self.assertEqual(
            formatar_expressao([]),
            "Monte sua expressao nos slots",
        )

    def test_analisar_tokens_de_slots_com_todas_premissas(self):
        dados, mensagem = analisar_tokens(["P", "E", "Q", "OU", "R"], ["P", "Q", "R"])

        self.assertEqual(mensagem, "Expressao valida.")
        self.assertEqual(dados["termos"], [("P", False), ("Q", False), ("R", False)])
        self.assertEqual(dados["operadores"], ["E", "OU"])

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
