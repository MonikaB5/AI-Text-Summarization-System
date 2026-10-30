async function loadHistory() {
    try {
        const response = await fetch('/api/history');
        const data = await response.json();
        
        const historyList = document.getElementById('historyList');
        if (!response.ok) {
            historyList.innerHTML = `<div class="alert alert-danger">${data.error}</div>`;
            return;
        }
        
        if (data.length === 0) {
            historyList.innerHTML = `
                <div class="text-center text-muted py-5">
                    <i class="fas fa-inbox fa-3x mb-3"></i>
                    <p>No summaries yet. <a href="/summarize">Create your first summary</a></p>
                </div>
            `;
            return;
        }
        
        let html = '<div class="table-responsive"><table class="table table-hover">';
        html += '<thead><tr><th>Title</th><th>Method</th><th>Words</th><th>Compression</th><th>Date</th><th>Actions</th></tr></thead><tbody>';
        
        data.forEach(item => {
            html += `
                <tr>
                    <td><strong>${item.title || 'Untitled'}</strong></td>
                    <td><span class="badge bg-${item.method === 'extractive' ? 'primary' : 'success'}">${item.method}</span></td>
                    <td>${item.original_word_count} → ${item.summary_word_count}</td>
                    <td>${item.compression_ratio}%</td>
                    <td>${item.created_at}</td>
                    <td>
                        <a href="/history/${item.id}" class="btn btn-sm btn-outline-violet">
                            <i class="fas fa-eye"></i>
                        </a>
                        <button class="btn btn-sm btn-outline-danger" onclick="deleteSummary(${item.id})">
                            <i class="fas fa-trash"></i>
                        </button>
                    </td>
                </tr>
            `;
        });
        
        html += '</tbody></table></div>';
        historyList.innerHTML = html;
    } catch (error) {
        document.getElementById('historyList').innerHTML = '<div class="alert alert-danger">Error loading history</div>';
    }
}

async function deleteSummary(id) {
    if (!confirm('Are you sure you want to delete this summary?')) return;
    
    try {
        const response = await fetch(`/api/history/${id}`, {
            method: 'DELETE'
        });
        const data = await response.json();
        
        if (response.ok) {
            showToast('Summary deleted successfully', 'success');
            loadHistory();
        } else {
            showToast(data.error, 'danger');
        }
    } catch (error) {
        showToast('Error deleting summary', 'danger');
    }
}

function showToast(message, type = 'info') {
    const toast = document.createElement('div');
    toast.className = `alert alert-${type} position-fixed top-0 end-0 m-3`;
    toast.style.zIndex = '9999';
    toast.style.maxWidth = '300px';
    toast.textContent = message;
    document.body.appendChild(toast);
    setTimeout(() => toast.remove(), 3000);
}

document.addEventListener('DOMContentLoaded', loadHistory);
