import time

import pyautogui

from configuracoes import (
    AMARELO,
    AZUL,
    AZUL_CLARO,
    BRANCO,
    CINZA,
    LIMITE_PINCA,
    MOVIMENTO_MINIMO,
    TEMPO_ENTRE_ATALHOS,
    TEMPO_PARA_PAUSAR,
    VELOCIDADE_DESLIZE,
    VELOCIDADE_ROLAGEM,
    VELOCIDADE_ZOOM,
    VERMELHO,
)
from detector import dedosLevantados, proporcaoPinca


class ControleAtalhos:
    def __init__(self):
        self.pausado = False
        self.cameraVisivel = True

        self.gestoAtual = None
        self.xReferencia = None
        self.yReferencia = None
        self.tempoReferencia = None
        self.inicioPunhoFechado = None
        self.pausaJaAlternada = False
        self.ultimoUsoAtalho = {}

    def zerarReferencias(self):
        self.xReferencia = None
        self.yReferencia = None
        self.tempoReferencia = None
        self.inicioPunhoFechado = None
        self.pausaJaAlternada = False

    def atalhoLiberado(self, nomeDoAtalho, horaAtual):
        if horaAtual - self.ultimoUsoAtalho.get(nomeDoAtalho, 0) >= TEMPO_ENTRE_ATALHOS:
            self.ultimoUsoAtalho[nomeDoAtalho] = horaAtual
            return True
        return False

    def identificarGesto(self, pontos):
        polegar, indicador, medio, anelar, mindinho = dedosLevantados(pontos)
        dedosSemPolegar = (indicador, medio, anelar, mindinho)

        if not any(dedosSemPolegar):
            return "punho"
        if proporcaoPinca(pontos, 8) < LIMITE_PINCA:
            return "zoom"
        if dedosSemPolegar == (True, True, False, False):
            return "rolagem"
        if dedosSemPolegar == (True, True, True, False):
            return "alternar_janela"
        if all(dedosSemPolegar) and polegar:
            return "palma"
        if polegar and mindinho and not (indicador or medio or anelar):
            return "shaka"
        return None

    def tratarPunho(self, horaAtual):
        if self.inicioPunhoFechado is None:
            self.inicioPunhoFechado = horaAtual

        segundosRestantes = TEMPO_PARA_PAUSAR - (horaAtual - self.inicioPunhoFechado)

        if segundosRestantes <= 0 and not self.pausaJaAlternada:
            self.pausado = not self.pausado
            self.pausaJaAlternada = True
            return "PAUSA ALTERNADA", VERMELHO
        if not self.pausaJaAlternada:
            return f"PUNHO: {segundosRestantes:.1f}s p/ pausar", VERMELHO
        return "PUNHO", VERMELHO

    def tratarShaka(self, horaAtual):
        if self.atalhoLiberado("camera", horaAtual):
            self.cameraVisivel = not self.cameraVisivel
        return "CAMERA", AZUL_CLARO

    def tratarRolagemOuZoom(self, gesto, posicaoY):
        if self.yReferencia is None:
            self.yReferencia = posicaoY
        diferencaY = posicaoY - self.yReferencia

        if abs(diferencaY) > MOVIMENTO_MINIMO:
            if gesto == "rolagem":
                pyautogui.scroll(int(-diferencaY * VELOCIDADE_ROLAGEM))
            else:
                pyautogui.keyDown("ctrl")
                pyautogui.scroll(int(-diferencaY * VELOCIDADE_ZOOM))
                pyautogui.keyUp("ctrl")
            self.yReferencia = posicaoY

        return ("ROLAGEM" if gesto == "rolagem" else "ZOOM"), AMARELO

    def tratarAlternarJanela(self, horaAtual):
        if self.atalhoLiberado("alternar_janela", horaAtual):
            pyautogui.hotkey("alt", "tab")
        return "ALT+TAB", AZUL

    def tratarPalma(self, posicaoX, horaAtual):
        if self.xReferencia is not None and self.tempoReferencia is not None:
            intervalo = max(horaAtual - self.tempoReferencia, 1e-3)
            velocidade = (posicaoX - self.xReferencia) / intervalo

            if abs(velocidade) > VELOCIDADE_DESLIZE and self.atalhoLiberado("deslize", horaAtual):
                if velocidade > 0:
                    pyautogui.hotkey("alt", "right")
                else:
                    pyautogui.hotkey("alt", "left")

        self.xReferencia = posicaoX
        self.tempoReferencia = horaAtual
        return "PALMA: deslize p/ voltar/avancar", CINZA

    def controlar(self, pontos):
        horaAtual = time.time()
        gesto = self.identificarGesto(pontos)

        if gesto != self.gestoAtual:
            self.zerarReferencias()
            self.gestoAtual = gesto

        posicaoX = pontos[9].x
        posicaoY = pontos[9].y

        if gesto == "punho":
            return self.tratarPunho(horaAtual)

        if gesto == "shaka":
            return self.tratarShaka(horaAtual)

        if self.pausado:
            return "PAUSADO", VERMELHO

        if gesto in ("rolagem", "zoom"):
            return self.tratarRolagemOuZoom(gesto, posicaoY)

        if gesto == "alternar_janela":
            return self.tratarAlternarJanela(horaAtual)

        if gesto == "palma":
            return self.tratarPalma(posicaoX, horaAtual)

        return "", BRANCO

    def maoSumiu(self):
        self.gestoAtual = None
        self.zerarReferencias()

    def soltarTudo(self):
        pyautogui.keyUp("ctrl")
