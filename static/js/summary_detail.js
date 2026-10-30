async function loadSummaryDetail() {
    try {
        const response = await fetch(`/api/history/${summaryId}`);
        const data = await response.json();
        
        const detailContent = document.getElementById('detailContent');
        if (!response.ok) {
            detailContent.innerHTML = `<div class="alert alert-danger">${data.error}</div>`;
            return;
        }
        
        let keywordsHtml = '';
        if (data.keywords && data.keywords.length > 0) {
            keywordsHtml = '<h6><i class="fas fa-tags me-2"></i>Keywords</h6>';
            data.keywords.forEach(k => {
                keywordsHtml += `<span class="keyword-badge">${k}</span>`;
            });
        }
        
        detailContent.innerHTML = `
            <div class="row">
                <div class="col-12 mb-4">
                    <div class="card shadow border-0">
                        <div class="card-header bg-navy text-white">
                            <h5 class="mb-0">${data.title || 'Untitled Summary'}</h5>
                        </div>
                        <div class="card-body">
                            <div class="row mb-3">
                                <div class="col-md-3">
                                    <small class="text-muted">Method</small><br>
                                    <strong>${data.method}</strong>
                                </div>
                                <div class="col-md-3">
                                    <small class="text-muted">Model</small><br>
                                    <strong>${data.model_used}</strong>
                                </div>
                                <div class="col-md-3">
                                    <small class="text-muted">Created</small><br>
                                    <strong>${data.created_at}</strong>
                                </div>
                                <div class="col-md-3">
                                    <small class="text-muted">Source</small><br>
                                    <strong>${data.source_type}</strong>
                                </div>
                            </div>
                            <div class="row mb-3">
                                <div class="col-md-3">
                                    <small class="text-muted">Original Words</small><br>
                                    <strong>${data.original_word_count}</strong>
                                </div>
                                <div class="col-md-3">
                                    <small class="text-muted">Summary Words</small><br>
                                    <strong>${data.summary_word_count}</strong>
                                </div>
                                <div class="col-md-3">
                                    <small class="text-muted">Compression</small><br>
                                    <strong>${data.compression_ratio}%</strong>
                                </div>
                                <div class="col-md-3">
                                    <small class="text-muted">Processing Time</small><br>
                                    <strong>${data.processing_time}s</strong>
                                </div>
                            </div>
                            ${keywordsHtml}
                        </div>
                    </div>
                </div>
                
                <div class="col-lg-6 mb-4">
                    <div class="card shadow border-0 h-100">
                        <div class="card-header bg-light">
                            <h6 class="mb-0"><i class="fas fa-file-alt me-2"></i>Original Text</h6>
                        </div>
                        <div class="card-body">
                            <div style="max-height: 400px; overflow-y: auto;">
                                <p style="white-space: pre-wrap;">${data.original_text}</p>
                            </div>
                        </div>
                    </div>
                </div>
                
                <div class="col-lg-6 mb-4">
                    <div class="card shadow border-0 h-100">
                        <div class="card-header bg-violet text-white">
                            <h6 class="mb-0"><i class="fas fa-magic me-2"></i>Summary</h6>
                        </div>
                        <div class="card-body">
                            <div style="max-height: 400px; overflow-y: auto;">
                                <p style="white-space: pre-wrap;">${data.summary_text}</p>
                            </div>
                            <button class="btn btn-violet mt-3" onclick="copyText('${data.summary_text.replace(/'/g, "\\'")}')">
                                <i class="fas fa-copy me-2"></i>Copy Summary
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        `;
    } catch (error) {
        document.getElementById('detailContent').innerHTML = '<div class="alert alert-danger">Error loading details</div>';
    }
}

function copyText(text) {
    navigator.clipboard.writeText(text).then(() => {
        showToast('Copied to clipboard', 'success');
    });
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

document.addEventListener('DOMContentLoaded', loadSummaryDetail);
