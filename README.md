# Protocolos de Sincronização de Tempo: Implementação de NTP e Algoritmo de Berkeley

## Índice

- [Introdução](#introdução)
- [Recursos](#recursos)
- [Tecnologias Utilizadas](#tecnologias-utilizadas)
- [Instalação](#instalação)
- [Uso](#uso)
  - [Cliente Network Time Protocol (NTP)](#cliente-network-time-protocol-ntp)
  - [Algoritmo de Berkeley](#algoritmo-de-berkeley)
    - [Servidor Berkeley](#servidor-berkeley)
    - [Cliente Berkeley](#cliente-berkeley)
- [Exemplos](#exemplos)
- [Resultados e Demonstrações](#resultados-e-demonstrações)
- [Contribuindo](#contribuindo)
- [Licença](#licença)

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
   git clone https://github.com/seuusuario/protocolos-sincronizacao-tempo.git
   cd protocolos-sincronizacao-tempo



# Trabalho
# Comando para saber minha posição geográfica:
# curl ipinfo.io
# Comando para saber a hora local:
# date
