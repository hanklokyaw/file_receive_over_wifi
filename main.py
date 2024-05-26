# from flask import Flask, request, redirect, url_for, flash, jsonify, render_template, send_from_directory
# from werkzeug.utils import secure_filename
# import os
#
# app = Flask(__name__)
# app.secret_key = 'supersecretkey'
#
# # Configure upload folder and allowed extensions
# UPLOAD_FOLDER = 'uploads'
# ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'mp4', 'mov'}
#
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
#
# if not os.path.exists(UPLOAD_FOLDER):
#     os.makedirs(UPLOAD_FOLDER)
#
# def allowed_file(filename):
#     return '.' in filename and \
#            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
#
# @app.route('/')
# def upload_form():
#     return render_template('index.html')
#
# @app.route('/upload', methods=['POST'])
# def upload_files():
#     if 'files' not in request.files:
#         flash('No file part')
#         return redirect(url_for('upload_form'))
#
#     files = request.files.getlist('files')
#     if not files or all(file.filename == '' for file in files):
#         flash('No selected file')
#         return redirect(url_for('upload_form'))
#
#     for file in files:
#         if file and allowed_file(file.filename):
#             filename = secure_filename(file.filename)
#             file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#
#     return jsonify({'message': 'Files successfully uploaded'})
#
# @app.route('/download')
# def index():
#     # Get the list of files in the 'uploads' directory
#     files = os.listdir('uploads')
#     return render_template('download.html', files=files)
#
# @app.route('/download/<filename>')
# def download_file(filename):
#     # Serve the selected file for download
#     return send_from_directory('uploads', filename)
#
# if __name__ == '__main__':
#     app.run(debug=True, host='0.0.0.0', port=5000)




from flask import Flask, request, redirect, url_for, flash, jsonify, render_template, send_from_directory
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Configure upload folder and allowed extensions
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'mp4', 'mov'}

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
    # Get the list of files in the 'uploads' directory
    files = os.listdir('uploads')
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
    return send_from_directory('uploads', filename)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
