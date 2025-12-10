// Load schema info on page load
document.addEventListener('DOMContentLoaded', function() {
    loadSchemaInfo();
});

function toggleSchema() {
    const schemaInfo = document.getElementById('schemaInfo');
    const toggleIcon = document.getElementById('schemaToggleIcon');
    const isVisible = schemaInfo.style.display !== 'none';
    
    schemaInfo.style.display = isVisible ? 'none' : 'block';
    toggleIcon.textContent = isVisible ? '▼' : '▲';
}

async function loadSchemaInfo() {
    try {
        const response = await fetch('/schema');
        const data = await response.json();
        
        if (data.error) {
            console.error('Error loading schema:', data.error);
            return;
        }
        
        // Update stats
        document.getElementById('totalRows').textContent = data.total_rows.toLocaleString();
        document.getElementById('tableName').textContent = data.table_name;
        document.getElementById('columnCount').textContent = data.columns.length;
        
        // Display departments
        const deptList = document.getElementById('departmentsList');
        deptList.innerHTML = '';
        if (data.departments && data.departments.length > 0) {
            data.departments.forEach(dept => {
                const badge = document.createElement('div');
                badge.className = 'department-badge';
                badge.innerHTML = `<strong>${dept.department}:</strong> ${dept.count} employees`;
                deptList.appendChild(badge);
            });
        }
        
        // Display columns
        const columnsList = document.getElementById('columnsList');
        columnsList.innerHTML = '';
        data.columns.forEach(col => {
            const colItem = document.createElement('div');
            colItem.className = 'column-item';
            colItem.innerHTML = `
                <span class="column-name">${col.name}</span>
                <span class="column-type">${col.type}</span>
            `;
            columnsList.appendChild(colItem);
        });
    } catch (error) {
        console.error('Error loading schema info:', error);
    }
}

function createStatCard(label, value) {
    const card = document.createElement('div');
    card.className = 'stat-card';
    
    const strong = document.createElement('strong');
    strong.textContent = label;
    
    const span = document.createElement('span');
    span.textContent = value;
    
    card.appendChild(strong);
    card.appendChild(span);
    
    return card;
}

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
        statsDiv.innerHTML = ''; // Clear previous stats
        
        if (data.results && data.results.rows !== undefined) {
            // Rows Returned card
            const rowsCard = createStatCard('Rows Returned', data.results.rows);
            statsDiv.appendChild(rowsCard);
            
            // Query Time and Rows Read cards (if statistics available)
            if (data.results.statistics) {
                const timeCard = createStatCard(
                    'Query Time', 
                    `${(data.results.statistics.elapsed * 1000).toFixed(2)} ms`
                );
                statsDiv.appendChild(timeCard);
                
                const readCard = createStatCard(
                    'Rows Read', 
                    data.results.statistics.rows_read || 'N/A'
                );
                statsDiv.appendChild(readCard);
            }
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

