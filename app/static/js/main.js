// ============================================================
// TAB SWITCHING
// ============================================================
function showTab(tabName, e) {
    document.querySelectorAll('.tab-content').forEach(el => {
        el.classList.remove('active');
    });
    document.querySelectorAll('.tab-btn').forEach(el => {
        el.classList.remove('active');
    });

    document.getElementById('tab-' + tabName).classList.add('active');
    if (e && e.target) e.target.classList.add('active');

    if (tabName === 'bpmn') {
        if (typeof renderMermaidDiagram === 'function') {
            renderMermaidDiagram();
        }
    }
}

// ============================================================
// DOWNLOAD DIAGRAM AS PNG
// ============================================================
function downloadDiagram() {
    const container = document.getElementById('mermaid-output');
    if (!container || !container.querySelector('svg')) {
        alert('Diagram not rendered yet. Click the Process Diagram tab first.');
        return;
    }

    const name = typeof processName !== 'undefined' ? processName : 'diagram';

    html2canvas(container, {
        backgroundColor: '#ffffff',
        scale: 2,
        useCORS: true,
        allowTaint: false
    }).then(function(canvas) {
        const a = document.createElement('a');
        a.download = name + '-diagram.png';
        a.href = canvas.toDataURL('image/png');
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
    }).catch(function(err) {
        console.error('html2canvas error:', err);
        alert('PNG export failed. Try downloading BPMN XML instead.');
    });
}
// ============================================================
// DOWNLOAD MARKDOWN
// ============================================================
function downloadMarkdown() {
    if (typeof sopRaw === 'undefined' || !sopRaw) {
        alert('No SOP content available.');
        return;
    }
    const blob = new Blob([sopRaw], { type: 'text/markdown' });
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = (typeof processName !== 'undefined' ? processName : 'SOP') + '.md';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
}

// ============================================================
// DOWNLOAD BPMN XML
// ============================================================
function downloadBPMN() {
    if (typeof bpmnXml === 'undefined' || !bpmnXml) {
        alert('No BPMN XML available for this SOP.');
        return;
    }
    const blob = new Blob([bpmnXml], { type: 'application/xml' });
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = (typeof processName !== 'undefined' ? processName : 'diagram') + '.bpmn';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
}

// ============================================================
// FORM LOADING STATE
// ============================================================
const form = document.getElementById('sop-form');
if (form) {
    form.addEventListener('submit', function () {
        const overlay = document.getElementById('loading-overlay');
        if (overlay) overlay.classList.add('active');
        const btn = document.getElementById('submit-btn');
        if (btn) btn.disabled = true;
    });
}