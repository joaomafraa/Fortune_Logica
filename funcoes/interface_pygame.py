import os

try:
    import pygame
except ModuleNotFoundError:
    pygame = None

from funcoes.constantes import PROPOSICOES
from funcoes.logica import (
    avaliar_expressao_com_proposicoes,
    calcular_chance_verdadeira,
    calcular_multiplicador,
    calcular_rodada,
    sortear_proposicoes,
)
from funcoes.saldo import carregar_saldo, salvar_saldo


LARGURA = 1100
ALTURA = 720
FPS = 60
PASTA_RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CAMINHOS_FUNDO = (
    os.path.join(PASTA_RAIZ, "assets", "fundo.png"),
    os.path.join(PASTA_RAIZ, "assets", "fundo.jpg"),
    os.path.join(PASTA_RAIZ, "assets", "fundo.jpeg"),
    os.path.join(PASTA_RAIZ, "assets", "fundo.webp"),
)
CAMINHOS_CACA_NIQUEL = (
    os.path.join(PASTA_RAIZ, "assets", "caçaniquel.png"),
    os.path.join(PASTA_RAIZ, "assets", "cacaniquel.png"),
    os.path.join(PASTA_RAIZ, "assets", "rolos_da_sorte.png"),
)
CAMINHOS_EXPRESSAO = (
    os.path.join(PASTA_RAIZ, "assets", "expressao.png"),
    os.path.join(PASTA_RAIZ, "assets", "expressao_logica.png"),
)

FUNDO = (9, 18, 38)
PAINEL = (23, 37, 66)
PAINEL_ESCURO = (14, 24, 46)
DESTAQUE = (245, 199, 90)
DESTAQUE_ESCURO = (161, 119, 34)
CLARO = (207, 224, 255)
BRANCO = (255, 255, 255)
PRETO = (7, 11, 22)
VERDE = (43, 177, 111)
VERMELHO = (199, 70, 70)
AZUL_BOTAO = (64, 124, 214)
CINZA = (80, 92, 115)
DOURADO = (236, 181, 57)
DOURADO_CLARO = (255, 224, 120)
ROXO = (91, 58, 154)
ROXO_ESCURO = (43, 28, 80)
VERMELHO_ESCURO = (105, 26, 44)

OPERADORES = ("E", "OU", "SE", "SSE")


def formatar_multiplicador(multiplicador):
    if multiplicador == int(multiplicador):
        return f"x{int(multiplicador)}"

    return f"x{multiplicador:.2f}"


def formatar_expressao(tokens):
    if not tokens:
        return "Monte sua expressao nos slots"

    return " ".join(tokens)


def analisar_tokens(tokens, nomes):
    termos = []
    operadores = []
    partes = []
    esperando_proposicao = True
    negado = False

    for token in tokens:
        if esperando_proposicao:
            if token == "NAO":
                if negado:
                    return None, "NAO ja foi aplicado. Escolha uma proposicao."
                negado = True
            elif token in nomes:
                termos.append((token, negado))
                if negado:
                    partes.append(f"NAO {token}")
                else:
                    partes.append(token)
                esperando_proposicao = False
                negado = False
            else:
                return None, "Escolha uma proposicao antes do operador."
        else:
            if token in OPERADORES:
                operadores.append(token)
                partes.append(token)
                esperando_proposicao = True
            else:
                return None, "Escolha um operador antes da proxima proposicao."

    if not termos:
        return None, "A expressao precisa ter pelo menos uma proposicao."

    if esperando_proposicao:
        return None, "A expressao nao pode terminar com operador ou NAO."

    dados = {
        "expressao": " ".join(partes),
        "termos": termos,
        "operadores": operadores,
    }

    return dados, "Expressao valida."


