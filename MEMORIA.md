# Banco de Memoria — Fortune Logica

Este arquivo guarda as decisoes principais do projeto para facilitar futuras alteracoes.

## Estado Atual

- O jogo roda no terminal pelo arquivo `fortune_logica.py`.
- A nova interface Pygame fica em `funcoes/interface_pygame.py` e deve ser testada separadamente.
- A interface grafica em Tkinter foi removida.
- A logica principal fica em `funcoes/logica.py`.
- O fluxo de jogo fica em `funcoes/jogo.py`.
- O saldo do jogador fica salvo em `saldo.txt`.

## Regras Do Jogo

- O jogador escolhe de 1 a 6 proposicoes.
- O jogador define uma aposta.
- O jogador monta manualmente a expressao.
- A expressao e escolhida antes do sorteio das proposicoes.
- Depois da montagem, o jogo mostra a probabilidade de a expressao dar verdadeiro e o multiplicador.
- Depois disso, o jogo sorteia `V` ou `F` para cada proposicao.
- Se a expressao final for verdadeira, o jogador ganha.
- Se a expressao final for falsa, o jogador perde a aposta.

## Jackpot

- Jackpot so acontece quando todas as proposicoes sorteadas forem `V` e a expressao final tambem for `V`.
- O bonus do jackpot usa a quantidade de proposicoes.
- Exemplo: com 3 proposicoes e multiplicador base `x2`, o bonus jackpot e `x3`, entao o multiplicador final vira `x6`.

## Multiplicador

- O multiplicador base vem da chance da expressao dar verdadeiro na tabela-verdade.
- Formula:

```text
multiplicador = total_de_linhas / linhas_verdadeiras
```

- Quanto menor a chance de uma expressao dar verdadeiro, maior o multiplicador.

## Operadores

- `E`: conjuncao.
- `OU`: disjuncao.
- `SE`: implicacao.
- `SSE`: bicondicional.
- `NAO`: negacao.

## Testes

Execute:

```bash
python -m unittest
```
