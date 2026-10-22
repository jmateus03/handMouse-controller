import math

import mediapipe as mp

from configuracoes import CONFIANCA_DETECCAO, MAXIMO_DE_MAOS

modeloMaos = mp.solutions.hands
desenhoMaos = mp.solutions.drawing_utils

detectorMaos = modeloMaos.Hands(
    max_num_hands=MAXIMO_DE_MAOS,
    min_detection_confidence=CONFIANCA_DETECCAO,
    min_tracking_confidence=CONFIANCA_DETECCAO,
)


def distanciaEntre(pontoA, pontoB):
    return math.hypot(pontoA.x - pontoB.x, pontoA.y - pontoB.y)


def tamanhoDaMao(pontos):
    return distanciaEntre(pontos[0], pontos[9]) or 1e-6


def proporcaoPinca(pontos, pontaDoDedo):
    return distanciaEntre(pontos[4], pontos[pontaDoDedo]) / tamanhoDaMao(pontos)


def dedosLevantados(pontos):
    pulso = pontos[0]

    def dedoLevantado(pontaDoDedo, juntaDoDedo):
        return distanciaEntre(pontos[pontaDoDedo], pulso) > distanciaEntre(pontos[juntaDoDedo], pulso)

    polegar = distanciaEntre(pontos[4], pontos[17]) > distanciaEntre(pontos[3], pontos[17])

    return (
        polegar,
        dedoLevantado(8, 6),
        dedoLevantado(12, 10),
        dedoLevantado(16, 14),
        dedoLevantado(20, 18),
    )


def separarMaosPorLado(resultado):
    maosEncontradas = {}

    if resultado.multi_hand_landmarks and resultado.multi_handedness:
        for pontos, lado in zip(
            resultado.multi_hand_landmarks,
            resultado.multi_handedness,
        ):
            nomeDoLado = lado.classification[0].label
            if nomeDoLado not in maosEncontradas:
                maosEncontradas[nomeDoLado] = pontos

    return maosEncontradas


def detectarMaos(quadroRGB):
    resultado = detectorMaos.process(quadroRGB)
    return separarMaosPorLado(resultado)


def desenharMaos(quadro, maosEncontradas):
    for pontos in maosEncontradas.values():
        desenhoMaos.draw_landmarks(quadro, pontos, modeloMaos.HAND_CONNECTIONS)


def fecharDetector():
    detectorMaos.close()
