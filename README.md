# Fortune Logica

Jogo educativo em Python para praticar logica proposicional com uma estetica de jackpot.

## Como jogar

Execute no terminal:

```bash
python fortune_logica.py
```

O jogador comeca com 100 moedas, escolhe de 1 a 6 proposicoes, define uma aposta e monta uma expressao antes de ver os valores sorteados usando:

- `E`
- `OU`
- `SE`
- `SSE`
- `NAO`

Depois disso, o jogo sorteia os valores `V` ou `F` e avalia a expressao. O multiplicador e calculado pela tabela-verdade da expressao: quanto menor a chance de ela dar verdadeiro, maior o premio.

Exemplo: se uma expressao tem chance de 50%, o multiplicador de retorno e `x2`. Em uma aposta de 10 moedas, ganhar em `x2` significa retorno total de 20 moedas, entao o lucro somado ao saldo e de 10 moedas.

Quando acontece jackpot, o multiplicador da expressao recebe um bonus pela dificuldade de cair. Esse bonus usa a quantidade de proposicoes: com 2 proposicoes, o bonus e `x2`; com 3, `x3`; com 6, `x6`.

O saldo fica salvo no arquivo `saldo.txt`, criado automaticamente na primeira vez que o jogo roda.

Antes do sorteio, o jogo tambem mostra expressoes aleatorias sugeridas com a chance e o multiplicador de cada uma. O jogador pode escolher uma sugestao ou montar a propria expressao.

## Testes

Execute:

```bash
python -m unittest
```

## Estrutura

- `fortune_logica.py`: arquivo principal para iniciar o jogo.
- `funcoes/`: pasta com as funcoes de entrada, interface, logica e fluxo do jogo.
- `saldo.txt`: arquivo criado automaticamente para guardar o dinheiro virtual.
