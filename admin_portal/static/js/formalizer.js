console.log("formalizer.js loaded");
function formalizeMessage() {
    const message = document.getElementById('informalText').value;
    axios.post('/admin-portal/formalize/', { message: message })
        .then(function (response) {
            document.getElementById('informalText').value = response.data.formalized_message;
            document.getElementById('error-message').innerText = '';
        })
        .catch(function (error) {
            console.error('Error:', error);
            document.getElementById('error-message').innerText = 'An error occurred while formalizing the message.';
        });
}