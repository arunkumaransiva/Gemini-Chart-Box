const API_BASE_URL = 'http://127.0.0.1:5000';
let chart = null;

async function loadSampleData() {
    const sampleSelect = document.getElementById('sampleData');
    const selectedSample = sampleSelect.value;
    const chartType = document.getElementById('chartType').value;
    
    if (!selectedSample) return;
    
    const errorDiv = document.getElementById('errorMessage');
    const loadingDiv = document.getElementById('loading');
    const chartSection = document.getElementById('chartSection');
    
    errorDiv.innerHTML = '';
    loadingDiv.style.display = 'block';
    chartSection.style.display = 'none';
    
    try {
        const response = await fetch(`${API_BASE_URL}/api/sample-data/${selectedSample}?chartType=${chartType}`);
        
        if (!response.ok) {
            throw new Error('Failed to load sample data');
        }
        
        const result = await response.json();
        
        if (!result.success) {
            throw new Error(result.error || 'Failed to load sample data');
        }
        
        // Display chart
        displayChart(result.chartData, result.chartType);
        
        // Get insights
        getInsights(selectedSample, result.chartData);
        
        chartSection.style.display = 'block';
    } catch (error) {
        console.error('Error:', error);
        errorDiv.innerHTML = `<div class="error">Error: ${error.message}</div>`;
        chartSection.style.display = 'none';
    } finally {
        loadingDiv.style.display = 'none';
    }
}

async function generateChart() {
    const query = document.getElementById('query').value;
    const chartType = document.getElementById('chartType').value;
    const errorDiv = document.getElementById('errorMessage');
    const loadingDiv = document.getElementById('loading');
    const chartSection = document.getElementById('chartSection');
    
    // Clear previous errors
    errorDiv.innerHTML = '';
    
    if (!query.trim()) {
        errorDiv.innerHTML = '<div class="error">Please enter a query</div>';
        return;
    }
    
    // Show loading state
    loadingDiv.style.display = 'block';
    chartSection.style.display = 'none';
    
    try {
        const response = await fetch(`${API_BASE_URL}/api/analyze`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                query: query,
                chartType: chartType
            })
        });
        
        if (!response.ok) {
            throw new Error(`API Error: ${response.statusText}`);
        }
        
        const result = await response.json();
        
        if (!result.success) {
            throw new Error(result.error || 'Failed to generate chart');
        }
        
        // Display chart
        displayChart(result.chartData, result.chartType);
        
        // Get insights
        getInsights(query, result.chartData);
        
        chartSection.style.display = 'block';
    } catch (error) {
        console.error('Error:', error);
        errorDiv.innerHTML = `<div class="error">Error: ${error.message}</div>`;
        chartSection.style.display = 'none';
    } finally {
        loadingDiv.style.display = 'none';
    }
}

function displayChart(chartData, chartType) {
    const ctx = document.getElementById('myChart').getContext('2d');
    
    // Destroy previous chart if it exists
    if (chart) {
        chart.destroy();
    }
    
    // Set default colors if not provided
    if (!chartData.datasets[0].backgroundColor) {
        chartData.datasets[0].backgroundColor = generateColors(chartData.labels.length);
    }
    
    chart = new Chart(ctx, {
        type: chartType,
        data: chartData,
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: true,
                    position: 'top',
                },
                title: {
                    display: false,
                }
            },
            scales: chartType === 'pie' || chartType === 'doughnut' ? {} : {
                y: {
                    beginAtZero: true,
                    ticks: {
                        beginAtZero: true
                    }
                }
            }
        }
    });
}

function generateColors(count) {
    const colors = [
        '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF',
        '#FF9F40', '#FF6384', '#C9CBCF', '#4BC0C0', '#FF6384'
    ];
    
    const result = [];
    for (let i = 0; i < count; i++) {
        result.push(colors[i % colors.length]);
    }
    return result;
}

async function getInsights(description, chartData) {
    try {
        const response = await fetch(`${API_BASE_URL}/api/insights`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                description: description,
                data: chartData
            })
        });
        
        if (!response.ok) {
            throw new Error('Failed to get insights');
        }
        
        const result = await response.json();
        
        if (result.success) {
            document.getElementById('insightsContent').innerHTML = 
                `<p>${result.insights}</p>`;
        }
    } catch (error) {
        console.error('Error getting insights:', error);
        document.getElementById('insightsContent').innerHTML = 
            '<p>Could not generate insights at this time.</p>';
    }
}

// Allow Enter key to generate chart
document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('query').addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            generateChart();
        }
    });
});
