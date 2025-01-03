from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs

HOST = 'localhost'
PORTA = 8080

class MeuServidorHTTP(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            conteudo_html = '''
            <html>
              <head><title>Formulário</title></head>
              <body>
                <h1>Página Inicial</h1>
                <form method="POST" action="/">
                  <label>Nome:</label>
                  <input type="text" name="nome"><br><br>
                  <label>E-mail:</label>
                  <input type="email" name="email"><br><br>
                  <input type="submit" value="Enviar">
                </form>
              </body>
            </html>
            '''
            self.wfile.write(conteudo_html.encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path == '/':
            tamanho = int(self.headers.get('Content-Length', 0))
            corpo = self.rfile.read(tamanho).decode('utf-8')
            dados = parse_qs(corpo)
            nome = dados.get('nome', [''])[0]
            nome = nome.strip()
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            resposta_html = f'''
            <html>
              <head><title>Bem-vindo</title></head>
              <body>
                <h1>Seja bem vindo(a) {nome} ao nosso site!</h1>
              </body>
            </html>
            '''
            self.wfile.write(resposta_html.encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

def iniciar_servidor():
    servidor = HTTPServer((HOST, PORTA), MeuServidorHTTP)
    print(f"Servidor HTTP rodando em http://{HOST}:{PORTA}")
    servidor.serve_forever()

if __name__ == "__main__":
    iniciar_servidor()