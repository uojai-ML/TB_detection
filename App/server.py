from flask import Flask, render_template, request, jsonify
import os
import cv2
import tensorflow as tf
import numpy as np

# Create an instance of Flask
app = Flask(__name__)

# Configuration

# This is the folder where images will be uploaded for processing
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# define the image size expected by our model
app.config['IMAGE_SIZE'] = 256

# First, Load the model
path_model = os.path.join('model', 'cnn.keras')
model = tf.keras.models.load_model(  path_model )

#--------------------------------------------------------------
#
#--------------------------------------------------------------
@app.route('/analysis', methods=['GET'])
def analysis():
	return render_template('analysis.html')

#--------------------------------------------------------------
# This function processes an image by invoking the model.
# It returns the results: Tuberculosis or Normal
#--------------------------------------------------------------
def process_image(image):

# Convert image to grayscale
	image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Resize the image
	imagesize = app.config['IMAGE_SIZE']
	image = cv2.resize(image, (imagesize, imagesize))

# Call the model to determine if image has TB
	img_array = np.expand_dims(image, axis=0)  # Add batch dimension
	prediction = model.predict(img_array)

# TB is present if probability is greater than 0.5
	probability = prediction[0][0]

	if probability > 0.5:
	  results = "Tuberculosis"
	else:
	  results = "Normal"
	  probability = 1.0 - probability

# Return the probability and detection class name
	return probability, results


#--------------------------------------------------------------
# This route is called when the user enters
# the application URL on a browser:
# e.g hptt://http://127.0.0.1:5000/
#--------------------------------------------------------------
@app.route('/')
def index():
    return render_template('index.html')

#--------------------------------------------------------------
# This route is called when the user uploads
# an image to the server.
#--------------------------------------------------------------
@app.route('/upload', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    if file:
        # Save the file to the upload folder
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)

        # Read the image using OpenCV
        img = cv2.imread(filepath)

        if img is None:
            return jsonify({'error': 'Invalid image file'}), 400

        # Call the model to determine if image has TB
        certainty, classname = process_image( img )

        print(certainty, classname)

        # Get image dimensions
        height, width, _ = img.shape

        # Return the results as a JSON response
        return jsonify({
            'message': 'File uploaded successfully',
            'filename': file.filename,
            'dimensions': {'width': width, 'height': height},
			'certainty': '{:.2f}%'.format(certainty*100.0),
			'classname': classname
        })


    return results



if __name__ == '__main__':
    app.run(debug=True)
