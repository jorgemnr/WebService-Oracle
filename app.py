# coding:utf-8
#!/usr/bin/env python

import json
import requests
from flask import Flask, request

# Ler credencial
from config import config


# Iniciar aplicativo
app = Flask(__name__)

# *************************
# Ambiente execução
# *************************
app.config["ambiente"] = "prd"
# *************************

# Configurações
if app.config["ambiente"] == "hom":
    # Proxy
    app.config["userproxy"] = config["userproxy"]
    app.config["proxy"] = {
        "http": app.config["userproxy"],
        "https": app.config["userproxy"],
    }
    # SSL
    app.config["verificarSSL"] = False
else:
    # Proxy
    app.config["proxy"] = ""
    # SSL
    app.config["verificarSSL"] = True

# Time-out
app.config["timeout"] = 30


# Rota para auto teste
@app.route("/", methods=["GET", "POST"])
def rota():
    status = {}
    try:
        # Serviço no ar
        status["1/2 - Conexao interna http"] = "Funcionando"

        # Testar proxy/saida
        response = requests.request(
            method="GET",
            url="https://jsonplaceholder.typicode.com/todos/1",
            headers={"Content-type": "application/json"},
            proxies=app.config["proxy"],
            verify=app.config["verificarSSL"],
            timeout=app.config["timeout"],
        )

        # Verifica se a requisição foi bem-sucedida
        response.raise_for_status()

        # retorno
        status["2/2 - Conexao externa https"] = "Funcionando"

    except Exception as MsgError:
        status["2/2 - Conexao externa https"] = str(MsgError)
    #
    return status


# Rota principal
@app.route("/consomews", methods=["GET", "POST", "PUT", "PATCH"])
def servico():
    status = ""
    ds_erro = ""
    try:
        # url https
        ds_erro = "GET url: "
        url = request.headers.get("url")

        # Headers
        ds_erro = "GET headers: "
        headers = request.headers.get("headers")

        ds_erro = "JSON headers: "
        headers = json.loads(headers)

        # dados do POST
        # if not response.headers.get('content-type').startswith("application/json")
        ds_erro = "DATA: "
        body = request.data
        # body =json.loads(request.data)

        # Efetuar request
        ds_erro = "REQUEST: "
        response = requests.request(
            method=request.method,
            url=url,
            data=body,
            headers=headers,
            proxies=app.config["proxy"],
            verify=app.config["verificarSSL"],
            timeout=app.config["timeout"],
        )

        # Verifica se a requisição foi bem-sucedida
        ds_erro = "Processar REQUEST: "
        response.raise_for_status()

        # Supondo que a resposta é um JSON
        ds_erro = "JSON retorno: "
        status = response.json()

        # retorno = retorno.decode("iso-8859-1")

    except Exception as MsgError:
        # status = "Erro: " + str(MsgError)
        status = "Erro - " + ds_erro + str(MsgError)
    #
    return status


if __name__ == "__main__":
    # app.run(host='apihml.seara.com.br', port = 5000, debug=True)
    # app.run(host="0.0.0.0", port=8888, debug=True)
    app.run(host="0.0.0.0", port=8888)
