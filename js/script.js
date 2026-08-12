function saveTrip() {
    const name = document.getElementById("tripName").value;
    const destination = document.getElementById("destination").value;

    if (!name || !destination) {
        alert("Please fill all fields!");
        return;
    }

    fetch("http://127.0.0.1:8000/trips", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            name: name,
            destination: destination
        })
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
        alert("Trip Saved Successfully!");
    })
    .catch(error => {
        console.error("Error:", error);
        alert("Error saving trip!");
    });
}