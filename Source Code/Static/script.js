document.getElementById('studentForm').addEventListener('submit', function(event) {
    event.preventDefault();
    alert('Form submitted successfully!');
});

document.getElementById('cancelButton').addEventListener('click', function() {
    document.getElementById('studentForm').reset();
});
