// API Configuration
const API_BASE_URL = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
    ? 'http://localhost:8000'
    : window.location.origin;

// State Management
let datasets = [];
let currentDatasetId = null;

// DOM Elements
const tabs = document.querySelectorAll('.tab');
const tabContents = document.querySelectorAll('.tab-content');
const uploadArea = document.getElementById('uploadArea');
const fileInput = document.getElementById('fileInput');
const uploadStatus = document.getElementById('uploadStatus');
const useDemoBtn = document.getElementById('useDemoBtn');
const datasetSelect = document.getElementById('datasetSelect');
const queryDatasetSelect = document.getElementById('queryDatasetSelect');
const questionInput = document.getElementById('questionInput');
const askBtn = document.getElementById('askBtn');

// Tab Navigation
tabs.forEach(tab => {
    tab.addEventListener('click', () => {
        const tabId = tab.dataset.tab;
        
        tabs.forEach(t => t.classList.remove('active'));
        tabContents.forEach(content => content.classList.add('hidden'));
        
        tab.classList.add('active');
        document.getElementById(`${tabId}-tab`).classList.remove('hidden');
        
        if (tabId === 'dashboard' || tabId === 'query') {
            updateDatasetSelectors();
        }
    });
});

// File Upload Handling
uploadArea.addEventListener('click', () => fileInput.click());

uploadArea.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadArea.classList.add('dragover');
});

uploadArea.addEventListener('dragleave', () => {
    uploadArea.classList.remove('dragover');
});

uploadArea.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadArea.classList.remove('dragover');
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        handleFileUpload(files[0]);
    }
});

fileInput.addEventListener('change', (e) => {
    if (e.target.files.length > 0) {
        handleFileUpload(e.target.files[0]);
    }
});

// Demo Dataset Button
useDemoBtn.addEventListener('click', async () => {
    showStatus('Loading demo dataset...', 'loading');
    try {
        const response = await fetch(`${API_BASE_URL}/api/v1/upload/demo`, {
            method: 'POST'
        });
        
        if (!response.ok) {
            throw new Error('Failed to load demo dataset');
        }
        
        const result = await response.json();
        showStatus('Demo dataset loaded successfully!', 'success');
        currentDatasetId = result.dataset_id;
        datasets.push({
            id: result.dataset_id,
            name: 'Demo Financial Dataset'
        });
        updateDatasetSelectors();
        
        // Switch to dashboard tab
        setTimeout(() => {
            document.querySelector('[data-tab="dashboard"]').click();
        }, 1000);
    } catch (error) {
        showStatus(`Error: ${error.message}`, 'error');
    }
});

// File Upload Function
async function handleFileUpload(file) {
    const validTypes = ['text/csv', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 'application/vnd.ms-excel'];
    const fileExtension = file.name.split('.').pop().toLowerCase();
    
    if (!['csv', 'xlsx', 'xls'].includes(fileExtension)) {
        showStatus('Invalid file type. Please upload CSV or Excel files.', 'error');
        return;
    }
    
    showStatus('Uploading file...', 'loading');
    
    const formData = new FormData();
    formData.append('file', file);
    
    try {
        const response = await fetch(`${API_BASE_URL}/api/v1/upload/`, {
            method: 'POST',
            body: formData
        });
        
        if (!response.ok) {
            throw new Error('Upload failed');
        }
        
        const result = await response.json();
        showStatus('File uploaded and processed successfully!', 'success');
        currentDatasetId = result.dataset_id;
        datasets.push({
            id: result.dataset_id,
            name: file.name
        });
        updateDatasetSelectors();
        
        // Switch to dashboard tab
        setTimeout(() => {
            document.querySelector('[data-tab="dashboard"]').click();
        }, 1000);
    } catch (error) {
        showStatus(`Error: ${error.message}`, 'error');
    }
}

// Status Display
function showStatus(message, type) {
    uploadStatus.textContent = message;
    uploadStatus.className = `status ${type}`;
    uploadStatus.classList.remove('hidden');
    
    if (type === 'success') {
        setTimeout(() => {
            uploadStatus.classList.add('hidden');
        }, 3000);
    }
}

// Dataset Selectors
function updateDatasetSelectors() {
    const dashboardSelector = document.getElementById('datasetSelector');
    const queryDatasetSelector = document.getElementById('queryDatasetSelector');

    
    if (datasets.length > 0) {
        dashboardSelector.classList.remove('hidden');
        queryDatasetSelector.classList.remove('hidden');
        
        const options = datasets.map(d => `<option value="${d.id}">${d.name}</option>`).join('');
        datasetSelect.innerHTML = '<option value="">-- Select a dataset --</option>' + options;
        queryDatasetSelect.innerHTML = '<option value="">-- Select a dataset --</option>' + options;
        
        if (currentDatasetId) {
            datasetSelect.value = currentDatasetId;
            queryDatasetSelect.value = currentDatasetId;
        }
    } else {
        dashboardSelector.classList.add('hidden');
        queryDatasetSelector.classList.add('hidden');
    }
}

// Dashboard Dataset Selection
datasetSelect.addEventListener('change', async () => {
    const datasetId = datasetSelect.value;
    if (datasetId) {
        currentDatasetId = datasetId;
        await loadDashboard(datasetId);
    }
});

// Query Dataset Selection
queryDatasetSelect.addEventListener('change', () => {
    const datasetId = queryDatasetSelect.value;
    if (datasetId) {
        currentDatasetId = datasetId;
        document.getElementById('queryForm').classList.remove('hidden');
        document.getElementById('noQueryDatasetMessage').classList.add('hidden');
    }
});

