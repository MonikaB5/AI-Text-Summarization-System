let extractedText = '';
let extractedSourceType = 'text';
let extractedSourceFilename = null;
let extractedSourceUrl = null;

// Character count for text input
const inputText = document.getElementById('inputText');
if (inputText) {
    inputText.addEventListener('input', function() {
        document.getElementById('textCharCount').textContent = this.value.length;
        extractedText = this.value;
        extractedSourceType = 'text';
        extractedSourceFilename = null;
        extractedSourceUrl = null;
    });
}

// File upload
const fileInput = document.getElementById('fileInput');
if (fileInput) {
    fileInput.addEventListener('change', async function(e) {
        const file = e.target.files[0];
        if (!file) return;
        
        const formData = new FormData();
        formData.append('file', file);
        
        document.getElementById('loadingDiv').style.display = 'block';
        
        try {
            const response = await fetch('/api/upload', {
                method: 'POST',
                body: formData
            });
            const data = await response.json();
            
            if (response.ok) {
                extractedText = data.text;
                extractedSourceType = 'file';
                extractedSourceFilename = data.filename;
                extractedSourceUrl = null;
                document.getElementById('fileName').textContent = data.filename;
                document.getElementById('fileLength').textContent = data.length;
                document.getElementById('fileInfo').style.display = 'block';
                showToast('File uploaded and processed successfully', 'success');
            } else {
                showToast(data.error, 'danger');
            }
        } catch (error) {
            showToast('Error uploading file', 'danger');
        } finally {
            document.getElementById('loadingDiv').style.display = 'none';
        }
    });
}

// URL extraction
const extractUrlBtn = document.getElementById('extractUrlBtn');
if (extractUrlBtn) {
    extractUrlBtn.addEventListener('click', async function() {
        const url = document.getElementById('urlInput').value;
        if (!url) {
            showToast('Please enter a URL', 'warning');
            return;
        }
        
        document.getElementById('loadingDiv').style.display = 'block';
        
        try {
            const response = await fetch('/api/extract-url', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ url: url })
            });
            const data = await response.json();
            
            if (response.ok) {
                extractedText = data.text;
                extractedSourceType = 'url';
                extractedSourceFilename = null;
                extractedSourceUrl = data.url;
                document.getElementById('urlText').textContent = data.url;
                document.getElementById('urlLength').textContent = data.length;
                document.getElementById('urlInfo').style.display = 'block';
                showToast('URL content extracted successfully', 'success');
            } else {
                showToast(data.error, 'danger');
            }
        } catch (error) {
            showToast('Error extracting URL', 'danger');
        } finally {
            document.getElementById('loadingDiv').style.display = 'none';
        }
    });
}

