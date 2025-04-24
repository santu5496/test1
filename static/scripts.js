document.getElementById('weather-data-form').addEventListener('submit', function(event) {
    event.preventDefault();
    const formData = new FormData(this);
    const data = {};
    formData.forEach((value, key) => {
        data[key] = value;
    });
    fetch('/predict', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    })
    .then(response => response.json())
    .then(data => {
        const predictionOutcome = document.getElementById('prediction-outcome');
        predictionOutcome.textContent = `Prediction: ${data.disaster_type}`;
    })
    .catch(error => {
        console.error('Error:', error);
    });
});