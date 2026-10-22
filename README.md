# Controlador de Mouse por Gestos

Controle o mouse do computador usando apenas as mãos na frente da webcam. Uma mão move o cursor e faz os cliques, a outra cuida de rolagem, zoom e atalhos.

Projeto **open source**: o código é aberto e você pode usar, estudar, modificar e distribuir à vontade.

## Recursos

- Controle do cursor com uma mão, com movimento suavizado
- Clique esquerdo (com arrastar), clique direito e clique duplo por gestos de pinça
- Rolagem, zoom, troca de janela e voltar/avançar com a outra mão
- Pausa e retomada do controle por gesto
- Janela da câmera que pode ser mostrada ou escondida por gesto
- Gestos medidos em proporção ao tamanho da mão, então funcionam perto ou longe da câmera
- Código dividido em módulos pequenos e fáceis de entender

## Tecnologias

- [Python](https://www.python.org/)
- [OpenCV](https://opencv.org/) para captura e exibição da câmera
- [MediaPipe](https://developers.google.com/mediapipe) para detecção das mãos
- [PyAutoGUI](https://pyautogui.readthedocs.io/) para controlar mouse e teclado

## Instalação

1. Tenha o Python instalado, em uma versão compatível com o MediaPipe 0.10.21.
2. Coloque os arquivos do projeto em uma pasta.
3. Instale as dependências:

```bash
pip install opencv-python mediapipe==0.10.21 pyautogui
```

## Como usar

Dentro da pasta do projeto, rode:

```bash
python principal.py
```

A janela da câmera abre por cima das outras. Mostre as mãos para a câmera e use os gestos abaixo.

Para fechar o programa, aperte `q` com a janela da câmera em foco, ou use `Ctrl+C` no terminal.

## Gestos

Por padrão, a **mão direita** controla o cursor e a **mão esquerda** controla os atalhos. Isso pode ser trocado nas configurações.

### Mão do cursor

| Gesto | Ação |
|---|---|
| Mover a mão | Move o cursor |
| Pinça polegar + indicador | Clique esquerdo (segure para arrastar) |
| Pinça polegar + médio | Clique direito |
| Pinça polegar + anelar | Clique duplo |

### Mão dos atalhos

| Gesto | Ação |
|---|---|
| Indicador + médio levantados, mover para cima ou para baixo | Rolagem |
| Pinça polegar + indicador, mover para cima ou para baixo | Zoom (Ctrl + rolagem) |
| Indicador + médio + anelar levantados | Alt + Tab |
| Palma aberta, deslizar rápido para os lados | Voltar ou avançar (Alt + seta) |
| Polegar + mindinho (shaka) | Mostrar ou esconder a câmera |
| Punho fechado por 1 segundo | Pausar ou retomar o controle |

Com o controle pausado, o cursor e os atalhos ficam parados. O punho (para retomar) e o shaka continuam funcionando.

## Configurações

Todas ficam em `configuracoes.py`:

| Configuração | O que faz |
|---|---|
| `MAO_DO_CURSOR` | Qual mão move o cursor (`"Right"` ou `"Left"`) |
| `SENSIBILIDADE` | Velocidade do cursor |
| `SUAVIZACAO` | Suavidade do movimento (menor = mais suave) |
| `LIMITE_PINCA` | Quão fechada a pinça precisa estar para contar como clique |
| `VELOCIDADE_ROLAGEM` | Velocidade da rolagem |
| `VELOCIDADE_ZOOM` | Velocidade do zoom |
| `MOVIMENTO_MINIMO` | Ignora tremidas pequenas na rolagem e no zoom |
| `VELOCIDADE_DESLIZE` | Velocidade necessária para o gesto de voltar/avançar |
| `TEMPO_PARA_PAUSAR` | Segundos com o punho fechado para pausar |
| `TEMPO_ENTRE_ATALHOS` | Intervalo mínimo entre atalhos repetidos |
| `INDICE_CAMERA` | Qual câmera usar (0 é a padrão) |
| `CONFIANCA_DETECCAO` | Confiança mínima do MediaPipe para detectar as mãos |

## Estrutura do projeto

| Arquivo | Responsabilidade |
|---|---|
| `principal.py` | Laço principal que junta tudo |
| `configuracoes.py` | Constantes e ajustes |
| `detector.py` | Detecção das mãos com MediaPipe e cálculos de pinça e dedos |
| `cursor.py` | Movimento do cursor e cliques |
| `atalhos.py` | Rolagem, zoom, atalhos, pausa e câmera |
| `janela.py` | Janela da câmera e tecla de saída |

## Dicas

- Use uma boa iluminação e um fundo sem muita bagunça.
- Deixe as duas mãos visíveis e evite que se sobreponham.
- Se o cursor estiver sendo controlado pela mão errada, troque `MAO_DO_CURSOR`.
- Se os cliques disparam sem querer, diminua `LIMITE_PINCA`. Se não disparam, aumente.
- Se o cursor treme, diminua `SUAVIZACAO` ou `SENSIBILIDADE`.

## Limitações

- O gesto de mostrar a janela da câmera sempre por cima funciona no Windows. Em outros sistemas pode não ter efeito.
- O atalho de voltar/avançar usa Alt + seta, comum em navegadores.
- Com a câmera escondida, a tecla `q` não funciona, pois não há janela em foco. Mostre a câmera de novo ou use `Ctrl+C`.
- O PyAutoGUI tem uma proteção: levar o mouse a um canto da tela interrompe o programa.

## Contribuindo

Contribuições são bem-vindas. Você pode abrir issues com bugs e ideias, ou enviar melhorias de código, novos gestos e correções na documentação.

## Licença

Este é um projeto open source. O código é livre para uso, estudo, modificação e distribuição.
