from flask import Flask, render_template, request, send_file
import os
from utils.subdomain import enumerate_subdomains
from utils.portscan import scan_ports
from utils.encryptor import generate_key, encrypt_data, decrypt_data
from utils.stego import encode_message, decode_message

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    result = ""
    if request.method == "POST":
        action = request.form.get("action")

        if action == "subdomain":
            domain = request.form.get("domain")
            result = "\n".join(enumerate_subdomains(domain))

        elif action == "portscan":
            target = request.form.get("target")
            ports = scan_ports(target)
            result = "\n".join(ports) if ports else "No ports found."

        elif action == "encrypt":
            message = request.form.get("message")
            key = generate_key()
            encrypted = encrypt_data(message, key)
            result = f"Encrypted Message:\n{encrypted.decode()}\n\nKey:\n{key.decode()}"

        elif action == "decrypt":
            enc_message = request.form.get("enc_message")
            enc_key = request.form.get("enc_key")
            try:
                plaintext = decrypt_data(enc_message.encode(), enc_key.encode())
                result = f"Decrypted Message:\n{plaintext}"
            except Exception as e:
                result = f"Decryption failed: {e}"

        elif action == "hide":
            file = request.files["image"]
            msg = request.form.get("msg_to_hide")
            image_path = os.path.join(UPLOAD_FOLDER, file.filename)
            output_path = os.path.join(UPLOAD_FOLDER, "stego.png")
            file.save(image_path)
            try:
                encode_message(image_path, msg, output_path)
                return send_file(output_path, as_attachment=True)
            except Exception as e:
                result = f"Error: {e}"

        elif action == "extract":
            file = request.files["stego_image"]
            image_path = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(image_path)
            try:
                message = decode_message(image_path)
                result = f"Extracted Message:\n{message}"
            except Exception as e:
                result = f"Error: {e}"

    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)