import pyautogui

from configuracoes import (
    CIANO,
    LARANJA,
    LIMITE_PINCA,
    MAGENTA,
    SENSIBILIDADE,
    SUAVIZACAO,
    VERDE,
    VERMELHO,
)
from detector import proporcaoPinca


class ControleCursor:
    def __init__(self):
        self.ultimoX = None
        self.ultimoY = None
        self.movimentoSuaveX = 0
        self.movimentoSuaveY = 0

        self.cliqueEsquerdoAnterior = False
        self.cliqueDireitoAnterior = False
        self.cliqueDuploAnterior = False

    def zerarMovimento(self):
        self.ultimoX = None
        self.ultimoY = None
        self.movimentoSuaveX = 0
        self.movimentoSuaveY = 0

    def moverCursor(self, ponto, larguraImagem, alturaImagem):
        if self.ultimoX is not None:
            deslocamentoX = (ponto.x - self.ultimoX) * larguraImagem * SENSIBILIDADE
            deslocamentoY = (ponto.y - self.ultimoY) * alturaImagem * SENSIBILIDADE

            self.movimentoSuaveX += (deslocamentoX - self.movimentoSuaveX) * SUAVIZACAO
            self.movimentoSuaveY += (deslocamentoY - self.movimentoSuaveY) * SUAVIZACAO

            pyautogui.moveRel(int(self.movimentoSuaveX), int(self.movimentoSuaveY))

        self.ultimoX = ponto.x
        self.ultimoY = ponto.y

    def atualizarCliques(self, cliqueEsquerdo, cliqueDireito):
        if cliqueEsquerdo and not self.cliqueEsquerdoAnterior:
            pyautogui.mouseDown(button="left")
        elif not cliqueEsquerdo and self.cliqueEsquerdoAnterior:
            pyautogui.mouseUp(button="left")

        if cliqueDireito and not self.cliqueDireitoAnterior:
            pyautogui.mouseDown(button="right")
        elif not cliqueDireito and self.cliqueDireitoAnterior:
            pyautogui.mouseUp(button="right")

        self.cliqueEsquerdoAnterior = cliqueEsquerdo
        self.cliqueDireitoAnterior = cliqueDireito

    def atualizarCliqueDuplo(self, cliqueDuplo):
        if cliqueDuplo and not self.cliqueDuploAnterior:
            pyautogui.doubleClick()
        self.cliqueDuploAnterior = cliqueDuplo

    def soltarCliques(self):
        self.atualizarCliques(False, False)
        self.cliqueDuploAnterior = False

    def identificarGesto(self, pontos):
        proporcoes = {
            "clique_esquerdo": proporcaoPinca(pontos, 8),
            "clique_direito": proporcaoPinca(pontos, 12),
            "clique_duplo": proporcaoPinca(pontos, 16),
        }
        gesto = min(proporcoes, key=proporcoes.get)

        if proporcoes[gesto] > LIMITE_PINCA:
            return None
        return gesto

    def controlar(self, pontos, larguraImagem, alturaImagem, pausado):
        if pausado:
            self.zerarMovimento()
            self.soltarCliques()
            return "PAUSADO", VERMELHO

        self.moverCursor(pontos[9], larguraImagem, alturaImagem)

        gesto = self.identificarGesto(pontos)

        self.atualizarCliques(gesto == "clique_esquerdo", gesto == "clique_direito")
        self.atualizarCliqueDuplo(gesto == "clique_duplo")

        if gesto == "clique_esquerdo":
            return "CLIQUE ESQUERDO / ARRASTAR", VERDE
        if gesto == "clique_direito":
            return "CLIQUE DIREITO", MAGENTA
        if gesto == "clique_duplo":
            return "CLIQUE DUPLO", LARANJA
        return "MOVENDO MOUSE", CIANO

    def maoSumiu(self):
        self.zerarMovimento()
        self.soltarCliques()

    def soltarTudo(self):
        self.soltarCliques()
        pyautogui.mouseUp(button="left")
        pyautogui.mouseUp(button="right")
