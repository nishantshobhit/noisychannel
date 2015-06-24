import os
# We'll render HTML templates and access data sent by POST
# using the request object from flask. Redirect and url_for
# will be used to redirect the user once the upload is done
# and send_from_directory will help us to send/show on the
# browser the file that the user just uploaded
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from werkzeug import secure_filename

from pyimagesearch.colordescriptor import ColorDescriptor
from pyimagesearch.searcher import Searcher
import argparse
import cv2

# initialize the image descriptor
COLOR_DESC = ColorDescriptor((8, 12, 3))
index_file = "neiman_top.csv"
SEARCHER = Searcher(index_file)

def image_url_map(filename):
    with open(filename) as f:
        return {os.path.basename(line.strip()):line.strip() for line in f if line.strip()}

#IMAGE_URL_MAP = image_url_map("n_images.txt")
IMAGE_URL_MAP = image_url_map("neiman_top/neiman_top.txt")


def search_results(filename, searcher):
    # load the query image and describe it
    try:
        query = cv2.imread(filename)
    except TypeError:
        query = cv2.imdecode(filename)
    features = COLOR_DESC.describe(query)
    results = searcher.search(features)
    return results


# Initialize the Flask application
app = Flask(__name__)

# This is the path to the upload directory
app.config['UPLOAD_FOLDER'] = 'uploads'
# These are the extension that we are accepting to be uploaded
app.config['ALLOWED_EXTENSIONS'] = set(['png', 'jpg', 'jpeg', 'gif'])

# For a given file, return whether it's an allowed type or not
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

# This route will show a form to perform an AJAX request
# jQuery is loaded to execute the request and update the
# value of the operation
@app.route('/')
def index():
    return render_template('index.html')

# Route that will process the file upload
@app.route('/upload', methods=['POST'])
def upload():
    # Get the name of the uploaded file
    file = request.files['file']
    # Check if the file is one of the allowed types/extensions
    if file and allowed_file(file.filename):
        # Make the filename safe, remove unsupported chars
        filename = secure_filename(file.filename)
        # Move the file form the temporal folder to
        # the upload folder we setup
        save_name = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(save_name)
        print "Finding results"
        results = search_results(save_name, SEARCHER)
        images = []
        for a, b in results:
            b = IMAGE_URL_MAP.get(b, b)
            print a, b
            images.append(b)
        # Redirect the user to the uploaded_file route, which
        # will basicaly show on the browser the uploaded file
        #return redirect(url_for('uploaded_file', filename=filename))
        return render_template('image_layout.html', items=images)


# This route is expecting a parameter containing the name
# of a file. Then it will locate that file on the upload
# directory and show it on the browser, so if the user uploads
# an image, that image is going to be show after the upload
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

if __name__ == '__main__':
    app.run(
        host="0.0.0.0",
        port=int("7090"),
        debug=True
    )
