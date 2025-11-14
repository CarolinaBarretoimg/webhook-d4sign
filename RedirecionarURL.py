from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# Pegamos a URL longa do Power Automate via variável de ambiente:
POWER_AUTOMATE_URL = os.getenv("FLOW_URL")


@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        data = request.get_json(force=True)

        # Reenvia o JSON recebido diretamente para o Power Automate
        response = requests.post(POWER_AUTOMATE_URL, json=data)

        return jsonify({
            "proxy_status": "forwarded",
            "flow_status": response.status_code
        }), response.status_code

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/", methods=["GET"])
def root():
    return jsonify({"message": "Proxy ativo. Use /webhook para POST."})