def calcular_preview(tokens, nomes):
    dados, mensagem = analisar_tokens(tokens, nomes)

    if dados is None:
        return {
            "valida": False,
            "mensagem": mensagem,
            "expressao": formatar_expressao(tokens),
            "verdadeiros": 0,
            "total": 0,
            "chance": 0,
            "multiplicador": 0,
            "termos": [],
            "operadores": [],
        }

    verdadeiros, total = calcular_chance_verdadeira(
        nomes,
        dados["termos"],
        dados["operadores"],
    )
    multiplicador = calcular_multiplicador(verdadeiros, total)
    chance = (verdadeiros / total) * 100

    return {
        "valida": True,
        "mensagem": mensagem,
        "expressao": dados["expressao"],
        "verdadeiros": verdadeiros,
        "total": total,
        "chance": chance,
        "multiplicador": multiplicador,
        "termos": dados["termos"],
        "operadores": dados["operadores"],
    }


class Botao:
    def __init__(self, x, y, largura, altura, texto, acao, cor=AZUL_BOTAO, ativo=True):
        self.rect = pygame.Rect(x, y, largura, altura)
        self.texto = texto
        self.acao = acao
        self.cor = cor
        self.ativo = ativo

    def desenhar(self, tela, fonte):
        cor = self.cor if self.ativo else CINZA
        pygame.draw.rect(tela, cor, self.rect, border_radius=10)
        pygame.draw.rect(tela, (106, 143, 197), self.rect, 2, border_radius=10)
        texto = fonte.render(self.texto, True, BRANCO if self.ativo else CLARO)
        tela.blit(texto, texto.get_rect(center=self.rect.center))

    def clicou(self, posicao):
        return self.ativo and self.rect.collidepoint(posicao)


class CampoTexto:
    def __init__(self, x, y, largura, altura, nome, texto):
        self.rect = pygame.Rect(x, y, largura, altura)
        self.nome = nome
        self.texto = texto

    def desenhar(self, tela, fonte, fonte_pequena, ativo=False):
        cor_borda = DESTAQUE if ativo else (106, 143, 197)
        pygame.draw.rect(tela, (14, 24, 46), self.rect, border_radius=10)
        pygame.draw.rect(tela, cor_borda, self.rect, 2, border_radius=10)

        label = fonte_pequena.render(self.nome, True, CLARO)
        tela.blit(label, (self.rect.x, self.rect.y - 20))

        texto = self.texto
        if ativo:
            texto += "|"

        superficie = fonte.render(texto, True, BRANCO)
        tela.blit(superficie, superficie.get_rect(center=self.rect.center))

    def clicou(self, posicao):
        return self.rect.collidepoint(posicao)


