document.addEventListener("DOMContentLoaded", function () {
    const paths = document.querySelectorAll('path');

    paths.forEach(path => {
        path.addEventListener('click', function () {
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
                    updateTable(stateName, data);
                })
                .catch(error => {
                    console.error('There was a problem with the fetch operation:', error);
                });
        });
    });

    function updateTable(stateName, data) {
        document.getElementById('StateName').innerText = stateName;
        const tableBody = document.getElementById('table-body');
        tableBody.innerHTML = ''; // Clear existing rows
        Object.entries(data).forEach(([key, value]) => {
            const row = document.createElement('tr');
            
            // Key cell
            const keyCell = document.createElement('td');
            keyCell.textContent = key;
            row.appendChild(keyCell);

            // Prediction cell
            const predictionCell = document.createElement('td');
            predictionCell.textContent = value[0]|| "N/A";
            row.appendChild(predictionCell);

            // Accuracy cell
            const accuracyCell = document.createElement('td');
            accuracyCell.textContent = value[1]|| "N/A";
            row.appendChild(accuracyCell);

            // Prediction cell
            const predictionCell1 = document.createElement('td');
            predictionCell1.textContent = value[2]|| "N/A";
            row.appendChild(predictionCell1);
    
            // Cost cell
            const costCell = document.createElement('td');
            costCell.textContent = value[3].toLocaleString();
            row.appendChild(costCell);
    
            tableBody.appendChild(row);
        });
    }
    
});