// Summarize button
const summarizeBtn = document.getElementById('summarizeBtn');
if (summarizeBtn) {
    summarizeBtn.addEventListener('click', async function() {
        const method = document.getElementById('methodSelect').value;
        const summaryLength = document.getElementById('lengthSelect').value;
        const title = document.getElementById('summaryTitle').value;
        
        if (!extractedText || extractedText.trim().length < 50) {
            showToast('Please provide text with at least 50 characters', 'warning');
            return;
        }
        
        document.getElementById('loadingDiv').style.display = 'block';
        document.getElementById('summaryPlaceholder').style.display = 'none';
        document.getElementById('summaryContent').style.display = 'none';
        
        try {
            const response = await fetch('/api/summarize', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    text: extractedText,
                    method: method,
                    summary_length: summaryLength,
                    source_type: extractedSourceType,
                    source_filename: extractedSourceFilename,
                    source_url: extractedSourceUrl,
                    title: title
                })
            });
            const data = await response.json();
            
            if (response.ok) {
                // Display summary
                document.getElementById('summaryText').value = data.summary_text;
                document.getElementById('origWords').textContent = data.original_word_count;
                document.getElementById('sumWords').textContent = data.summary_word_count;
                document.getElementById('compression').textContent = data.compression_ratio + '%';
                document.getElementById('procTime').textContent = data.processing_time + 's';
                document.getElementById('methodUsed').textContent = data.method === 'extractive' ? 'Extractive (TextRank)' : 'Abstractive (BART)';
                document.getElementById('modelUsed').textContent = data.model_used;
                
                if (data.fallback_used) {
                    document.getElementById('fallbackWarning').style.display = 'block';
                } else {
                    document.getElementById('fallbackWarning').style.display = 'none';
                }
                
                // Display keywords
                const keywordsList = document.getElementById('keywordsList');
                keywordsList.innerHTML = '';
                if (data.keywords && data.keywords.length > 0) {
                    data.keywords.forEach(keyword => {
                        const badge = document.createElement('span');
                        badge.className = 'keyword-badge';
                        badge.textContent = keyword;
                        keywordsList.appendChild(badge);
                    });
                }
                
                // Display key sentences
                if (data.key_sentences && data.key_sentences.length > 0) {
                    const keyList = document.getElementById('keySentencesList');
                    keyList.innerHTML = '';
                    data.key_sentences.forEach(s => {
                        const li = document.createElement('li');
                        li.textContent = s;
                        keyList.appendChild(li);
                    });
                    document.getElementById('keySentencesSection').style.display = 'block';
                }
                
                document.getElementById('summaryContent').style.display = 'block';
                showToast('Summary generated successfully!', 'success');
            } else {
                showToast(data.error, 'danger');
                document.getElementById('summaryPlaceholder').style.display = 'block';
            }
        } catch (error) {
            showToast('Error generating summary', 'danger');
            document.getElementById('summaryPlaceholder').style.display = 'block';
        } finally {
            document.getElementById('loadingDiv').style.display = 'none';
        }
    });
}

// Compare button
const compareBtn = document.getElementById('compareBtn');
if (compareBtn) {
    compareBtn.addEventListener('click', async function() {
        const summaryLength = document.getElementById('lengthSelect').value;
        if (!extractedText || extractedText.trim().length < 30) {
            showToast('Please provide text with at least 30 characters', 'warning');
            return;
        }
        document.getElementById('loadingDiv').style.display = 'block';
        try {
            const response = await fetch('/api/compare', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({text: extractedText, summary_length: summaryLength})
            });
            const data = await response.json();
            if (response.ok) {
                document.getElementById('extSummary').value = data.extractive.summary_text;
                document.getElementById('extWords').textContent = data.extractive.word_count;
                document.getElementById('extComp').textContent = data.extractive.compression_ratio;
                document.getElementById('extTime').textContent = data.extractive.processing_time;
                
                if (data.abstractive.error) {
                    document.getElementById('absSummary').value = '';
                    document.getElementById('absError').textContent = 'Error: ' + data.abstractive.error;
                    document.getElementById('absError').style.display = 'block';
                    document.getElementById('absWords').textContent = '-';
                    document.getElementById('absComp').textContent = '-';
                    document.getElementById('absTime').textContent = '-';
                } else {
                    document.getElementById('absSummary').value = data.abstractive.summary_text;
                    document.getElementById('absWords').textContent = data.abstractive.word_count;
                    document.getElementById('absComp').textContent = data.abstractive.compression_ratio;
                    document.getElementById('absTime').textContent = data.abstractive.processing_time;
                    document.getElementById('absError').style.display = 'none';
                }
                document.getElementById('comparisonSection').style.display = 'block';
                showToast('Comparison generated', 'success');
            } else {
                showToast(data.error, 'danger');
            }
        } catch (error) {
            showToast('Error comparing', 'danger');
        } finally {
            document.getElementById('loadingDiv').style.display = 'none';
        }
    });
}