class InterfacePygame:
    def __init__(self):
        if pygame is None:
            raise RuntimeError("Pygame nao esta instalado. Rode: pip install -r requirements.txt")

        pygame.init()
        pygame.display.set_caption("Fortune Logica")
        self.tela = pygame.display.set_mode((LARGURA, ALTURA))
        self.relogio = pygame.time.Clock()
        self.fonte_titulo = pygame.font.SysFont("arial", 42, bold=True)
        self.fonte_expressao = pygame.font.SysFont("arial", 34, bold=True)
        self.fonte_grande = pygame.font.SysFont("arial", 28, bold=True)
        self.fonte_media = pygame.font.SysFont("arial", 20, bold=True)
        self.fonte_pequena = pygame.font.SysFont("arial", 16, bold=True)
        self.fundo_imagem = self.carregar_fundo()
        self.caca_niquel_imagem = self.carregar_caca_niquel()
        self.expressao_imagem = self.carregar_expressao()

        self.saldo = carregar_saldo()
        self.aposta = 10
        self.quantidade = 3
        self.aposta_texto = str(self.aposta)
        self.quantidade_texto = str(self.quantidade)
        self.campo_ativo = None
        self.campo_aposta = CampoTexto(690, 626, 90, 42, "Aposta", self.aposta_texto)
        self.campo_quantidade = CampoTexto(800, 626, 90, 42, "Premissas", self.quantidade_texto)
        self.negacoes = []
        self.operadores_slots = []
        self.proposicoes_sorteadas = {}
        self.status = "Clique nos slots de operador para montar a expressao."
        self.resultado = ""
        self.tela_resultado = False
        self.ultima_rodada = {}
        self.animando = False
        self.inicio_animacao = 0
        self.resultado_pendente = {}
        self.rodando = True
        self.botoes = []
        self.slot_premissas = []
        self.slot_operadores = []
        self.resetar_slots()

    def carregar_fundo(self):
        for caminho in CAMINHOS_FUNDO:
            if os.path.exists(caminho):
                imagem = pygame.image.load(caminho).convert()
                return pygame.transform.smoothscale(imagem, (LARGURA, ALTURA))

        return None

    def carregar_caca_niquel(self):
        for caminho in CAMINHOS_CACA_NIQUEL:
            if os.path.exists(caminho):
                return pygame.image.load(caminho).convert_alpha()

        return None

    def carregar_expressao(self):
        for caminho in CAMINHOS_EXPRESSAO:
            if os.path.exists(caminho):
                return pygame.image.load(caminho).convert_alpha()

        return None

    def desenhar_fundo(self):
        if self.fundo_imagem is not None:
            self.tela.blit(self.fundo_imagem, (0, 0))
            sombra = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)
            sombra.fill((0, 0, 0, 15))
            self.tela.blit(sombra, (0, 0))
            return

        self.tela.fill(FUNDO)
        pygame.draw.circle(self.tela, (18, 35, 70), (160, 100), 190)
        pygame.draw.circle(self.tela, (20, 52, 94), (940, 600), 220)
        pygame.draw.rect(self.tela, (51, 78, 121), (20, 20, 1060, 680), 4, border_radius=24)

    def nomes_ativos(self):
        return PROPOSICOES[: self.quantidade]

    def resetar_slots(self):
        self.negacoes = []
        self.operadores_slots = []

        for _ in range(self.quantidade):
            self.negacoes.append(False)

        for _ in range(self.quantidade - 1):
            self.operadores_slots.append(None)

    def tokens_dos_slots(self):
        tokens = []
        nomes = self.nomes_ativos()

        for indice, nome in enumerate(nomes):
            if self.negacoes[indice]:
                tokens.append("NAO")

            tokens.append(nome)

            if indice < len(self.operadores_slots):
                operador = self.operadores_slots[indice]

                if operador is not None:
                    tokens.append(operador)

        return tokens

    def limitar_aposta(self):
        if self.aposta < 1:
            self.aposta = 1
        if self.aposta > self.saldo:
            self.aposta = self.saldo
        self.aposta_texto = str(self.aposta)
        self.campo_aposta.texto = self.aposta_texto

    def definir_quantidade(self, quantidade):
        antiga_quantidade = self.quantidade
        self.quantidade = quantidade

        if self.quantidade < 1:
            self.quantidade = 1
        if self.quantidade > 6:
            self.quantidade = 6

        if self.quantidade != antiga_quantidade:
            self.resetar_slots()
            self.proposicoes_sorteadas = {}
            self.resultado = ""
            self.status = "Premissas alteradas. Escolha os operadores nos slots."

        self.quantidade_texto = str(self.quantidade)
        self.campo_quantidade.texto = self.quantidade_texto

    def campos_validos(self):
        if not self.aposta_texto.isdigit():
            return False
        if not self.quantidade_texto.isdigit():
            return False

        aposta = int(self.aposta_texto)
        quantidade = int(self.quantidade_texto)

        return 1 <= aposta <= self.saldo and 1 <= quantidade <= 6

    def aplicar_texto_dos_campos(self):
        if self.aposta_texto.isdigit():
            self.aposta = int(self.aposta_texto)

        if self.quantidade_texto.isdigit():
            quantidade = int(self.quantidade_texto)

            if 1 <= quantidade <= 6:
                self.definir_quantidade(quantidade)

    def alternar_negacao(self, indice):
        if 0 <= indice < len(self.negacoes):
            self.negacoes[indice] = not self.negacoes[indice]
            self.status = "NAO alternado na premissa."
            self.resultado = ""

    def alternar_operador(self, indice):
        if not 0 <= indice < len(self.operadores_slots):
            return

        atual = self.operadores_slots[indice]

        if atual is None:
            self.operadores_slots[indice] = OPERADORES[0]
        else:
            proximo = (OPERADORES.index(atual) + 1) % len(OPERADORES)
            self.operadores_slots[indice] = OPERADORES[proximo]

        self.status = "Operador alterado."
        self.resultado = ""

    def limpar_expressao(self):
        if self.animando:
            return

        self.resetar_slots()
        self.proposicoes_sorteadas = {}
        self.resultado = ""
        self.tela_resultado = False
        self.ultima_rodada = {}
        self.resultado_pendente = {}
        self.status = "Expressao limpa."

    def continuar_depois_resultado(self):
        self.tela_resultado = False
        self.resultado = ""
        self.ultima_rodada = {}
        self.resultado_pendente = {}
        self.status = "Monte a expressao e clique em GIRAR."

    def girar(self):
        if self.animando:
            return

        if not self.campos_validos():
            self.status = "Digite uma aposta valida e premissas de 1 a 6."
            return

        self.aplicar_texto_dos_campos()
        preview = calcular_preview(self.tokens_dos_slots(), self.nomes_ativos())

        if not preview["valida"]:
            self.status = preview["mensagem"]
            return

        if self.saldo <= 0:
            self.status = "Saldo zerado. Edite saldo.txt para recomecar."
            return

        proposicoes = sortear_proposicoes(self.quantidade)
        resultado_logico = avaliar_expressao_com_proposicoes(
            preview["termos"],
            preview["operadores"],
            proposicoes,
        )
        novo_saldo, variacao, multiplicador_final, jackpot = calcular_rodada(
            self.saldo,
            self.aposta,
            resultado_logico,
            preview["multiplicador"],
            self.quantidade,
            proposicoes,
        )

        resultado_texto = ""
        if jackpot:
            resultado_texto = (
                f"JACKPOT! Todas cairam V. Final {formatar_multiplicador(multiplicador_final)}. "
                f"Lucro {variacao}."
            )
        elif resultado_logico:
            resultado_texto = (
                f"VITORIA! Final {formatar_multiplicador(multiplicador_final)}. "
                f"Lucro {variacao}."
            )
        else:
            resultado_texto = f"DERROTA. Voce perdeu {-variacao}."

        self.resultado_pendente = {
            "novo_saldo": novo_saldo,
            "proposicoes": proposicoes,
            "resultado": resultado_texto,
            "jackpot": jackpot,
            "resultado_logico": resultado_logico,
            "variacao": variacao,
            "multiplicador_final": multiplicador_final,
        }
        self.proposicoes_sorteadas = {}
        self.inicio_animacao = pygame.time.get_ticks()
        self.animando = True
        self.status = "Girando os rolos... aguarde o resultado."

    def finalizar_animacao(self):
        if not self.resultado_pendente:
            self.animando = False
            return

        self.saldo = self.resultado_pendente["novo_saldo"]
        salvar_saldo(self.saldo)
        self.proposicoes_sorteadas = self.resultado_pendente["proposicoes"]
        self.resultado = self.resultado_pendente["resultado"]
        self.ultima_rodada = {
            "jackpot": self.resultado_pendente["jackpot"],
            "resultado_logico": self.resultado_pendente["resultado_logico"],
            "variacao": self.resultado_pendente["variacao"],
            "multiplicador_final": self.resultado_pendente["multiplicador_final"],
        }

        self.animando = False
        self.status = "Rodada finalizada. Ajuste ou gire de novo."
        self.tela_resultado = True

    def criar_botoes(self, preview):
        self.botoes = []
        if self.tela_resultado:
            self.botoes.append(Botao(440, 585, 220, 58, "CONTINUAR", self.continuar_depois_resultado, AZUL_BOTAO))
            return

        self.botoes.append(Botao(70, 626, 120, 42, "LIMPAR", self.limpar_expressao, VERMELHO))
        texto_girar = "GIRANDO..." if self.animando else "GIRAR"
        self.botoes.append(Botao(440, 620, 220, 54, texto_girar, self.girar, VERDE, preview["valida"] and self.campos_validos() and not self.animando))

    def desenhar_texto(self, texto, x, y, fonte, cor=BRANCO):
        superficie = fonte.render(texto, True, cor)
        self.tela.blit(superficie, (x, y))

    def desenhar_painel(self, rect, cor=PAINEL):
        pygame.draw.rect(self.tela, cor, rect, border_radius=16)
        pygame.draw.rect(self.tela, (72, 101, 151), rect, 2, border_radius=16)

    def desenhar_painel_transparente(self, rect, cor, alpha=185, borda=DOURADO):
        superficie = pygame.Surface((rect.w, rect.h), pygame.SRCALPHA)
        pygame.draw.rect(superficie, (*cor, alpha), superficie.get_rect(), border_radius=18)
        pygame.draw.rect(superficie, (*borda, 230), superficie.get_rect(), 2, border_radius=18)
        self.tela.blit(superficie, rect.topleft)

    def desenhar_moldura_slot(self, rect):
        sombra = rect.move(0, 8)
        pygame.draw.rect(self.tela, (5, 8, 18), sombra, border_radius=28)
        pygame.draw.rect(self.tela, DOURADO, rect, border_radius=28)
        pygame.draw.rect(self.tela, DOURADO_CLARO, rect, 4, border_radius=28)

        interno = rect.inflate(-24, -24)
        pygame.draw.rect(self.tela, ROXO_ESCURO, interno, border_radius=20)
        pygame.draw.rect(self.tela, (33, 51, 88), interno, 3, border_radius=20)

        for indice in range(11):
            x = rect.x + 24 + indice * 74
            pygame.draw.circle(self.tela, DOURADO_CLARO, (x, rect.y + 18), 6)
            pygame.draw.circle(self.tela, DOURADO_CLARO, (x, rect.bottom - 18), 6)

    def desenhar_texto_centralizado(self, texto, rect, fonte, cor=BRANCO):
        superficie = fonte.render(texto, True, cor)
        self.tela.blit(superficie, superficie.get_rect(center=rect.center))

    def desenhar_imagem_recortada(self, imagem, origem, destino):
        recorte = imagem.subsurface(origem).copy()
        recorte = pygame.transform.smoothscale(recorte, (destino.w, destino.h))
        self.tela.blit(recorte, destino.topleft)

    def valor_animado_do_rolo(self, nome, indice):
        if not self.animando:
            if nome in self.proposicoes_sorteadas:
                return "V" if self.proposicoes_sorteadas[nome] else "F"
            return "?"

        agora = pygame.time.get_ticks()
        tempo = agora - self.inicio_animacao
        tempo_parada = 900 + indice * 450
        proposicoes_finais = self.resultado_pendente.get("proposicoes", {})

        if tempo >= tempo_parada and nome in proposicoes_finais:
            return "V" if proposicoes_finais[nome] else "F"

        ciclo = (tempo // 90 + indice) % 4
        valores = ("V", "F", "?", "F")
        return valores[ciclo]

    def atualizar_animacao(self):
        if not self.animando:
            return

        tempo_total = 900 + (self.quantidade - 1) * 450 + 650
        if pygame.time.get_ticks() - self.inicio_animacao >= tempo_total:
            self.finalizar_animacao()

    def desenhar_slot(self):
        rect = pygame.Rect(245, 105, 610, 407)

        if self.caca_niquel_imagem is not None:
            imagem = pygame.transform.smoothscale(self.caca_niquel_imagem, (rect.w, rect.h))
            self.tela.blit(imagem, rect.topleft)
        else:
            self.desenhar_moldura_slot(rect)
            self.desenhar_texto_centralizado("ROLOS DA SORTE", pygame.Rect(rect.x, rect.y + 10, rect.w, 28), self.fonte_media, PRETO)

        area_rolos = pygame.Rect(rect.x + 58, rect.y + 190, rect.w - 116, 112)

        nomes = self.nomes_ativos()
        largura_caixa = 80
        altura_caixa = 72
        espaco = 11

        if len(nomes) == 4:
            largura_caixa = 70
            espaco = 9
        elif len(nomes) >= 5:
            largura_caixa = 58
            altura_caixa = 64
            espaco = 7

        total_largura = len(nomes) * largura_caixa + (len(nomes) - 1) * espaco
        inicio_x = area_rolos.centerx - total_largura // 2
        inicio_y = area_rolos.centery - altura_caixa // 2

        for indice, nome in enumerate(nomes):
            x = inicio_x + indice * (largura_caixa + espaco)
            caixa = pygame.Rect(x, inicio_y, largura_caixa, altura_caixa)
            pygame.draw.rect(self.tela, (7, 12, 28), caixa.move(0, 4), border_radius=16)
            pygame.draw.rect(self.tela, BRANCO, caixa, border_radius=16)
            pygame.draw.rect(self.tela, (230, 238, 255), caixa.inflate(-8, -8), border_radius=12)
            pygame.draw.rect(self.tela, DOURADO, caixa, 3, border_radius=16)

            brilho = pygame.Rect(caixa.x + 8, caixa.y + 8, caixa.w - 16, 16)
            pygame.draw.rect(self.tela, (255, 255, 255), brilho, border_radius=8)

            valor = self.valor_animado_do_rolo(nome, indice)
            cor_valor = ROXO
            if valor == "V":
                cor_valor = VERDE
            elif valor == "F":
                cor_valor = VERMELHO

            self.desenhar_texto_centralizado(nome, pygame.Rect(x, inicio_y + 6, largura_caixa, 18), self.fonte_pequena, ROXO_ESCURO)
            self.desenhar_texto_centralizado(valor, pygame.Rect(x, inicio_y + 24, largura_caixa, 42), self.fonte_titulo, cor_valor)

    def desenhar_pagina_resultado(self):
        self.desenhar_fundo()

        if self.fundo_imagem is None:
            self.desenhar_texto("FORTUNE LOGICA", 70, 35, self.fonte_titulo, DESTAQUE)

        self.desenhar_painel_transparente(pygame.Rect(55, 72, 190, 54), ROXO_ESCURO, 190)
        self.desenhar_texto(f"Saldo: {self.saldo}", 82, 90, self.fonte_media, DOURADO_CLARO)

        painel = pygame.Rect(275, 235, 550, 330)
        cor_painel = DESTAQUE_ESCURO if self.ultima_rodada.get("jackpot") else PAINEL_ESCURO
        self.desenhar_painel_transparente(painel, cor_painel, 215)

        if self.ultima_rodada.get("jackpot"):
            titulo = "JACKPOT"
            cor_titulo = DESTAQUE
        elif self.ultima_rodada.get("resultado_logico"):
            titulo = "VOCE GANHOU"
            cor_titulo = VERDE
        else:
            titulo = "VOCE PERDEU"
            cor_titulo = VERMELHO

        self.desenhar_texto_centralizado(titulo, pygame.Rect(275, 260, 550, 64), self.fonte_titulo, cor_titulo)
        self.desenhar_texto_centralizado(self.resultado, pygame.Rect(305, 335, 490, 48), self.fonte_media, BRANCO)

        multiplicador = self.ultima_rodada.get("multiplicador_final", 0)
        variacao = self.ultima_rodada.get("variacao", 0)
        resultado_logico = "VERDADEIRO" if self.ultima_rodada.get("resultado_logico") else "FALSO"

        self.desenhar_texto_centralizado(
            f"Resultado logico: {resultado_logico}",
            pygame.Rect(305, 395, 490, 32),
            self.fonte_media,
            CLARO,
        )
        self.desenhar_texto_centralizado(
            f"Multiplicador final: {formatar_multiplicador(multiplicador)}",
            pygame.Rect(305, 435, 490, 32),
            self.fonte_media,
            DESTAQUE,
        )
        self.desenhar_texto_centralizado(
            f"Variacao no saldo: {variacao} moedas",
            pygame.Rect(305, 475, 490, 32),
            self.fonte_media,
            BRANCO,
        )

        for botao in self.botoes:
            botao.desenhar(self.tela, self.fonte_pequena)

        pygame.display.flip()

    def desenhar_expressao_slots(self, preview):
        self.slot_premissas = []
        self.slot_operadores = []

        nomes = self.nomes_ativos()
        if len(nomes) <= 3:
            premise_w = 62
            operator_w = 44
            gap = 6
            fonte_slot = self.fonte_pequena
        elif len(nomes) <= 4:
            premise_w = 48
            operator_w = 34
            gap = 5
            fonte_slot = self.fonte_pequena
        else:
            premise_w = 32
            operator_w = 24
            gap = 3
            fonte_slot = self.fonte_pequena

        total_w = len(nomes) * premise_w + (len(nomes) - 1) * operator_w + (len(nomes) * 2 - 2) * gap
        x = 550 - total_w // 2
        y = 495

        for indice, nome in enumerate(nomes):
            premissa_rect = pygame.Rect(x, y, premise_w, 44)
            self.slot_premissas.append((premissa_rect, indice))
            pygame.draw.rect(self.tela, (37, 64, 112), premissa_rect, border_radius=14)
            pygame.draw.rect(self.tela, DESTAQUE, premissa_rect, 2, border_radius=14)

            texto = nome
            if self.negacoes[indice]:
                texto = f"NAO {nome}"

            self.desenhar_texto_centralizado(texto, premissa_rect, fonte_slot, BRANCO)

            x += premise_w + gap

            if indice < len(nomes) - 1:
                operador_rect = pygame.Rect(x, y + 7, operator_w, 30)
                self.slot_operadores.append((operador_rect, indice))
                operador = self.operadores_slots[indice]
                cor = (52, 89, 154) if operador is not None else (28, 39, 65)
                pygame.draw.rect(self.tela, cor, operador_rect, border_radius=12)
                pygame.draw.rect(self.tela, CLARO, operador_rect, 2, border_radius=12)
                self.desenhar_texto_centralizado(operador or "?", operador_rect, fonte_slot, DESTAQUE)
                x += operator_w + gap

        if preview["valida"]:
            resumo_texto = f"% = {preview['chance']:.2f}%    Xx = {formatar_multiplicador(preview['multiplicador'])}"
        else:
            resumo_texto = "% = --    Xx = --"

        self.desenhar_texto_centralizado(resumo_texto, pygame.Rect(320, 550, 460, 24), self.fonte_pequena, DESTAQUE)

    def desenhar(self):
        self.atualizar_animacao()
        preview = calcular_preview(self.tokens_dos_slots(), self.nomes_ativos())
        self.criar_botoes(preview)

        if self.tela_resultado:
            self.desenhar_pagina_resultado()
            return

        self.desenhar_fundo()

        if self.fundo_imagem is None:
            self.desenhar_texto("FORTUNE LOGICA", 70, 35, self.fonte_titulo, DESTAQUE)

        self.desenhar_painel_transparente(pygame.Rect(55, 72, 190, 54), ROXO_ESCURO, 190)
        self.desenhar_texto(f"Saldo: {self.saldo}", 82, 90, self.fonte_media, DOURADO_CLARO)
        self.campo_aposta.desenhar(
            self.tela,
            self.fonte_media,
            self.fonte_pequena,
            self.campo_ativo == "aposta",
        )
        self.campo_quantidade.desenhar(
            self.tela,
            self.fonte_media,
            self.fonte_pequena,
            self.campo_ativo == "quantidade",
        )

        self.desenhar_slot()

        expressao_largura = 520
        expressao_altura = 345
        expressao_rect = pygame.Rect(290, 325, expressao_largura, expressao_altura)

        if self.expressao_imagem is not None:
            imagem = pygame.transform.smoothscale(self.expressao_imagem, (expressao_rect.w, expressao_rect.h))
            self.tela.blit(imagem, expressao_rect.topleft)
        else:
            self.desenhar_painel_transparente(expressao_rect, ROXO_ESCURO, 195)
            self.desenhar_texto_centralizado("MONTE SUA EXPRESSAO", pygame.Rect(200, 408, 700, 28), self.fonte_media, DESTAQUE)

        self.desenhar_expressao_slots(preview)

        for botao in self.botoes:
            botao.desenhar(self.tela, self.fonte_pequena)

        pygame.display.flip()

    def tratar_digitacao(self, evento):
        if self.campo_ativo is None:
            return

        if evento.key == pygame.K_RETURN:
            self.campo_ativo = None
            return

        if evento.key == pygame.K_BACKSPACE:
            if self.campo_ativo == "aposta":
                self.aposta_texto = self.aposta_texto[:-1]
                self.campo_aposta.texto = self.aposta_texto
            elif self.campo_ativo == "quantidade":
                self.quantidade_texto = self.quantidade_texto[:-1]
                self.campo_quantidade.texto = self.quantidade_texto
            return

        if not evento.unicode.isdigit():
            return

        if self.campo_ativo == "aposta":
            if len(self.aposta_texto) < 4:
                self.aposta_texto += evento.unicode
                self.campo_aposta.texto = self.aposta_texto
                if self.aposta_texto.isdigit():
                    self.aposta = int(self.aposta_texto)
                self.status = "Aposta digitada pelo jogador."
        elif self.campo_ativo == "quantidade":
            self.quantidade_texto = evento.unicode
            self.campo_quantidade.texto = self.quantidade_texto
            if self.quantidade_texto.isdigit():
                quantidade = int(self.quantidade_texto)
                if 1 <= quantidade <= 6:
                    self.definir_quantidade(quantidade)
                else:
                    self.status = "Use de 1 a 6 premissas."

    def tratar_eventos(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self.rodando = False
            elif evento.type == pygame.KEYDOWN:
                if self.animando:
                    continue
                self.tratar_digitacao(evento)
            elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                if self.animando:
                    continue

                if self.tela_resultado:
                    for botao in self.botoes:
                        if botao.clicou(evento.pos):
                            botao.acao()
                            break
                    return

                if self.campo_aposta.clicou(evento.pos):
                    self.campo_ativo = "aposta"
                    return

                if self.campo_quantidade.clicou(evento.pos):
                    self.campo_ativo = "quantidade"
                    return

                self.campo_ativo = None

                for rect, indice in self.slot_premissas:
                    if rect.collidepoint(evento.pos):
                        self.alternar_negacao(indice)
                        return

                for rect, indice in self.slot_operadores:
                    if rect.collidepoint(evento.pos):
                        self.alternar_operador(indice)
                        return

                for botao in self.botoes:
                    if botao.clicou(evento.pos):
                        botao.acao()
                        break

    def executar(self):
        while self.rodando:
            self.tratar_eventos()
            self.desenhar()
            self.relogio.tick(FPS)

        pygame.quit()


def main():
    if pygame is None:
        print("Pygame nao esta instalado.")
        print("Instale com: pip install -r requirements.txt")
        return

    app = InterfacePygame()
    app.executar()


if __name__ == "__main__":
    main()
