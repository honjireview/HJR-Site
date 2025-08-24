document.addEventListener('DOMContentLoaded', () => {
    const chatForm = document.getElementById('chat-form');
    const messageInput = document.getElementById('message-input');
    const chatMessages = document.getElementById('chat-messages');
    const sendButton = document.getElementById('send-button');
    const charCounter = document.getElementById('char-counter');

    const MAX_CHARS = 2000;

    // Auto-resize textarea
    messageInput.addEventListener('input', () => {
        messageInput.style.height = 'auto';
        messageInput.style.height = (messageInput.scrollHeight) + 'px';

        const currentLength = messageInput.value.length;
        charCounter.textContent = `${currentLength} / ${MAX_CHARS}`;
        charCounter.classList.toggle('text-red-400', currentLength > MAX_CHARS);
        sendButton.disabled = currentLength === 0 || currentLength > MAX_CHARS;
    });

    chatForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const question = messageInput.value.trim();
        if (!question || question.length > MAX_CHARS) return;

        // Display user message
        appendMessage(question, 'user');
        messageInput.value = '';
        messageInput.style.height = 'auto';
        charCounter.textContent = `0 / ${MAX_CHARS}`;
        sendButton.disabled = true;

        // Display loading indicator
        appendMessage('', 'bot', true);

        try {
            const response = await fetch('/bot/ai-assistant', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ question: question }),
            });

            const data = await response.json();

            // Remove loading indicator and display bot response
            removeLoadingIndicator();
            if (data.error) {
                appendMessage(data.error, 'bot', false, true);
            } else {
                appendMessage(data.answer, 'bot');
            }

        } catch (error) {
            removeLoadingIndicator();
            appendMessage('Не удалось подключиться к серверу. Пожалуйста, попробуйте позже.', 'bot', false, true);
            console.error('Fetch error:', error);
        }
    });

    function appendMessage(text, sender, isLoading = false, isError = false) {
        const messageWrapper = document.createElement('div');
        messageWrapper.className = `flex items-start gap-3 ${sender === 'user' ? 'justify-end' : ''}`;

        const iconDiv = document.createElement('div');
        iconDiv.className = `font-bold w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0 text-sm ${sender === 'user' ? 'bg-slate-700 text-slate-300' : 'bg-indigo-500/20 text-indigo-300'}`;
        iconDiv.textContent = sender === 'user' ? 'Вы' : 'ИИ';

        const messageDiv = document.createElement('div');
        messageDiv.className = `p-3 rounded-lg max-w-xl text-sm ${sender === 'user' ? 'bg-indigo-600 text-white' : 'bg-slate-800 text-slate-300'}`;

        if (isLoading) {
            messageDiv.innerHTML = '<div class="flex items-center justify-center space-x-2"><div class="w-2 h-2 rounded-full bg-slate-500 animate-pulse"></div><div class="w-2 h-2 rounded-full bg-slate-500 animate-pulse" style="animation-delay: 0.2s;"></div><div class="w-2 h-2 rounded-full bg-slate-500 animate-pulse" style="animation-delay: 0.4s;"></div></div>';
            messageWrapper.id = 'loading-indicator';
        } else {
            messageDiv.textContent = text;
        }

        if (isError) {
            messageDiv.classList.add('bg-red-500/20', 'text-red-300');
        }

        if (sender === 'user') {
            messageWrapper.appendChild(messageDiv);
            messageWrapper.appendChild(iconDiv);
        } else {
            messageWrapper.appendChild(iconDiv);
            messageWrapper.appendChild(messageDiv);
        }

        chatMessages.appendChild(messageWrapper);
        chatMessages.scrollTop = chatMessages.scrollHeight; // Auto-scroll to bottom
    }

    function removeLoadingIndicator() {
        const loadingIndicator = document.getElementById('loading-indicator');
        if (loadingIndicator) {
            loadingIndicator.remove();
        }
    }
});