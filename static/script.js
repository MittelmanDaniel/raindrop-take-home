function useExample(query) {
    document.getElementById('queryInput').value = query;
    submitQuery();
}

async function submitQuery() {
    const queryInput = document.getElementById('queryInput');
    const query = queryInput.value.trim();
    
    if (!query) {
        alert('Please enter a query');
        return;
    }

    // Hide previous results
    document.getElementById('results').style.display = 'none';
    document.getElementById('error').style.display = 'none';
    document.getElementById('loading').style.display = 'block';
    
    const submitBtn = document.getElementById('submitBtn');
    submitBtn.disabled = true;

    try {
        const response = await fetch('/query', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ query: query })
        });

        const data = await response.json();
        document.getElementById('loading').style.display = 'none';
        submitBtn.disabled = false;

        if (data.error) {
            document.getElementById('error').textContent = 'Error: ' + data.error;
            document.getElementById('error').style.display = 'block';
            return;
        }

        // Display SQL
        document.getElementById('sqlQuery').textContent = data.generated_sql;

        // Display stats
        const statsDiv = document.getElementById('stats');
        if (data.results && data.results.rows !== undefined) {
            statsDiv.innerHTML = `
                <div class="stat-card">
                    <strong>Rows Returned</strong>
                    <span>${data.results.rows}</span>
                </div>
                ${data.results.statistics ? `
                    <div class="stat-card">
                        <strong>Query Time</strong>
                        <span>${(data.results.statistics.elapsed * 1000).toFixed(2)} ms</span>
                    </div>
                    <div class="stat-card">
                        <strong>Rows Read</strong>
                        <span>${data.results.statistics.rows_read || 'N/A'}</span>
                    </div>
                ` : ''}
            `;
        } else {
            statsDiv.innerHTML = '';
        }

        // Display JSON data
        document.getElementById('jsonData').textContent = JSON.stringify(data.results, null, 2);
        document.getElementById('results').style.display = 'block';

    } catch (error) {
        document.getElementById('loading').style.display = 'none';
        submitBtn.disabled = false;
        document.getElementById('error').textContent = 'Error: ' + error.message;
        document.getElementById('error').style.display = 'block';
    }
}