// Load Dashboard
async function loadDashboard(datasetId) {
    document.getElementById('dashboardContent').classList.add('hidden');
    document.getElementById('noDatasetMessage').classList.add('hidden');
    
    try {
        const response = await fetch(`${API_BASE_URL}/api/v1/dashboard/${datasetId}`);
        
        if (!response.ok) {
            throw new Error('Failed to load dashboard');
        }
        
        const dashboard = await response.json();
        displayDashboard(dashboard);
    } catch (error) {
        console.error('Error loading dashboard:', error);
        document.getElementById('noDatasetMessage').classList.remove('hidden');
    }
}

// Display Dashboard
function displayDashboard(dashboard) {
    document.getElementById('dashboardContent').classList.remove('hidden');
    
    // Schema
    const schemaContent = document.getElementById('schemaContent');
    if (dashboard.schema && dashboard.schema.columns) {
        let schemaHTML = '<table class="schema-table"><thead><tr><th>Column</th><th>Type</th><th>Description</th></tr></thead><tbody>';
        dashboard.schema.columns.forEach(col => {
            schemaHTML += `<tr><td>${col.name || col.column_name || 'N/A'}</td><td>${col.type || col.data_type || 'N/A'}</td><td>${col.description || '-'}</td></tr>`;
        });
        schemaHTML += '</tbody></table>';
        schemaContent.innerHTML = schemaHTML;
    } else {
        schemaContent.innerHTML = '<p>No schema information available</p>';
    }
    
    // KPIs
    const kpiContent = document.getElementById('kpiContent');
    if (dashboard.kpis && dashboard.kpis.length > 0) {
        let kpiHTML = '<div class="kpi-grid">';
        dashboard.kpis.forEach(kpi => {
            kpiHTML += `
                <div class="kpi-card">
                    <h4>${kpi.name || kpi.metric || 'KPI'}</h4>
                    <div class="value">${kpi.value || kpi.metric_value || 'N/A'}</div>
                    <div class="description">${kpi.description || kpi.insight || ''}</div>
                </div>
            `;
        });
        kpiHTML += '</div>';
        kpiContent.innerHTML = kpiHTML;
    } else {
        kpiContent.innerHTML = '<p>No KPIs available</p>';
    }
    
    // Relationships
    const relationshipsContent = document.getElementById('relationshipsContent');
    if (dashboard.relationships && dashboard.relationships.length > 0) {
        let relHTML = '';
        dashboard.relationships.forEach(rel => {
            relHTML += `
                <div class="relationship-item">
                    <strong>${rel.from || rel.source || 'N/A'}</strong> → 
                    <strong>${rel.to || rel.target || 'N/A'}</strong>
                    ${rel.type ? `(${rel.type})` : ''}
                </div>
            `;
        });
        relationshipsContent.innerHTML = relHTML || '<p>No relationships detected</p>';
    } else {
        relationshipsContent.innerHTML = '<p>No relationships detected</p>';
    }
}

// Query Handling
askBtn.addEventListener('click', async () => {
    const question = questionInput.value.trim();
    const datasetId = queryDatasetSelect.value;
    
    if (!question) {
        alert('Please enter a question');
        return;
    }
    
    if (!datasetId) {
        alert('Please select a dataset');
        return;
    }
    
    askBtn.disabled = true;
    askBtn.textContent = 'Processing...';
    
    try {
        const response = await fetch(`${API_BASE_URL}/api/v1/query`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                dataset_id: datasetId,
                question: question
            })
        });
        
        if (!response.ok) {
            throw new Error('Query failed');
        }
        
        const result = await response.json();
        displayQueryResult(result);
    } catch (error) {
        console.error('Error processing query:', error);
        alert('Error processing query. Please try again.');
    } finally {
        askBtn.disabled = false;
        askBtn.textContent = 'Ask Question';
    }
});

// Display Query Result
function displayQueryResult(result) {
    document.getElementById('queryResult').classList.remove('hidden');
    
    // SQL Query
    document.getElementById('sqlQuery').innerHTML = `
        <h4>Generated SQL Query:</h4>
        <pre>${result.sql_query || result.query || 'N/A'}</pre>
    `;
    
    // Results
    const resultsDiv = document.getElementById('queryResults');
    if (result.results && result.results.length > 0) {
        const columns = Object.keys(result.results[0]);
        let tableHTML = '<table class="results-table"><thead><tr>';
        columns.forEach(col => {
            tableHTML += `<th>${col}</th>`;
        });
        tableHTML += '</tr></thead><tbody>';
        
        result.results.forEach(row => {
            tableHTML += '<tr>';
            columns.forEach(col => {
                tableHTML += `<td>${row[col] !== null ? row[col] : 'NULL'}</td>`;
            });
            tableHTML += '</tr>';
        });
        
        tableHTML += '</tbody></table>';
        resultsDiv.innerHTML = `<h4>Results (${result.results.length} rows):</h4>${tableHTML}`;
    } else {
        resultsDiv.innerHTML = '<h4>Results:</h4><p>No results returned</p>';
    }
    
    // Explanation
    document.getElementById('queryExplanation').innerHTML = `
        <h4>Explanation:</h4>
        <p>${result.explanation || result.description || 'No explanation available'}</p>
    `;
}

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    // Check if there are any existing datasets
    updateDatasetSelectors();
    
    // Show appropriate messages
    if (datasets.length === 0) {
        document.getElementById('noDatasetMessage').classList.remove('hidden');
        document.getElementById('noQueryDatasetMessage').classList.remove('hidden');
    }
});
