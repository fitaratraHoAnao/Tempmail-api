from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

# Route pour générer un email temporaire
@app.route('/generate', methods=['GET'])
def generate_temp_mail():
    response = requests.get('https://www.1secmail.com/api/v1/?action=genRandomMailbox&count=1')
    
    if response.status_code == 200:
        email = response.json()[0]
        return jsonify({"tempmail": email}), 200
    else:
        return jsonify({"error": "Unable to generate email"}), 500

# Route pour vérifier la boîte de réception
@app.route('/check', methods=['GET'])
def check_inbox():
    # Récupérer l'email depuis les paramètres d'URL (par exemple : ?inbox=wnix4h24a@dpptd.com)
    email = request.args.get('inbox')
    
    if not email:
        return jsonify({"error": "Email is required"}), 400

    # Extraire le login et le domaine de l'email
    try:
        login, domain = email.split('@')
    except ValueError:
        return jsonify({"error": "Invalid email format"}), 400

    # Appel à l'API pour vérifier la boîte de réception
    inbox_url = f'https://www.1secmail.com/api/v1/?action=getMessages&login={login}&domain={domain}'
    response = requests.get(inbox_url)
    
    if response.status_code == 200:
        inbox = response.json()
        return jsonify({"inbox": inbox}), 200
    else:
        return jsonify({"error": "Unable to check inbox"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
  
