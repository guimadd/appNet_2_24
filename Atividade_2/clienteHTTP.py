from urllib import request

def requisitar_pagina_inicial():
    url = "http://localhost:8080/"
    resposta = request.urlopen(url)
    conteudo = resposta.read().decode("utf-8")
    with open("pagina_inicial.txt", "w", encoding="utf-8") as arquivo:
        arquivo.write(conteudo)
    print("Conteúdo da página inicial salvo em 'pagina_inicial.txt'.")

if __name__ == "__main__":
    requisitar_pagina_inicial()