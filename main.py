from flask import Flask, render_template, request, redirect, url_for, session
import os
import image_read as image_read
from quote_finder import QuoteFinder
from werkzeug.utils import secure_filename
import time
from flask_bootstrap import Bootstrap
from flask_dropzone import Dropzone
from config import Config 

app = Flask(__name__)
app.config.from_object(Config())
bootstrap = Bootstrap(app)
dropzone = Dropzone(app)
app.config.update(
    UPLOADED_PATH='static/images',
    # Flask-Dropzone config:
    DROPZONE_ALLOWED_FILE_TYPE='image',
    DROPZONE_MAX_FILE_SIZE=5,
    DROPZONE_MAX_FILES=1,
    DROPZONE_REDIRECT_VIEW='quote_output'
)

app.secret_key = b'A_SECRET_KEY'
# DROPZONE_IN_FORM=True,
# DROPZONE_UPLOAD_ON_CLICK=True
# DROPZONE_UPLOAD_BTN_ID='submit',

@app.route('/', methods=['GET', 'POST'])
def index():
    file_dir = os.listdir('static/images/')
    # Remove any stored image from the images folder
    if file_dir:
        for f in file_dir:
            os.remove(os.path.join('static/images/', f))
    #set session for image results
    if "filename" not in session:
        session['filename'] = ''
    if(request.method=='POST'):
        print('Request: ', request)
        f = request.files.get('file')
        print(f)
        timestr = time.strftime("%Y%m%d-%H%M%S")
        filename = timestr+'_'+secure_filename(f.filename)
        image_path = os.path.join(app.config['UPLOADED_PATH'], filename)
        f.save(image_path)
        # filename.append(filename.url(filename))
        session['filename'] = filename
        print("Saved at", image_path)
    return render_template('index.html', title='Test')

@app.route('/output')
def quote_output():
    # Redirect to home if no images to display
    if "filename" not in session or session['filename'] == []:
        return redirect(url_for('index'))

    # Set the filename and remove the session variables
    image_path = 'static/images/' + session['filename']
    full_image_path = os.path.join(app.config['UPLOADED_PATH'], session['filename'])
    session.pop('filename', None) #None is the default argument for dict

    pred_list='test'
    # pred_list = image_read.im_read(full_image_path)
    qf = QuoteFinder(full_image_path)
    pred_list = qf.find_quote()
 
    return render_template('output.html', title='Test', pred_list=pred_list, image_path=image_path)

if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=False)