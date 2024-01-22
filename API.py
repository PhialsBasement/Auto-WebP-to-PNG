from flask import Flask, request, jsonify
from PIL import Image
from io import BytesIO

app = Flask(__name__)

def convert_webp_to_png(webp_data):
    try:
        with Image.open(BytesIO(webp_data)) as img:
            # Convert the image to PNG format
            png_data = BytesIO()
            img.save(png_data, format='PNG')
            return png_data.getvalue()
    except Exception as e:
        return f"Error: {str(e)}"


@app.route('/convert', methods=['POST'])
def convert_image():
    if 'image' not in request.files:
        return jsonify({"error": "No image provided"}), 400

    webp_file = request.files['image']
    if webp_file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if webp_file and webp_file.filename.endswith('.webp'):
        webp_data = webp_file.read()
        png_data = convert_webp_to_png(webp_data)
        if isinstance(png_data, bytes):
            return jsonify({"png_data": png_data.decode('latin-1')})
        else:
            return jsonify({"error": png_data}), 500
    else:
        return jsonify({"error": "Invalid file format. Please provide a WebP image"}), 400


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
