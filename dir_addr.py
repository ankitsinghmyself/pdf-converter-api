from flask import Flask

UPLOAD_FOLDER = '/tmp'
download_text_file = '/tmp'
app = Flask(__name__)
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DOWNLOAD_FOLDER'] = download_text_file
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024