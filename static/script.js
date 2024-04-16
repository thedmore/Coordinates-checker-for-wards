document
  .getElementById("coordinateForm")
  .addEventListener("submit", function (event) {
    event.preventDefault();
    var id = document.getElementById("idInput").value;
    var coordinates = document
      .getElementById("coordinatesInput")
      .value.split(",")
      .map((coord) => parseFloat(coord.trim()));
    var latitude = coordinates[0];
    var longitude = coordinates[1];

    fetch("/check", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        id: id,
        latitude: latitude,
        longitude: longitude,
      }),
    })
      .then((response) => response.text())
      .then((data) => {
        document.getElementById("result").innerText = data;
        document.getElementById("coordinateForm").reset(); // Reset the form
      });
  });
