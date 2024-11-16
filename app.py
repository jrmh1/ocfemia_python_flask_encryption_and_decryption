from flask import Flask, request, jsonify
from cryptography.fernet import Fernet

app = Flask(__name__)

key = Fernet.generate_key()
cipher_suite = Fernet(key)


@app.route('/encrypt', methods=['POST'])
def encrypt_data():
    data = request.get_json()
    text = data.get('text')
    if not text:
        return jsonify({'error': 'No text provided'}), 400

    encrypted_text = cipher_suite.encrypt(text.encode())  # Encrypt the text
    return jsonify({'encrypted_text': encrypted_text.decode()}), 200


@app.route('/decrypt', methods=['POST'])
def decrypt_data():
    data = request.get_json()
    encrypted_text = data.get('encrypted_text')
    if not encrypted_text:
        return jsonify({'error': 'No encrypted_text provided'}), 400

    try:
        decrypted_text = cipher_suite.decrypt(encrypted_text.encode()).decode()
        return jsonify({'decrypted_text': decrypted_text}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400


if __name__ == '__main__':
    app.run(debug=True)