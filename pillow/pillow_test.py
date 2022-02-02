from PIL import Image
from flask import Flask, render_template, request, send_file
from werkzeug.utils import secure_filename
from pillow_ext import EXTENSIONS


UPLOAD_FOLDER = 'static'


app = Flask(__name__)


def rotate_img(filename, flag):
    file_path = f'{UPLOAD_FOLDER}\\{filename}'
    img = Image.open(file_path)
    if flag == 'left':
        img = img.transpose(Image.ROTATE_90)
    elif flag == 'right':
        img = img.transpose(Image.ROTATE_270)
    elif flag == 'upend':
        img = img.transpose(Image.ROTATE_180)
    img.save(f'{UPLOAD_FOLDER}\\{filename}')


def check_ext(f_name):
    ext = f_name.split('.')[-1]
    return '.' in f_name and ext in EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        if not file:
            return render_template('index.html', msg='No file selected')
        if check_ext(file.filename):
            filename = secure_filename(file.filename)
            file.save(f'{UPLOAD_FOLDER}\\{filename}')
            return render_template('index.html', file=filename)
        else:
            return render_template('index.html', msg='File format is not supported')
    return render_template('index.html')


@app.route('/rotate/<filename>', methods=['GET', 'POST'])
def rotate(filename):
    if request.method == 'POST':
        rotate_img(filename, request.values.keys().pop())
    return render_template('index.html', file=filename)


@app.route('/download/<filename>')
def download(filename):
    download_path = f'{UPLOAD_FOLDER}\\{filename}'
    return send_file(download_path, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)

