import ctypes
import sys
import time

import pyautogui

from configuracoes import (
    AZUL,
    CINZA,
    NOME_JANELA,
    TEMPO_ENTRE_DUAS_MAOS,
    VARIACAO_DUAS_MAOS,
    VERDE,
)
from detector import dedosLevantados, distanciaEntre, tamanhoDaMao

SW_MAXIMIZE = 3
SW_MINIMIZE = 6


def alterarJanelaAtiva(maximizar):
    if sys.platform != "win32":
        pyautogui.hotkey("win", "up" if maximizar else "down")
        return

    user32 = ctypes.windll.user32
    janela = user32.GetForegroundWindow()
    if not janela:
        return

    tamanho = user32.GetWindowTextLengthW(janela) + 1
    titulo = ctypes.create_unicode_buffer(tamanho)
    user32.GetWindowTextW(janela, titulo, tamanho)

    # nao mexe na janela da camera do proprio controlador
    if titulo.value == NOME_JANELA:
        return

    user32.ShowWindow(janela, SW_MAXIMIZE if maximizar else SW_MINIMIZE)


class ControleDuasMaos:
    def __init__(self):
        self.distanciaReferencia = None
        self.ultimoAcionamento = 0
        self.ultimoTexto = ""
        self.ultimaCor = CINZA

    def zerar(self):
        self.distanciaReferencia = None

    def palmaAberta(self, pontos):
        return all(dedosLevantados(pontos))

    def controlar(self, maosEncontradas):
        if "Left" not in maosEncontradas or "Right" not in maosEncontradas:
            self.zerar()
            return None

        direita = maosEncontradas["Right"].landmark
        esquerda = maosEncontradas["Left"].landmark

        if not (self.palmaAberta(direita) and self.palmaAberta(esquerda)):
            self.zerar()
            return None

        tamanhoMedio = (tamanhoDaMao(direita) + tamanhoDaMao(esquerda)) / 2
        distancia = distanciaEntre(direita[9], esquerda[9]) / tamanhoMedio
        horaAtual = time.time()

        if self.distanciaReferencia is None:
            self.distanciaReferencia = distancia

        variacao = distancia - self.distanciaReferencia
        liberado = horaAtual - self.ultimoAcionamento >= TEMPO_ENTRE_DUAS_MAOS

        if liberado and abs(variacao) >= VARIACAO_DUAS_MAOS:
            maximizar = variacao > 0
            alterarJanelaAtiva(maximizar)
            self.ultimoAcionamento = horaAtual
            self.distanciaReferencia = distancia
            self.ultimoTexto = "MAXIMIZAR" if maximizar else "MINIMIZAR"
            self.ultimaCor = VERDE if maximizar else AZUL

        if horaAtual - self.ultimoAcionamento < 1.0:
            return f"Janela: {self.ultimoTexto}", self.ultimaCor

        return "Duas maos: afaste p/ maximizar, junte p/ minimizar", CINZA
