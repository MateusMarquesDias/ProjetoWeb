import socket
import redis
import logging
from flask import Flask

app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379)

def get_ip():
    try:
        nome_host = socket.gethostname()
        endereco_ip = socket.gethostbyname(nome_host)
    except socket.gaierror:
        logging.error("Falha ao recuperar o endereço IP: Nome do host não pôde ser resolvido")
        endereco_ip = 'Não foi possível recuperar o endereço IP'
    except socket.error as e:
        logging.error(f"Ocorreu um erro de soquete: {e}")
        endereco_ip = 'Não foi possível recuperar o endereço IP'
    return endereco_ip

@app.route('/')
def hello():
    return get_ip()

if __name__ == "__main__":
    logging.basicConfig(level=logging.ERROR)
    app.run(host='0.0.0.0')
