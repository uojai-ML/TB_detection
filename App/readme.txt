README

This folder containts the TB Detection application code and 
resources.  This directory is structured as follows:

App/
│
├── server.py
├── static/
│   ├── style.css
│   ├── bootstrap.min.css
│   ├── analysis.js
│   └── uploads
├── templates/
│   ├── index.html
│   └── analysis.html
└── model/
    └── cnn.keras


DESCRIPTION OF FILES

server.py - this is the flask server that runs the application
static/style.css - CSS style for the look and feel of HTML elements
static/bootstrap.min.css - CSS style for look and feel of HTML elements
static/analysis.js - Javascript to handle the uploading of image and display results
static/uploads - directory to store uploaded images
templates/index.html - the welcome page
templates/analysis.html - the x ray image upload page


REQUIRED LIBRARIES

- Python
- flask (pip install flask)
- opencv (pip install opencv-python)
- tensorflow  (pip install tensorflow)

