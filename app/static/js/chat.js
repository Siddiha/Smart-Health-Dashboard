// Show/hide chat widget
const chatWidget = document.getElementById('chatWidget');
const showChatBtn = document.getElementById('showChat');
const minimizeChatBtn = document.getElementById('minimizeChat');

if (showChatBtn && chatWidget) {
  showChatBtn.addEventListener('click', () => {
    chatWidget.classList.add('active');
    showChatBtn.style.display = 'none';
    document.getElementById('userMessage').focus();
  });
}
if (minimizeChatBtn && chatWidget) {
  minimizeChatBtn.addEventListener('click', () => {
    chatWidget.classList.remove('active');
    showChatBtn.style.display = 'block';
  });
}

// Send message
const sendBtn = document.getElementById('sendMessage');
const userInput = document.getElementById('userMessage');
const chatMessages = document.getElementById('chatMessages');

function appendMessage(content, sender = 'user') {
  const msgDiv = document.createElement('div');
  msgDiv.className = 'chat-message ' + sender;
  msgDiv.innerHTML = `<div class="message-content">${content}</div><div class="message-time">${new Date().toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})}</div>`;
  chatMessages.appendChild(msgDiv);
  chatMessages.scrollTop = chatMessages.scrollHeight;
}

async function sendMessage() {
  const message = userInput.value.trim();
  if (!message) return;
  appendMessage(message, 'user');
  userInput.value = '';
  try {
    const res = await fetch('/chat', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({message})
    });
    if (!res.ok) throw new Error('Failed to get response');
    const data = await res.json();
    appendMessage(data.response, 'bot');
    // If backend returns dashboard updates, update them
    if (data.dashboard) {
      if (window.fetchDashboardData) fetchDashboardData();
    }
  } catch (err) {
    appendMessage('Sorry, I could not process your request.', 'bot');
  }
}

if (sendBtn && userInput) {
  sendBtn.addEventListener('click', sendMessage);
  userInput.addEventListener('keydown', function(e) {
    if (e.key === 'Enter') sendMessage();
  });
} 