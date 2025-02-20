// Get references to DOM elements
const fileInput = document.getElementById('fileInput');
const preview = document.getElementById('preview');
const certainty = document.getElementById('certainty');
const classname = document.getElementById('classname');
const resultDiv = document.getElementById('results');
const processButton = document.getElementById('processButton');

processButton.style.visibility = 'hidden';
certainty.innerText = '';
classname.innerText = '';

// Event listener for file input change
fileInput.addEventListener('change', function () {
    const file = fileInput.files[0];
    certainty.innerText = '';
    classname.innerText = '';
    console.log('onchange')

    if (file) {
        // Display the image preview
        const reader = new FileReader();
        reader.onload = function (e) {
            preview.src = e.target.result;
            preview.style.display = 'block';
            processButton.disabled = false; // Enable the upload button
            processButton.style.visibility = 'visible';
            resultDiv.innerText = ''; // Clear any previous status
        };
        reader.readAsDataURL(file);
    } else {
        // No file selected
        preview.style.display = 'none';
        processButton.disabled = true;
        processButton.style.visibility = 'hidden';
        resultDiv.innerText = 'No file selected.';

    }
});

function uploadImage() {
    const fileInput = document.getElementById('fileInput');
    const resultDiv = document.getElementById('result');

    if (!fileInput.files || !fileInput.files[0]) {
        resultDiv.innerText = 'Please select an image first.';
        return;
    }

    const formData = new FormData();
    formData.append('file', fileInput.files[0]);

    fetch('/upload', {
        method: 'POST',
        body: formData
    })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                resultDiv.innerText = 'Error: ' + data.error;
            } else {
                certainty.innerText = `${data.certainty}`;
                classname.innerText = `${data.classname}`;
            }
        })
        .catch(error => {
            resultDiv.innerText = 'Error: ' + error.message;
        });
}