# Fortune Logica

Jogo educativo em Python para praticar logica proposicional no terminal com uma estetica de jackpot.

## Como jogar

Execute no terminal:

```bash
python fortune_logica.py
```

Para testar a nova interface Pygame em tela unica, instale as dependencias e rode:

```bash
pip install -r requirements.txt
python -m funcoes.interface_pygame
```

O jogador comeca com 100 moedas, escolhe de 1 a 6 proposicoes, define uma aposta e monta uma expressao antes de ver os valores sorteados usando:

- `E`
- `OU`
- `SE`
- `SSE`
- `NAO`

Depois disso, o jogo sorteia os valores `V` ou `F` e avalia a expressao. O multiplicador e calculado pela tabela-verdade da expressao: quanto menor a chance de ela dar verdadeiro, maior o premio.

Exemplo: se uma expressao tem chance de 50%, o multiplicador de retorno e `x2`. Em uma aposta de 10 moedas, ganhar em `x2` significa retorno total de 20 moedas, entao o lucro somado ao saldo e de 10 moedas.

O jackpot acontece somente quando todas as proposicoes sorteadas caem como `V` e a expressao final tambem resulta em `V`. Nesse caso, o multiplicador da expressao recebe um bonus pela dificuldade de cair. Esse bonus usa a quantidade de proposicoes: com 2 proposicoes, o bonus e `x2`; com 3, `x3`; com 6, `x6`.

O saldo fica salvo no arquivo `saldo.txt`, criado automaticamente na primeira vez que o jogo roda.

Antes do sorteio, o jogador monta a propria expressao. Depois da montagem, o jogo mostra a probabilidade de a expressao dar verdadeiro e o multiplicador.

As principais decisoes do projeto ficam registradas em `MEMORIA.md`.

## Testes

Execute:

```bash
python -m unittest
```

## Estrutura

- `fortune_logica.py`: arquivo principal para iniciar o jogo.
- `funcoes/`: pasta com as funcoes de entrada, interface de terminal, logica e fluxo do jogo.
- `saldo.txt`: arquivo criado automaticamente para guardar o dinheiro virtual.
- `MEMORIA.md`: banco de memoria com regras e decisoes do projeto.
