"""
dashboard.py
------------
Lightweight interactive UI for uploading CSV files, viewing raw & cleaned data,
triggering Agent 1 feedback analysis, and viewing full structured intelligence.
"""

from fastapi.responses import HTMLResponse

DASHBOARD_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Customer Feedback Intelligence Dashboard (Milestone 2)</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
  <style>
    .badge-positive { background-color: #def7ec; color: #03543f; border: 1px solid #31c48d; }
    .badge-negative { background-color: #fde8e8; color: #9b1c1c; border: 1px solid #f98080; }
    .badge-neutral  { background-color: #e1effe; color: #1e429f; border: 1px solid #76a9fa; }
    .badge-complaint { background-color: #feecdc; color: #8a2c0d; }
    .badge-request   { background-color: #edebfe; color: #5521b5; }
    .badge-praise    { background-color: #def7ec; color: #03543f; }
    .badge-inquiry   { background-color: #e1effe; color: #1e429f; }
    .badge-feedback  { background-color: #f3f4f6; color: #374151; }
  </style>
</head>
<body class="bg-slate-50 min-h-screen text-slate-800 antialiased">

  <!-- Header -->
  <header class="bg-white border-b border-slate-200 sticky top-0 z-30 shadow-sm">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
      <div class="flex items-center space-x-3">
        <div class="bg-indigo-600 text-white p-2 rounded-lg font-bold text-xl flex items-center justify-center w-10 h-10 shadow">
          <i class="fa-solid fa-brain"></i>
        </div>
        <div>
          <h1 class="font-bold text-slate-900 text-lg leading-tight">AI Feedback Intelligence</h1>
          <p class="text-xs text-slate-500">Milestone 2 &bull; Agent 1 (CrewAI + Gemini + MongoDB)</p>
        </div>
      </div>
      <div class="flex items-center space-x-3">
        <span id="health-badge" class="px-2.5 py-1 text-xs font-semibold rounded-full bg-slate-100 text-slate-600 border">
          Checking backend...
        </span>
        <a href="/docs" target="_blank" class="text-xs bg-slate-100 hover:bg-slate-200 text-slate-700 px-3 py-1.5 rounded-md font-medium transition">
          <i class="fa-solid fa-code mr-1"></i> Swagger Docs
        </a>
      </div>
    </div>
  </header>

  <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">

    <!-- Quick Test Bar & Upload Box Grid -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">

      <!-- Upload Box -->
      <div class="lg:col-span-1 bg-white p-6 rounded-xl border border-slate-200 shadow-sm flex flex-col justify-between">
        <div>
          <div class="flex items-center justify-between mb-3">
            <h2 class="font-semibold text-slate-900 text-sm tracking-wide uppercase flex items-center">
              <i class="fa-solid fa-file-csv text-indigo-600 mr-2 text-base"></i> 1. Upload CSV
            </h2>
            <span class="text-xs text-indigo-600 font-medium bg-indigo-50 px-2 py-0.5 rounded">Any Schema</span>
          </div>
          <p class="text-xs text-slate-500 mb-4">
            Upload CSV with feedback. Standard or custom columns (<code class="text-indigo-600">review_text</code>, <code class="text-indigo-600">comment</code>, etc.) are automatically detected.
          </p>

          <form id="upload-form" class="space-y-4">
            <label class="border-2 border-dashed border-slate-300 hover:border-indigo-500 rounded-lg p-6 text-center block cursor-pointer transition bg-slate-50 hover:bg-indigo-50/20">
              <i class="fa-solid fa-cloud-arrow-up text-3xl text-slate-400 mb-2"></i>
              <span id="file-label" class="block text-xs font-medium text-slate-700 truncate">Click to select CSV</span>
              <span class="block text-[10px] text-slate-400 mt-1">.csv format</span>
              <input type="file" id="csv-file-input" accept=".csv" class="hidden">
            </label>
            <button type="submit" id="upload-btn" class="w-full bg-indigo-600 hover:bg-indigo-700 text-white text-xs font-semibold py-2.5 px-4 rounded-lg shadow-sm transition flex items-center justify-center">
              <i class="fa-solid fa-upload mr-2"></i> Upload & Clean
            </button>
          </form>
        </div>

        <div id="upload-status" class="mt-4 text-xs hidden"></div>
      </div>

      <!-- Quick Single Feedback Tester -->
      <div class="lg:col-span-2 bg-white p-6 rounded-xl border border-slate-200 shadow-sm">
        <div class="flex items-center justify-between mb-3">
          <h2 class="font-semibold text-slate-900 text-sm tracking-wide uppercase flex items-center">
            <i class="fa-solid fa-wand-magic-sparkles text-amber-500 mr-2 text-base"></i> 2. Live Agent 1 Tester
          </h2>
          <span class="text-xs text-amber-600 font-medium bg-amber-50 px-2 py-0.5 rounded">Instant Gemini Analysis</span>
        </div>
        <p class="text-xs text-slate-500 mb-4">
          Type or paste any customer review or complaint below to see Agent 1 determine sentiment, theme, pain point, issue, feature request, intent, product area, keywords, and confidence score.
        </p>

        <div class="space-y-3">
          <div class="flex gap-2">
            <input type="text" id="live-input" value="Payment confirmation is unclear and confirmation screen error occurred during checkout"
              class="flex-1 text-xs border border-slate-300 rounded-lg px-3 py-2.5 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500">
            <button id="live-btn" onclick="testLiveRecord()" class="bg-amber-500 hover:bg-amber-600 text-white text-xs font-semibold px-4 py-2.5 rounded-lg shadow-sm transition flex items-center">
              <i class="fa-solid fa-bolt mr-1.5"></i> Analyze
            </button>
          </div>

          <div id="live-result" class="hidden p-4 rounded-lg bg-slate-50 border border-slate-200 text-xs">
            <!-- Rendered output -->
          </div>
        </div>
      </div>

    </div>

    <!-- Upload Batches & Agent 1 Trigger Section -->
    <div class="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden">
      <div class="px-6 py-4 border-b border-slate-200 flex flex-wrap items-center justify-between gap-4">
        <div>
          <h2 class="font-bold text-slate-900 text-base flex items-center">
            <i class="fa-solid fa-database text-indigo-600 mr-2"></i> 3. Uploaded Batches in MongoDB
          </h2>
          <p class="text-xs text-slate-500">Select a batch to inspect cleaned rows or run Agent 1 full analysis.</p>
        </div>
        <button onclick="loadBatches()" class="text-xs bg-slate-100 hover:bg-slate-200 text-slate-700 px-3 py-1.5 rounded-md font-medium transition flex items-center">
          <i class="fa-solid fa-rotate mr-1.5"></i> Refresh Batches
        </button>
      </div>

      <div class="overflow-x-auto">
        <table class="w-full text-left text-xs text-slate-600">
          <thead class="bg-slate-50 text-slate-700 uppercase font-semibold text-[11px] border-b border-slate-200">
            <tr>
              <th class="px-6 py-3">Batch ID / Filename</th>
              <th class="px-6 py-3">Total Rows</th>
              <th class="px-6 py-3">Cleaned (AI-Ready)</th>
              <th class="px-6 py-3">Quality Score</th>
              <th class="px-6 py-3">AI Agent Status</th>
              <th class="px-6 py-3 text-right">Actions</th>
            </tr>
          </thead>
          <tbody id="batches-table-body" class="divide-y divide-slate-100">
            <tr>
              <td colspan="6" class="px-6 py-8 text-center text-slate-400">Loading batches...</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Full Agent 1 Structured Intelligence View -->
    <div id="analyses-section" class="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden hidden">
      <div class="px-6 py-4 border-b border-slate-200 flex flex-wrap items-center justify-between gap-4 bg-indigo-50/30">
        <div>
          <div class="flex items-center space-x-2">
            <span class="h-2 w-2 rounded-full bg-emerald-500 inline-block"></span>
            <h2 class="font-bold text-slate-900 text-base">
              Agent 1 Analysis Output: <span id="current-batch-name" class="text-indigo-600 font-mono text-sm"></span>
            </h2>
          </div>
          <p class="text-xs text-slate-500 mt-0.5">
            Results saved in MongoDB <code class="bg-white px-1 py-0.5 rounded border text-indigo-700 font-mono">feedback_analyses</code> collection.
          </p>
        </div>
        <div class="flex items-center space-x-2">
          <span id="analysis-count-badge" class="px-2.5 py-1 text-xs font-semibold rounded-full bg-indigo-100 text-indigo-800">
            0 Records Analyzed
          </span>
        </div>
      </div>

      <div class="p-6">
        <div id="analyses-cards-container" class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <!-- Cards injected here -->
        </div>
      </div>
    </div>

    <!-- MongoDB Atlas Connection Guide -->
    <div class="bg-white rounded-xl border border-slate-200 p-6 shadow-sm">
      <h3 class="font-bold text-slate-900 text-sm uppercase tracking-wide flex items-center mb-3">
        <i class="fa-solid fa-leaf text-emerald-600 mr-2 text-base"></i> How to View Collections in MongoDB Atlas
      </h3>
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4 text-xs">
        <div class="p-4 rounded-lg bg-slate-50 border border-slate-200">
          <span class="font-bold text-slate-800 block mb-1">1. Log into Atlas</span>
          <p class="text-slate-500">Go to <a href="https://cloud.mongodb.com" target="_blank" class="text-indigo-600 underline">cloud.mongodb.com</a> and sign in with your MongoDB credentials.</p>
        </div>
        <div class="p-4 rounded-lg bg-slate-50 border border-slate-200">
          <span class="font-bold text-slate-800 block mb-1">2. Browse Collections</span>
          <p class="text-slate-500">Click on <strong>Database</strong> &rarr; your cluster (e.g. <code class="font-mono">Cluster0</code>) &rarr; <strong>Browse Collections</strong>.</p>
        </div>
        <div class="p-4 rounded-lg bg-slate-50 border border-slate-200">
          <span class="font-bold text-slate-800 block mb-1">3. Select Database & Tables</span>
          <p class="text-slate-500">Select database <code class="font-mono text-emerald-700 font-semibold">csv_pipeline_demo</code>. You will see: <code class="font-mono">batches</code>, <code class="font-mono">raw_data</code>, <code class="font-mono">cleaned_data</code>, and <code class="font-mono text-indigo-700 font-semibold">feedback_analyses</code>!</p>
        </div>
      </div>
    </div>

  </main>

  <script>
    // Load health on startup
    async function checkHealth() {
      try {
        const res = await fetch('/health');
        const data = await res.json();
        const el = document.getElementById('health-badge');
        if (data.api === 'ok' && data.mongodb === 'ok') {
          if (data.gemini_configured) {
            el.className = 'px-2.5 py-1 text-xs font-semibold rounded-full bg-emerald-100 text-emerald-800 border border-emerald-300';
            el.innerHTML = '<i class="fa-solid fa-circle-check mr-1"></i> MongoDB: OK | Gemini: Ready';
          } else {
            el.className = 'px-2.5 py-1 text-xs font-semibold rounded-full bg-amber-100 text-amber-800 border border-amber-300';
            el.innerHTML = '<i class="fa-solid fa-triangle-exclamation mr-1"></i> MongoDB: OK | Set GEMINI_API_KEY in .env';
          }
        } else {
          el.className = 'px-2.5 py-1 text-xs font-semibold rounded-full bg-rose-100 text-rose-800 border border-rose-300';
          el.innerHTML = '<i class="fa-solid fa-circle-xmark mr-1"></i> Backend Warning';
        }
      } catch (e) {
        console.error(e);
      }
    }

    // File input label update
    const fileInput = document.getElementById('csv-file-input');
    const fileLabel = document.getElementById('file-label');
    fileInput.addEventListener('change', (e) => {
      if (e.target.files.length > 0) {
        fileLabel.innerText = e.target.files[0].name;
      }
    });

    // Upload form
    document.getElementById('upload-form').addEventListener('submit', async (e) => {
      e.preventDefault();
      if (!fileInput.files.length) {
        alert('Please choose a CSV file first');
        return;
      }

      const btn = document.getElementById('upload-btn');
      const statusBox = document.getElementById('upload-status');
      btn.disabled = true;
      btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin mr-2"></i> Uploading & Cleaning...';
      statusBox.className = 'mt-4 text-xs block p-3 rounded-lg bg-blue-50 text-blue-800 border border-blue-200';
      statusBox.innerText = 'Processing file...';

      const formData = new FormData();
      formData.append('file', fileInput.files[0]);

      try {
        const res = await fetch('/upload-csv', { method: 'POST', body: formData });
        const data = await res.json();
        if (res.ok) {
          statusBox.className = 'mt-4 text-xs block p-3 rounded-lg bg-emerald-50 text-emerald-800 border border-emerald-200';
          statusBox.innerHTML = `<strong>Uploaded!</strong> Batch ID: <code>${data.batch_id}</code> &bull; Cleaned rows: ${data.cleaned_rows_stored}/${data.total_rows}`;
          loadBatches();
        } else {
          statusBox.className = 'mt-4 text-xs block p-3 rounded-lg bg-rose-50 text-rose-800 border border-rose-200';
          statusBox.innerText = data.detail || 'Upload failed.';
        }
      } catch (err) {
        statusBox.className = 'mt-4 text-xs block p-3 rounded-lg bg-rose-50 text-rose-800 border border-rose-200';
        statusBox.innerText = 'Error: ' + err.message;
      } finally {
        btn.disabled = false;
        btn.innerHTML = '<i class="fa-solid fa-upload mr-2"></i> Upload & Clean';
      }
    });

    // Load batches list
    async function loadBatches() {
      const tbody = document.getElementById('batches-table-body');
      tbody.innerHTML = '<tr><td colspan="6" class="px-6 py-6 text-center text-slate-400"><i class="fa-solid fa-spinner fa-spin mr-2"></i> Refreshing batches...</td></tr>';
      try {
        const res = await fetch('/batches');
        const batches = await res.json();
        if (!batches.length) {
          tbody.innerHTML = '<tr><td colspan="6" class="px-6 py-6 text-center text-slate-400">No batches uploaded yet. Upload a CSV above!</td></tr>';
          return;
        }

        tbody.innerHTML = batches.map(b => {
          const aiStatus = b.ai_status || 'NOT_ANALYZED';
          let aiBadge = `<span class="px-2 py-0.5 rounded text-[10px] font-semibold bg-slate-100 text-slate-600">Pending</span>`;
          if (aiStatus === 'COMPLETED') {
            aiBadge = `<span class="px-2 py-0.5 rounded text-[10px] font-semibold bg-emerald-100 text-emerald-800"><i class="fa-solid fa-check mr-1"></i> Analyzed (${b.ai_analyzed_count || 0})</span>`;
          } else if (aiStatus === 'PROCESSING') {
            aiBadge = `<span class="px-2 py-0.5 rounded text-[10px] font-semibold bg-amber-100 text-amber-800"><i class="fa-solid fa-spinner fa-spin mr-1"></i> Processing</span>`;
          }

          return `
            <tr class="hover:bg-slate-50/80 transition">
              <td class="px-6 py-4">
                <div class="font-medium text-slate-900">${b.filename || 'Untitled'}</div>
                <div class="text-[10px] text-slate-400 font-mono">${b._id}</div>
              </td>
              <td class="px-6 py-4 font-semibold text-slate-700">${b.total_rows ?? '-'}</td>
              <td class="px-6 py-4 font-semibold text-emerald-600">${b.cleaned_rows_stored ?? b.cleaned_row_count ?? '-'}</td>
              <td class="px-6 py-4 font-semibold">${b.quality_score ? b.quality_score + '%' : '-'}</td>
              <td class="px-6 py-4">${aiBadge}</td>
              <td class="px-6 py-4 text-right space-x-1">
                <button onclick="runAgent1Batch('${b._id}')" class="bg-indigo-600 hover:bg-indigo-700 text-white px-2.5 py-1 rounded text-xs font-medium transition shadow-xs">
                  <i class="fa-solid fa-play mr-1"></i> Run Agent 1
                </button>
                <button onclick="viewBatchAnalyses('${b._id}', '${b.filename}')" class="bg-slate-100 hover:bg-slate-200 text-slate-700 px-2.5 py-1 rounded text-xs font-medium transition">
                  <i class="fa-solid fa-eye mr-1"></i> View Output
                </button>
              </td>
            </tr>
          `;
        }).join('');
      } catch (err) {
        tbody.innerHTML = `<tr><td colspan="6" class="px-6 py-4 text-center text-rose-500">Failed to load batches: ${err.message}</td></tr>`;
      }
    }

    // Run Agent 1 for batch
    async function runAgent1Batch(batchId) {
      if (!confirm(`Run Agent 1 on batch ${batchId}? Gemini will extract sentiment, theme, pain point, issue, feature request, intent, keywords, and confidence for all records.`)) return;

      const section = document.getElementById('analyses-section');
      section.classList.remove('hidden');
      document.getElementById('current-batch-name').innerText = batchId;
      const container = document.getElementById('analyses-cards-container');
      container.innerHTML = '<div class="col-span-2 text-center py-12 text-slate-500"><i class="fa-solid fa-brain fa-bounce text-3xl text-indigo-600 mb-3 block"></i>Agent 1 is analyzing customer records via Gemini API and storing into MongoDB... Please wait...</div>';

      try {
        const res = await fetch(`/ai/jobs/analyze/${batchId}`, { method: 'POST' });
        const data = await res.json();
        if (res.ok) {
          viewBatchAnalyses(batchId, 'Batch Results');
          loadBatches();
        } else {
          container.innerHTML = `<div class="col-span-2 p-4 rounded bg-rose-50 text-rose-700 text-xs">Analysis Error: ${data.detail || 'Failed'}</div>`;
        }
      } catch (err) {
        container.innerHTML = `<div class="col-span-2 p-4 rounded bg-rose-50 text-rose-700 text-xs">Error: ${err.message}</div>`;
      }
    }

    // View analyses for batch
    async function viewBatchAnalyses(batchId, filename) {
      const section = document.getElementById('analyses-section');
      section.classList.remove('hidden');
      document.getElementById('current-batch-name').innerText = `${filename || ''} (${batchId})`;
      const container = document.getElementById('analyses-cards-container');
      container.innerHTML = '<div class="col-span-2 text-center py-8 text-slate-400"><i class="fa-solid fa-spinner fa-spin mr-2"></i> Loading analyses from MongoDB...</div>';

      try {
        const res = await fetch(`/ai/batches/${batchId}/analyses`);
        const data = await res.json();
        const analyses = data.analyses || [];
        document.getElementById('analysis-count-badge').innerText = `${analyses.length} Records Analyzed`;

        if (!analyses.length) {
          container.innerHTML = `
            <div class="col-span-2 text-center py-12 bg-slate-50 rounded-lg border border-dashed border-slate-300">
              <i class="fa-solid fa-magnifying-glass text-3xl text-slate-300 mb-2 block"></i>
              <p class="text-slate-500 text-xs mb-3">No Agent 1 analysis results found for this batch yet.</p>
              <button onclick="runAgent1Batch('${batchId}')" class="bg-indigo-600 hover:bg-indigo-700 text-white text-xs px-3 py-1.5 rounded font-medium shadow-sm">
                Run Agent 1 Now
              </button>
            </div>
          `;
          return;
        }

        container.innerHTML = analyses.map(item => renderAnalysisCard(item)).join('');
        section.scrollIntoView({ behavior: 'smooth' });
      } catch (err) {
        container.innerHTML = `<div class="col-span-2 p-4 text-xs text-rose-600">Error loading analyses: ${err.message}</div>`;
      }
    }

    // Render single analysis card
    function renderAnalysisCard(item) {
      const a = item.analysis || item;
      const sentiment = (a.sentiment || 'neutral').toLowerCase();
      const intent = a.intent || 'Feedback';

      const sentimentClass = sentiment === 'positive' ? 'badge-positive' : (sentiment === 'negative' ? 'badge-negative' : 'badge-neutral');
      const intentClass = `badge-${intent.toLowerCase()}`;

      const keywordsHtml = (a.keywords || []).map(k =>
        `<span class="bg-slate-100 text-slate-600 text-[10px] px-2 py-0.5 rounded font-mono border border-slate-200">${k}</span>`
      ).join(' ');

      return `
        <div class="bg-white border border-slate-200 hover:border-indigo-300 rounded-xl p-5 shadow-xs hover:shadow-md transition flex flex-col justify-between">
          <div>
            <!-- Feedback Raw Text -->
            <div class="text-slate-800 font-medium text-xs mb-3 bg-slate-50 p-3 rounded-lg border border-slate-100">
              <i class="fa-solid fa-comment-dots text-indigo-500 mr-1.5"></i>
              "${item.feedback_text || a.feedback_text || '-'}"
            </div>

            <!-- Badges Row -->
            <div class="flex flex-wrap gap-2 items-center mb-4">
              <span class="px-2.5 py-0.5 rounded-full text-xs font-bold ${sentimentClass}">
                ${sentiment.toUpperCase()}
              </span>
              <span class="px-2 py-0.5 rounded text-xs font-semibold ${intentClass}">
                ${intent}
              </span>
              <span class="px-2 py-0.5 rounded text-xs font-semibold bg-slate-100 text-slate-700">
                <i class="fa-solid fa-layer-group text-slate-400 mr-1"></i> ${a.theme || 'General'}
              </span>
              <span class="px-2 py-0.5 rounded text-xs font-semibold bg-slate-100 text-slate-700">
                <i class="fa-solid fa-cube text-slate-400 mr-1"></i> ${a.product_area || 'Core'}
              </span>
              <span class="ml-auto text-[11px] font-bold text-slate-500">
                <i class="fa-solid fa-bullseye text-emerald-500 mr-1"></i> ${(a.confidence * 100).toFixed(0)}% Conf
              </span>
            </div>

            <!-- Granular Fields -->
            <div class="space-y-2 text-xs border-t border-slate-100 pt-3">
              ${a.pain_point ? `
                <div class="flex items-start">
                  <span class="text-slate-400 w-24 shrink-0 font-medium">Pain Point:</span>
                  <span class="text-slate-700 font-medium text-rose-700">${a.pain_point}</span>
                </div>
              ` : ''}
              ${a.issue ? `
                <div class="flex items-start">
                  <span class="text-slate-400 w-24 shrink-0 font-medium">Issue / Error:</span>
                  <span class="text-amber-700 font-medium">${a.issue}</span>
                </div>
              ` : ''}
              ${a.feature_request ? `
                <div class="flex items-start">
                  <span class="text-slate-400 w-24 shrink-0 font-medium">Feature Req:</span>
                  <span class="text-indigo-700 font-medium">${a.feature_request}</span>
                </div>
              ` : ''}
              ${a.reasoning ? `
                <div class="flex items-start">
                  <span class="text-slate-400 w-24 shrink-0 font-medium">Reasoning:</span>
                  <span class="text-slate-500 italic">${a.reasoning}</span>
                </div>
              ` : ''}
            </div>
          </div>

          <!-- Keywords & Footer -->
          <div class="mt-4 pt-3 border-t border-slate-100 flex items-center justify-between">
            <div class="flex flex-wrap gap-1 items-center">
              <span class="text-[10px] text-slate-400 mr-1">Keywords:</span>
              ${keywordsHtml}
            </div>
            <span class="text-[10px] font-mono text-slate-300">MongoDB</span>
          </div>
        </div>
      `;
    }

    // Live single tester
    async function testLiveRecord() {
      const input = document.getElementById('live-input');
      const text = input.value.trim();
      if (!text) return;

      const btn = document.getElementById('live-btn');
      const resBox = document.getElementById('live-result');
      btn.disabled = true;
      btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin mr-1"></i> Analyzing...';
      resBox.className = 'block p-4 rounded-lg bg-slate-50 border border-slate-200 text-xs';
      resBox.innerHTML = '<i class="fa-solid fa-spinner fa-spin mr-2 text-indigo-600"></i> Running Agent 1 via CrewAI + Gemini...';

      try {
        const res = await fetch('/ai/analyze-record?save_to_db=true', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ feedback_text: text })
        });
        const data = await res.json();
        if (res.ok) {
          const a = data.analysis;
          resBox.className = 'block p-4 rounded-lg bg-emerald-50/40 border border-emerald-200 text-xs';
          resBox.innerHTML = `
            <div class="flex items-center justify-between pb-2 mb-2 border-b border-emerald-100">
              <div class="flex items-center space-x-2">
                <span class="px-2 py-0.5 rounded text-xs font-bold ${a.sentiment === 'positive' ? 'badge-positive' : (a.sentiment === 'negative' ? 'badge-negative' : 'badge-neutral')}">${a.sentiment.toUpperCase()}</span>
                <span class="px-2 py-0.5 rounded text-xs font-semibold badge-${a.intent.toLowerCase()}">${a.intent}</span>
                <span class="font-semibold text-slate-700">Theme: ${a.theme}</span>
                <span class="text-slate-500 font-medium">Area: ${a.product_area}</span>
              </div>
              <span class="text-xs font-bold text-emerald-700"><i class="fa-solid fa-bullseye mr-1"></i> Confidence: ${(a.confidence * 100).toFixed(0)}%</span>
            </div>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-2 text-slate-700">
              <div><strong>Pain Point:</strong> ${a.pain_point || '<span class="text-slate-400">None</span>'}</div>
              <div><strong>Issue / Bug:</strong> ${a.issue || '<span class="text-slate-400">None</span>'}</div>
              <div><strong>Feature Request:</strong> ${a.feature_request || '<span class="text-slate-400">None</span>'}</div>
              <div><strong>Keywords:</strong> ${(a.keywords || []).join(', ')}</div>
            </div>
            ${a.reasoning ? `<div class="mt-2 text-[11px] text-slate-500 italic"><strong>Reasoning:</strong> ${a.reasoning}</div>` : ''}
            ${data.stored_in_db ? `<div class="mt-2 text-[10px] text-indigo-600 font-mono"><i class="fa-solid fa-check mr-1"></i> Saved in MongoDB: ${data.analysis_id}</div>` : ''}
          `;
        } else {
          resBox.className = 'block p-4 rounded-lg bg-rose-50 border border-rose-200 text-xs text-rose-700';
          resBox.innerText = data.detail || 'Analysis failed.';
        }
      } catch (err) {
        resBox.className = 'block p-4 rounded-lg bg-rose-50 border border-rose-200 text-xs text-rose-700';
        resBox.innerText = 'Error: ' + err.message;
      } finally {
        btn.disabled = false;
        btn.innerHTML = '<i class="fa-solid fa-bolt mr-1.5"></i> Analyze';
      }
    }

    // Init
    checkHealth();
    loadBatches();
  </script>
</body>
</html>
"""


def get_dashboard_html() -> str:
    return DASHBOARD_HTML
