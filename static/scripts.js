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
        predictionOutcome.innerHTML = ''; // Clear previous content
        if (typeof data === 'object' && data !== null) {
          for (const key in data) {
              if (data.hasOwnProperty(key)) {
                  const value = data[key];
                  const paragraph = document.createElement('p');
                  paragraph.textContent = `${key}: ${value}`;
                  predictionOutcome.appendChild(paragraph);
              }
          }
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
});