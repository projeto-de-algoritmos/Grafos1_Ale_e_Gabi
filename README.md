# Projeto e Análise de Algoritimos - Grafos 1 

**Alunos:**  
* Gabriela Guedes - 16/0121612
* Alexandre Miguel - 16/0000840

## Configurações
O projeto forma grafos com informações da API do Twitter, para poder rodar o projeto é necessário ter uma conta no twitter e cadastra-la como [developer](https://developer.twitter.com/). Após ter sua conta na Twitter Developer, é necessário [criar um App](https://developer.twitter.com/en/apps/create).

Com o App criado, renomeie o arquivo `example_tokens.py` para `tokens.py` e coloque os tokens do seu App no lugar indicado.

## Instalação
O projeto utiliza das bibliotecas `plotly` e `networkx` para a visualização dos grafos. Para instalar as bibliotecas rode os comandos:
``` sh
pip install plotly
pip install networkx
```
Além da plotly o projeto também utiliza da biblioteca `requests` para fazer as requisições para a API do Twitter. Para instalar rode o comando:
``` sh
pip install requests
```

## Como rodar o projeto
Após ter todas as bibliotecas instaladas rode o projeto com o comando:
```sh
python twitterGraph.py
```
**Observação:** O projeto é feito em Python3
