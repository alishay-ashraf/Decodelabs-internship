// Initialize Chart.js
const ctx = document.getElementById('iotChart').getContext('2d');
const maxDataPoints = 10;

const iotChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: [], // Timestamps go here
        datasets: [
            {
                label: 'Temperature (°C)',
                data: [],
                borderColor: '#ff6384',
                backgroundColor: 'rgba(255, 99, 132, 0.1)',
                borderWidth: 2,
                tension: 0.3,
                yAxisID: 'y-temp'
            },
            {
                label: 'Humidity (%)',
                data: [],
                borderColor: '#36a2eb',
                backgroundColor: 'rgba(54, 162, 235, 0.1)',
                borderWidth: 2,
                tension: 0.3,
                yAxisID: 'y-humid'
            }
        ]
    },
    options: {
        responsive: true,
        scales: {
            'y-temp': {
                type: 'linear',
                position: 'left',
                title: { display: true, text: 'Temperature (°C)', color: '#ff6384' }
            },
            'y-humid': {
                type: 'linear',
                position: 'right',
                title: { display: true, text: 'Humidity (%)', color: '#36a2eb' },
                grid: { drawOnChartArea: false } // prevents grid line overlap
            }
        }
    }
});

// Function to simulate incoming IoT device data
function generateMockSensorData() {
    const now = new Date();
    const timestamp = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' });
    
    // Simulate natural ambient flux variations
    const temperature = (22 + Math.random() * 5).toFixed(1); 
    const humidity = (50 + Math.random() * 15).toFixed(1);

    return { timestamp, temperature, humidity };
}

// Function to update the entire UI
function updateDashboard() {
    const data = generateMockSensorData();

    // 1. Update metric cards text
    document.getElementById('temp-val').innerText = data.temperature;
    document.getElementById('humid-val').innerText = data.humidity;

    // 2. Update the Chart
    if (iotChart.data.labels.length >= maxDataPoints) {
        iotChart.data.labels.shift();
        iotChart.data.datasets[0].data.shift();
        iotChart.data.datasets[1].data.shift();
    }
    
    iotChart.data.labels.push(data.timestamp);
    iotChart.data.datasets[0].data.push(data.temperature);
    iotChart.data.datasets[1].data.push(data.humidity);
    iotChart.update(); // Redraws chart dynamically

    // 3. Update the historical log table
    const tableBody = document.getElementById('table-body');
    const newRow = document.createElement('tr');
    newRow.innerHTML = `
        <td>${data.timestamp}</td>
        <td>${data.temperature}</td>
        <td>${data.humidity}</td>
    `;
    
    // Insert new logs at the top
    tableBody.insertBefore(newRow, tableBody.firstChild);

    // Prune the table rows if they exceed our visual history budget
    if (tableBody.children.length > maxDataPoints) {
        tableBody.removeChild(tableBody.lastChild);
    }
}

// Initial pull on load, then poll every 3000ms (3 seconds)
updateDashboard();
setInterval(updateDashboard, 3000);