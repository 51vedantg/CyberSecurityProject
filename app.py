from flask import Flask, render_template, jsonify, send_from_directory
import subprocess
import os

app = Flask(__name__, static_folder='static')

# Home route that serves the index.html page
@app.route('/')
def home():
    return render_template('index.html')

# Route to run the recovery script using PowerShell as Administrator
@app.route('/run-script')
def run_script():
    try:
        script_path = r"C:\\Users\\vedan\\CyberSecurity-Project\\dataRecovery.py"
        command = f"powershell -Command \"Start-Process python -ArgumentList '{script_path}' -Verb runAs\""
        result = subprocess.run(command, shell=True, capture_output=True, text=True)

        if result.stderr:
            return f"❌ Failed to run script: {result.stderr}"

        return "✅ Recovery Complete. Check your Images folder!"
    except Exception as e:
        return f"❌ Unexpected error: {str(e)}"

# Route to return list of recovered images
@app.route('/get-images')
def get_images():
    image_folder = os.path.join(os.path.expanduser("~"), "Images")
    if not os.path.exists(image_folder):
        return jsonify([])

    files = [f for f in os.listdir(image_folder) if f.lower().endswith('.jpg')]
    return jsonify(files)

# Serve the recovered images from the Images folder
@app.route('/Images/<path:filename>')
def serve_image(filename):
    image_folder = os.path.join(os.path.expanduser("~"), "Images")
    return send_from_directory(image_folder, filename)

if __name__ == '__main__':
    app.run(debug=True)
