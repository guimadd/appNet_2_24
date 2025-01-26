# Protocolos de Sincronização de Tempo: Implementação de NTP e Algoritmo de Berkeley

## Índice

- [Introdução](#introdução)
- [Recursos](#recursos)
- [Tecnologias Utilizadas](#tecnologias-utilizadas)
- [Instalação](#instalação)
- [Dicas](#Dicas)

## Introdução

A sincronização de tempo é crucial em sistemas distribuídos para garantir consistência e coordenação entre múltiplos dispositivos. Este projeto implementa dois protocolos fundamentais de sincronização de tempo:

1. **Network Time Protocol (NTP):** Um protocolo amplamente utilizado projetado para sincronizar os relógios de computadores em redes de dados com latência variável e comutadas por pacotes.
2. **Algoritmo de Berkeley:** Um método de sincronização adequado para redes locais, que centraliza a coordenação do tempo por meio de um servidor.

Este repositório fornece implementações em Python para o cliente NTP e para os componentes servidor e cliente do Algoritmo de Berkeley, juntamente com instruções para configuração e uso.

## Recursos

- **Cliente NTP:**
  - Sincroniza o tempo do sistema com servidores NTP públicos.
  - Calcula o atraso de ida e volta para melhorar a precisão.
  - Exibe o tempo sincronizado e métricas de atraso.

- **Algoritmo de Berkeley:**
  - Sincronização de tempo centralizada em uma rede local.
  - O servidor coleta o tempo de múltiplos clientes, calcula a média e distribui ajustes.
  - Os clientes ajustam seus relógios locais com base nas instruções do servidor.

## Tecnologias Utilizadas

- **Linguagem de Programação:** Python 3.x
- **Bibliotecas:**
  - `socket`: Para comunicações de rede.
  - `struct`: Para manipulação de dados binários.
  - `time` e `datetime`: Para operações relacionadas ao tempo.
  - `pytz`: Para manipulação de fusos horários (Algoritmo de Berkeley).

## Instalação

1. **Clonar o Repositório:**
   ```bash
   git clone https://github.com/guimadd/appNet_2_24.git
   cd AV2



## Dicas
Comando para saber minha posição geográfica:
 ```bash
curl ipinfo.io
 ```
Comando para saber a hora local:
 ```
date
