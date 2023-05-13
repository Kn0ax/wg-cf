import os
from flask import Flask, redirect, render_template, request, send_file
from werkzeug.middleware.proxy_fix import ProxyFix
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = './up'  # Change this to the path where you want to save uploaded files
ALLOWED_EXTENSIONS = {'conf'}  # Only allow .conf files to be uploaded


def allowed_file(filename):
  return '.' in filename and filename.rsplit(
    '.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return redirect("https://repl.it/@kn0ax/wg-cf")

@app.route('/wg')
def guide():
    filename = request.args.get('')
    return render_template('index.html', filename=secure_filename(filename))

@app.route('/upload', methods=['POST'])
def upload_file():
  # Check if the POST request contains a file and it's a .conf file
  if 'file' not in request.files or not allowed_file(
      request.files['file'].filename):
    return f'Invalid file\n', 400

  # Save the file to disk with a 4-digit filename and .conf extension
  file = request.files['file']
  filename = f"{os.urandom(2).hex()}"
  filen = f"{filename}.conf"
  file.save(os.path.join(UPLOAD_FOLDER, filen))

  return f'https://kn0.dev/wg?={filename}\n', 200

@app.route('/config')
def download_file():
    # Get the filename from the URL parameter
    filename = request.args.get('')
    # Check if the file exists and return it for download
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    if os.path.exists(filepath):
        response = send_file(filepath, as_attachment=True)
        # Delete the file after it has been sent for download
        os.remove(filepath)
        return response, 200
    else:
        return 'File not found', 404

app.wsgi_app = ProxyFix(
    app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1
)