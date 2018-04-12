"""classifier front end.

This is a flask fron end for an image classifier, Resnet50 at first.
to be replaced with a custom neural net once I have the time.
"""
import os

from flask_bootstrap import Bootstrap

from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
from img_rec import get_predictions

UPLOAD_FOLDER = 'static/uploads/'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'monkey'


def allowed_file(filename):
    # validated filenames
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

'''
@app.route('/eliot', methods=['GET', 'POST'])
def dummy():
    # dummy page for troubleshooting.
    if request.method == 'POST':
        #get_predictions('static/uploads/2014-05-31_08.16.21.jpg')
        return render_template('view_predictions.html')
    return render_template('index.html')
'''

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    # file uploader
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


@app.route('/<filename>', methods=['GET', 'POST'])
def uploaded_file(filename):
    # routes to a page to display the uploaded file.
    if request.method == 'POST':
        #get_predictions(UPLOAD_FOLDER+filename)
        preds = get_predictions(UPLOAD_FOLDER+filename)
        print(preds)
        return render_template('view_predictions.html',
                               prediction =preds,
                               filename=UPLOAD_FOLDER+filename)
    return render_template('render_image.html',
                           filename=UPLOAD_FOLDER+filename)


@app.route('/<filename>', methods=['GET', 'POST'])
def display_predictions(filename, preds):
    return render_template('view_predictions.html')


if __name__ == "__main__":
    app.run()
