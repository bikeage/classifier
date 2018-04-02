"""This is a flask fron end for an image classifier, Resnet50 at first.
to be replaced with a custom neural net once I have the time.
"""
import os

from flask import Flask, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
from flask import send_from_directory

UPLOAD_FOLDER = 'static/uploads/'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'monkey'


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/eliot', methods=['GET', 'POST'])
def dummy():
    return render_template('index.html')


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file',
                                    filename=filename))
    return render_template('uploader.html')

#@app.route('/view', methods=['GET', 'POST'])
@app.route('/uploads/<filename>', methods=['GET', 'POST'])
def uploaded_file( filename ):
    return render_template('render_image.html', filename='/static/uploads/'+filename)
    #return send_from_directory(app.config['UPLOAD_FOLDER'],
    #                           filename)