// Evaluate button
const evaluateBtn = document.getElementById('evaluateBtn');
if (evaluateBtn) {
    evaluateBtn.addEventListener('click', async function() {
        const summary = document.getElementById('summaryText').value;
        const reference = document.getElementById('referenceSummary').value;
        if (!summary) {
            showToast('Generate a summary first', 'warning');
            return;
        }
        if (!reference) {
            showToast('Enter reference summary', 'warning');
            return;
        }
        try {
            const response = await fetch('/api/evaluate', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({summary: summary, reference: reference})
            });
            const data = await response.json();
            if (response.ok) {
                document.getElementById('r1p').textContent = data.rouge1.precision;
                document.getElementById('r1r').textContent = data.rouge1.recall;
                document.getElementById('r1f').textContent = data.rouge1.fmeasure;
                document.getElementById('r2p').textContent = data.rouge2.precision;
                document.getElementById('r2r').textContent = data.rouge2.recall;
                document.getElementById('r2f').textContent = data.rouge2.fmeasure;
                document.getElementById('r3p').textContent = data.rougeL.precision;
                document.getElementById('r3r').textContent = data.rougeL.recall;
                document.getElementById('r3f').textContent = data.rougeL.fmeasure;
                document.getElementById('rougeNote').textContent = data.note;
                document.getElementById('rougeResults').style.display = 'block';
                showToast('Evaluation complete', 'success');
            } else {
                showToast(data.error, 'danger');
            }
        } catch (error) {
            showToast('Error evaluating', 'danger');
        }
    });
}

function copySummary() {
    const summaryText = document.getElementById('summaryText');
    summaryText.select();
    document.execCommand('copy');
    showToast('Summary copied to clipboard', 'success');
}

async function downloadTxt() {
    const text = document.getElementById('summaryText').value;
    if (!text) {
        showToast('No summary to download', 'warning');
        return;
    }
    const stats = {
        original_words: document.getElementById('origWords').textContent,
        summary_words: document.getElementById('sumWords').textContent,
        compression_ratio: document.getElementById('compression').textContent,
        method: document.getElementById('methodUsed').textContent,
        model_used: document.getElementById('modelUsed').textContent,
        processing_time: document.getElementById('procTime').textContent.replace('s', '')
    };
    try {
        const response = await fetch('/api/export/txt', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({summary_text: text, stats: stats})
        });
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'summary.txt';
        a.click();
        window.URL.revokeObjectURL(url);
        showToast('Downloaded as TXT', 'success');
    } catch (error) {
        showToast('Error downloading', 'danger');
    }
}

async function downloadPdf() {
    const text = document.getElementById('summaryText').value;
    if (!text) {
        showToast('No summary to download', 'warning');
        return;
    }
    const stats = {
        original_words: document.getElementById('origWords').textContent,
        summary_words: document.getElementById('sumWords').textContent,
        compression_ratio: document.getElementById('compression').textContent,
        method: document.getElementById('methodUsed').textContent,
        model_used: document.getElementById('modelUsed').textContent,
        processing_time: document.getElementById('procTime').textContent.replace('s', '')
    };
    try {
        const response = await fetch('/api/export/pdf', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({summary_text: text, stats: stats})
        });
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'summary.pdf';
        a.click();
        window.URL.revokeObjectURL(url);
        showToast('Downloaded as PDF', 'success');
    } catch (error) {
        showToast('Error downloading', 'danger');
    }
}

async function downloadDocx() {
    const text = document.getElementById('summaryText').value;
    if (!text) {
        showToast('No summary to download', 'warning');
        return;
    }
    const stats = {
        original_words: document.getElementById('origWords').textContent,
        summary_words: document.getElementById('sumWords').textContent,
        compression_ratio: document.getElementById('compression').textContent,
        method: document.getElementById('methodUsed').textContent,
        model_used: document.getElementById('modelUsed').textContent,
        processing_time: document.getElementById('procTime').textContent.replace('s', '')
    };
    try {
        const response = await fetch('/api/export/docx', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({summary_text: text, stats: stats})
        });
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'summary.docx';
        a.click();
        window.URL.revokeObjectURL(url);
        showToast('Downloaded as DOCX', 'success');
    } catch (error) {
        showToast('Error downloading', 'danger');
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
