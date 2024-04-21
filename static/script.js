document.addEventListener("DOMContentLoaded", function() {
    const paths = document.querySelectorAll('path');

    paths.forEach(path => {
        path.addEventListener('click', function() {
            var stateName = this.id;
            var requestData = { state: stateName };
    
            // Send the data to the backend
            fetch('/send-data', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(requestData)
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                // Handle the response from the backend
                console.log('Response from backend:', data);
                console.log(stateName)
                updateTable(data);
            })
            .catch(error => {
                console.error('There was a problem with the fetch operation:', error);
            });
        });
    });

    function updateTable(data) {
        const tableBody = document.getElementById('table-body');
        tableBody.innerHTML = ''; // Clear existing rows
        Object.entries(data).forEach(([key, value]) => {
            const row = document.createElement('tr');
            const predictionCell = document.createElement('td');
            predictionCell.textContent = key + ": " + value[0];
            const costCell = document.createElement('td');
            costCell.textContent = value[1].toLocaleString();
            row.appendChild(predictionCell);
            row.appendChild(costCell);
            tableBody.appendChild(row);
        });
    }
});