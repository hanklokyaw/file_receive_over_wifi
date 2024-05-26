from flask import Flask, request, redirect, url_for, flash, jsonify, render_template, send_from_directory
from werkzeug.utils import secure_filename
import os
import qrcode
import socket
from PIL import Image

app = Flask(__name__)
app.secret_key = 'supersecretkey'
io_port = 5000

# Configure upload folder and allowed extensions
UPLOAD_FOLDER = 'receive'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'mp4', 'mov', 'csv', 'xls', 'xlsx', 'ppt'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload')
def upload_form():
    return render_template('upload.html')

@app.route('/download')
def download_form():
    # Get the list of files in the 'receive' directory
    files = os.listdir('send')
    return render_template('download.html', files=files)

@app.route('/upload', methods=['POST'])
def upload_files():
    if 'files' not in request.files:
        flash('No file part')
        return redirect(url_for('upload_form'))

    files = request.files.getlist('files')
    if not files or all(file.filename == '' for file in files):
        flash('No selected file')
        return redirect(url_for('upload_form'))

    for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    return jsonify({'message': 'Files successfully uploaded'})

@app.route('/download/<filename>')
def download_file(filename):
    # Serve the selected file for download
    return send_from_directory('send', filename)

def generate_qr_code(url):
    # Generate a QR code for the given URL
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(fill='black', back_color='white')
    img_path = 'qr_code.png'
    img.save(img_path)
    return img_path

def print_ip_address(port):
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    io_url = f"http://{local_ip}:{port}"
    return io_url


if __name__ == '__main__':
    io_ip_address = print_ip_address(io_port)
    # print(f"Server is running on {io_ip_address}")
    qr_code_file_path = generate_qr_code(io_ip_address)
    os.startfile(qr_code_file_path)
    app.run(debug=True, host='0.0.0.0', port=io_port)
