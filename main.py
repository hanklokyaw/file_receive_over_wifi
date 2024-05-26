from flask import Flask, request, redirect, url_for, flash, jsonify, render_template, send_from_directory
from werkzeug.utils import secure_filename
import os
import qrcode
import socket

# Function to generate a QR code image for a given URL
def generate_qr_code(url):
    """
    Generate a QR code image for the given URL.

    Parameters:
        url (str): The URL to encode in the QR code.

    Returns:
        str: The file path of the generated QR code image.
    """
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

# Function to print the IP address and port for the server
def print_ip_address(port):
    """
    Print the IP address and port for the server.

    Parameters:
        port (int): The port number for the server.

    Returns:
        str: The URL of the server.
    """
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    io_url = f"http://{local_ip}:{port}"
    return io_url

# Function to run the Flask server
def run_flask_server(port):
    """
    Run the Flask server.

    Parameters:
        port (int): The port number for the server.
    """
    io_ip_address = print_ip_address(port)
    qr_code_file_path = generate_qr_code(io_ip_address)
    os.startfile(qr_code_file_path)
    app.run(debug=True, host='0.0.0.0', port=port)

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Configure upload folder and allowed extensions
UPLOAD_FOLDER = 'receive'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'mp4', 'mov', 'csv', 'xls', 'xlsx', 'ppt'}
IO_PORT = 5000

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Function to check if a file has an allowed extension
def allowed_file(filename):
    """
    Check if a file has an allowed extension.

    Parameters:
        filename (str): The name of the file.

    Returns:
        bool: True if the file has an allowed extension, False otherwise.
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Route for the home page
@app.route('/')
def index():
    return render_template('index.html')

# Route for the upload form page
@app.route('/upload')
def upload_form():
    return render_template('upload.html')

# Route for the download form page
@app.route('/download')
def download_form():
    # Get the list of files in the 'receive' directory
    files = os.listdir('send')
    return render_template('download.html', files=files)

# Route for uploading files
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

# Route for downloading files
@app.route('/download/<filename>')
def download_file(filename):
    # Serve the selected file for download
    return send_from_directory('send', filename)

# Main entry point of the application
if __name__ == '__main__':
    run_flask_server(IO_PORT)
