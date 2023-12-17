document.getElementById('uploadForm').addEventListener('submit', function (event) {
    event.preventDefault(); // Prevent the default form submission
    convertImage();
});

function convertImage() {
    const inputElement = document.getElementById('imageInput');
    const fileTypeElement = document.getElementById('fileType');
    const convertedImageElement = document.getElementById('convertedImage');
    const downloadLinkElement = document.getElementById('downloadLink');

    const file = inputElement.files[0];

    if (file) {
        const formData = new FormData();
        formData.append('image', file);
        formData.append('fileType', fileTypeElement.value);

        // Hide the "Converted image" text initially
        convertedImageElement.style.display = 'none';

        fetch('/convert', {
            method: 'POST',
            body: formData
        })
        .then(response => response.blob())
        .then(blob => {
            // Display converted image
            convertedImageElement.src = URL.createObjectURL(blob);

            // Enable download link
            downloadLinkElement.href = URL.createObjectURL(blob);
            downloadLinkElement.style.display = 'inline';

            // Show the "Converted image" text
            convertedImageElement.style.display = 'block';

            // Adjust the size of the displayed image based on its aspect ratio
            const img = new Image();
            img.src = URL.createObjectURL(blob);
            img.onload = function () {
                const aspectRatio = img.width / img.height;
                const maxWidth = window.innerWidth / 3; // Adjust this value as needed

                if (aspectRatio > 1) {
                    // Landscape image
                    convertedImageElement.style.width = Math.min(img.width, maxWidth) + 'px';
                    convertedImageElement.style.height = 'auto';
                } else {
                    // Portrait or square image
                    convertedImageElement.style.width = 'auto';
                    convertedImageElement.style.height = Math.min(img.height, maxWidth) + 'px';
                }
            };
        })
        .catch(error => console.error('Error:', error));
    }
}

