import cv2
import pyautogui

from atalhos import ControleAtalhos
from configuracoes import INDICE_CAMERA, MAO_DO_CURSOR
from cursor import ControleCursor
from detector import desenharMaos, detectarMaos, fecharDetector
from duasmaos import ControleDuasMaos
from janela import JanelaCamera

pyautogui.PAUSE = 0


def abrirWebcam():
    webcam = cv2.VideoCapture(INDICE_CAMERA)

    if not webcam.isOpened():
        print("Nao foi possivel abrir a camera")
        return None

    return webcam


def lerQuadro(webcam):
    leuImagem, quadro = webcam.read()

    if not leuImagem:
        print("Erro ao capturar imagem")
        return None

    return cv2.flip(quadro, 1)


def ladoDaMaoSecundaria():
    return "Left" if MAO_DO_CURSOR == "Right" else "Right"


def processarMaoDoCursor(maosEncontradas, cursor, atalhos, janela, quadro):
    if MAO_DO_CURSOR not in maosEncontradas:
        cursor.maoSumiu()
        return

    alturaImagem, larguraImagem, _ = quadro.shape

    texto, cor = cursor.controlar(
        maosEncontradas[MAO_DO_CURSOR].landmark,
        larguraImagem,
        alturaImagem,
        atalhos.pausado,
    )
    janela.escreverTexto(quadro, f"Cursor: {texto}", (20, 40), cor)


def processarMaoSecundaria(maosEncontradas, atalhos, janela, quadro):
    lado = ladoDaMaoSecundaria()

    if lado not in maosEncontradas:
        atalhos.maoSumiu()
        return

    texto, cor = atalhos.controlar(maosEncontradas[lado].landmark)
    janela.escreverTexto(quadro, f"Atalhos: {texto}", (20, 75), cor)


def processarDuasMaos(maosEncontradas, duasMaos, cursor, atalhos, janela, quadro):
    if atalhos.pausado:
        duasMaos.zerar()
        return False

    resultado = duasMaos.controlar(maosEncontradas)

    if resultado is None:
        return False

    # enquanto o gesto das duas maos esta ativo, cursor e atalhos ficam parados
    cursor.maoSumiu()
    atalhos.maoSumiu()

    texto, cor = resultado
    janela.escreverTexto(quadro, texto, (20, 40), cor)
    return True


def iniciar():
    webcam = abrirWebcam()

    if webcam is None:
        fecharDetector()
        return

    cursor = ControleCursor()
    atalhos = ControleAtalhos()
    duasMaos = ControleDuasMaos()
    janela = JanelaCamera()

    try:
        while True:
            quadro = lerQuadro(webcam)

            if quadro is None:
                break

            quadroRGB = cv2.cvtColor(quadro, cv2.COLOR_BGR2RGB)
            maosEncontradas = detectarMaos(quadroRGB)

            desenharMaos(quadro, maosEncontradas)

            if not processarDuasMaos(maosEncontradas, duasMaos, cursor, atalhos, janela, quadro):
                processarMaoDoCursor(maosEncontradas, cursor, atalhos, janela, quadro)
                processarMaoSecundaria(maosEncontradas, atalhos, janela, quadro)

            janela.atualizar(quadro, atalhos.cameraVisivel)

            if janela.pediuParaSair():
                break

    finally:
        cursor.soltarTudo()
        atalhos.soltarTudo()
        webcam.release()
        fecharDetector()
        janela.encerrar()


if __name__ == "__main__":
    iniciar()
