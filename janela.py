import cv2

from configuracoes import (
    ALTURA_JANELA,
    LARGURA_JANELA,
    NOME_JANELA,
    TECLA_PARA_SAIR,
)


class JanelaCamera:
    def __init__(self):
        self.aberta = False

    def abrir(self, quadro):
        cv2.namedWindow(NOME_JANELA, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(NOME_JANELA, LARGURA_JANELA, ALTURA_JANELA)
        cv2.imshow(NOME_JANELA, quadro)
        cv2.setWindowProperty(NOME_JANELA, cv2.WND_PROP_TOPMOST, 1)
        self.aberta = True

    def fechar(self):
        cv2.destroyWindow(NOME_JANELA)
        self.aberta = False

    def atualizar(self, quadro, visivel):
        if visivel and not self.aberta:
            self.abrir(quadro)
        elif visivel:
            cv2.imshow(NOME_JANELA, quadro)
        elif self.aberta:
            self.fechar()

    def escreverTexto(self, quadro, texto, posicao, cor):
        cv2.putText(quadro, texto, posicao, cv2.FONT_HERSHEY_SIMPLEX, 0.7, cor, 2)

    def pediuParaSair(self):
        return cv2.waitKey(1) & 0xFF == ord(TECLA_PARA_SAIR)

    def encerrar(self):
        cv2.destroyAllWindows()
