function saveTrip() {
  const name = document.getElementById("tripName").value;
  const destination = document.getElementById("destination").value;

  if (!name || !destination) {
    alert("Please fill all fields!");
    return;
  }

  let trips = JSON.parse(localStorage.getItem("trips")) || [];

  trips.push({ name, destination });

  localStorage.setItem("trips", JSON.stringify(trips));

  alert("Trip Saved!");
}