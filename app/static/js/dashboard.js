// Sidebar active highlighting
const sidebarLinks = document.querySelectorAll('.sidebar-menu li a');
sidebarLinks.forEach(link => {
  link.addEventListener('click', function() {
    sidebarLinks.forEach(l => l.parentElement.classList.remove('active'));
    this.parentElement.classList.add('active');
  });
});

// Fetch and update dashboard data
document.addEventListener('DOMContentLoaded', () => {
  fetchDashboardData();
  fetchAlerts();
  initCharts();
});

async function fetchDashboardData() {
  try {
    const res = await fetch('/api/dashboard');
    if (!res.ok) throw new Error('Failed to load dashboard data');
    const data = await res.json();
    document.getElementById('total_cases').textContent = data.total_cases;
    document.getElementById('total_recoveries').textContent = data.total_recoveries;
    document.getElementById('active_cases').textContent = data.active_cases;
    document.getElementById('risk_index').textContent = data.risk_index;
    document.getElementById('last_update').textContent = data.last_update;
    document.getElementById('cases_trend').textContent = data.cases_trend;
    document.getElementById('recoveries_trend').textContent = data.recoveries_trend;
    document.getElementById('active_trend').textContent = data.active_trend;
    document.getElementById('risk_trend').textContent = data.risk_trend;
    // AI Predictions
    updateAIPredictions(data.ai_predictions);
  } catch (err) {
    showError('Could not load dashboard data.');
  }
}

function updateAIPredictions(pred) {
  if (!pred) return;
  const aiDiv = document.getElementById('ai_predictions_content');
  aiDiv.innerHTML = `
    <div class="prediction-metric">
      <div class="prediction-header">
        <h4>Outbreak Probability</h4>
        <span class="prediction-badge high">${pred.probability > 70 ? 'High' : 'Moderate'}</span>
      </div>
      <div class="prediction-gauge">
        <div class="gauge-fill" style="width: ${pred.probability}%;"></div>
        <span class="gauge-value">${pred.probability}%</span>
      </div>
    </div>
    <div class="prediction-metric">
      <div class="prediction-header">
        <h4>Est. Peak Date</h4>
        <span class="prediction-date">${pred.peak_date}</span>
      </div>
      <div class="prediction-confidence">
        <span>Confidence: ${pred.confidence}%</span>
      </div>
    </div>
  `;
}

// Fetch and display recent health alerts
async function fetchAlerts() {
  try {
    const res = await fetch('/api/alerts');
    if (!res.ok) throw new Error('Failed to load alerts');
    const data = await res.json();
    const alertsDiv = document.getElementById('outbreaks_content');
    alertsDiv.innerHTML = data.alerts.map(alert => `
      <div class="alert-item">
        <div class="alert-icon ${alert.severity}"><i class="fas fa-exclamation-triangle"></i></div>
        <div class="alert-content">
          <h4>${alert.title}</h4>
          <p>${alert.description}</p>
          <span class="alert-time">${alert.time}</span>
        </div>
        <button class="btn-icon"><i class="fas fa-chevron-right"></i></button>
      </div>
    `).join('');
  } catch (err) {
    showError('Could not load health alerts.');
  }
}

// Chart.js initialization
let trendChart;
function initCharts() {
  fetch('/api/trends')
    .then(res => res.json())
    .then(data => {
      const ctx = document.getElementById('trendChart').getContext('2d');
      trendChart = new Chart(ctx, {
        type: 'line',
        data: data,
        options: {responsive: true}
      });
    })
    .catch(() => showError('Could not load trend data.'));
}

// Search functionality
const searchInput = document.querySelector('.search-container input');
if (searchInput) {
  searchInput.addEventListener('input', function() {
    // Implement search/filter logic here
    // For example, filter alerts or dashboard cards
  });
}

// Error handling
function showError(msg) {
  alert(msg); // Replace with a toast or UI message in production
} 