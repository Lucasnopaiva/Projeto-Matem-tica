# Corrida Fake 3D

Este projeto e um jogo simples de corrida feito em Python com a biblioteca
`pygame`.

## O que voce precisa instalar

Antes de rodar o jogo, instale:

1. **Python**
   - Baixe em: https://www.python.org/downloads/
   - Durante a instalacao, marque a opcao **Add Python to PATH**.

2. **Pygame**
   - Depois de instalar o Python, abra o terminal dentro da pasta do projeto e
     rode:

```bash
pip install pygame
```

## Como abrir o terminal na pasta do projeto

No Windows:

1. Abra a pasta do projeto.
2. Clique na barra de endereco da pasta.
3. Digite `cmd` e aperte **Enter**.

Isso abre o terminal ja no lugar certo.

## Como rodar o jogo

Com o terminal aberto na pasta do projeto, rode:

```bash
python main.py
```

Se esse comando nao funcionar, tente:

```bash
py main.py
```

Uma janela do jogo deve abrir com o titulo **Corrida Fake 3D**.

## Controles

- **Seta para esquerda** ou **A**: move o carro para a esquerda.
- **Seta para direita** ou **D**: move o carro para a direita.
- **R**: reinicia o jogo depois do game over.
- **Fechar a janela**: encerra o jogo.

## Objetivo

Desvie dos cones e barreiras para continuar pontuando. Com o tempo, o jogo fica
mais rapido e a pista comeca a ter curvas.

## Erros comuns

### `python` nao e reconhecido

Isso geralmente significa que o Python nao foi adicionado ao PATH. Reinstale o
Python e marque a opcao **Add Python to PATH**, ou tente rodar:

```bash
py main.py
```

### `ModuleNotFoundError: No module named 'pygame'`

Esse erro significa que o `pygame` ainda nao foi instalado. Rode:

```bash
pip install pygame
```

Depois tente abrir o jogo novamente:

```bash
python main.py
```
