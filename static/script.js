// Add JavaScript code here
// This is just an example
// You can add functionality like handling clicks, animations, etc.

// Example: Alert when an image is clicked
document.addEventListener('DOMContentLoaded', function() {
    const images = document.querySelectorAll('.grid-item img');
    images.forEach(image => {
        image.addEventListener('click', function() {
            alert('You clicked on an image!');
        });
    });
});