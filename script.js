document.addEventListener('DOMContentLoaded', function() {

    // --- Mobile Menu Logic ---
    const mobileMenuButton = document.getElementById('mobile-menu-button');
    const mobileMenu = document.getElementById('mobile-menu');
    if (mobileMenuButton) {
        mobileMenuButton.addEventListener('click', () => mobileMenu.classList.toggle('hidden'));
    }

    // --- Tabs & Accordion Logic (for bot.html) ---
    const problemTabs = document.querySelectorAll('.problem-tab');
    if (problemTabs.length > 0) {
        const solutionContents = document.querySelectorAll('.solution-content');
        problemTabs.forEach(tab => {
            tab.addEventListener('click', () => {
                const targetId = tab.dataset.tab;
                problemTabs.forEach(t => {
                    t.classList.remove('tab-active');
                    t.classList.add('tab-inactive');
                });
                tab.classList.replace('tab-inactive', 'tab-active');
                solutionContents.forEach(c => c.id === targetId ? c.classList.remove('hidden') : c.classList.add('hidden'));
            });
        });
    }

    const faqQuestions = document.querySelectorAll('.faq-question');
    if (faqQuestions.length > 0) {
        faqQuestions.forEach(question => {
            question.addEventListener('click', () => {
                const answer = question.nextElementSibling;
                const arrow = question.querySelector('.arrow-down');
                const isOpening = !answer.style.maxHeight || answer.style.maxHeight === '0px';

                // Close all other accordions before opening the new one
                faqQuestions.forEach(q => {
                    if (q !== question) {
                        q.nextElementSibling.style.maxHeight = '0px';
                        if (q.querySelector('.arrow-down')) q.querySelector('.arrow-down').classList.remove('rotated');
                    }
                });

                if (isOpening) {
                    answer.style.maxHeight = answer.scrollHeight + 'px';
                    if (arrow) arrow.classList.add('rotated');
                } else {
                    answer.style.maxHeight = '0px';
                    if (arrow) arrow.classList.remove('rotated');
                }
            });
        });
    }

    // --- Gemini AI Consultant Logic ---
    const askAiButton = document.getElementById('ask-ai-button');
    if (askAiButton) {
        const aiQuestionInput = document.getElementById('ai-question');
        const aiResponseContainer = document.getElementById('ai-response-container');
        const aiResponseDiv = document.getElementById('ai-response');

        // A mock set of rules for the AI to use as context.
        const projectRules = `
Устав сообщества Honji Review (контекст для ИИ):
1. Общие положения:
   1.1. Все участники обязаны уважать друг друга. Оскорбления и переход на личности запрещены.
   1.2. Публикация NSFW-контента строго запрещена.
   1.3. Реклама сторонних ресурсов без согласования с администрацией запрещена.
2. Правила публикаций:
   2.1. Все обзоры должны быть оригинальными. Плагиат карается баном.
   2.2. Обзор должен содержать минимум 300 слов и 2 уникальных изображения.
   2.3. Заголовок должен быть информативным и не содержать кликбейт.
3. Апелляции:
   3.1. Пользователь может подать апелляцию на решение модератора в течение 48 часов.
   3.2. Апелляция рассматривается независимым ИИ-арбитром. Решение ИИ является окончательным, если оно не противоречит уставу.
`;

        /**
         * Calls the Gemini API with a given prompt and handles retries with exponential backoff.
         * @param {string} prompt The complete prompt to send to the API.
         * @returns {Promise<string>} The text response from the AI.
         */
        const callGeminiAPI = async (prompt) => {
            let delay = 1000; // Initial delay of 1 second
            for (let i = 0; i < 5; i++) { // Retry up to 5 times
                try {
                    const apiKey = ""; // The API key is injected by the execution environment.
                    const apiUrl = `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-05-20:generateContent?key=${apiKey}`;

                    const payload = {
                        contents: [{
                            role: "user",
                            parts: [{ text: prompt }]
                        }]
                    };

                    const response = await fetch(apiUrl, {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify(payload)
                    });

                    if (response.ok) {
                        const result = await response.json();
                        if (result.candidates && result.candidates.length > 0 &&
                            result.candidates[0].content && result.candidates[0].content.parts &&
                            result.candidates[0].content.parts.length > 0) {
                            return result.candidates[0].content.parts[0].text;
                        } else {
                            // If the response structure is valid but empty, treat it as an error to trigger retry.
                            throw new Error("Invalid response structure from API");
                        }
                    } else if (response.status === 429 || response.status >= 500) {
                        // For throttling or server errors, wait and retry.
                        await new Promise(resolve => setTimeout(resolve, delay));
                        delay *= 2; // Double the delay for the next retry.
                    } else {
                        // For other client-side errors (e.g., 400 Bad Request), don't retry.
                        const errorResult = await response.json();
                        throw new Error(errorResult.error.message || `API request failed with status ${response.status}`);
                    }
                } catch (error) {
                    if (i === 4) { // If this was the last attempt
                        console.error("Error calling Gemini API after multiple retries:", error);
                        return `Произошла ошибка при обращении к ИИ. Пожалуйста, попробуйте еще раз позже. (${error.message})`;
                    }
                    // Wait before the next retry
                    await new Promise(resolve => setTimeout(resolve, delay));
                    delay *= 2;
                }
            }
            return "Не удалось получить ответ от ИИ после нескольких попыток.";
        };

        askAiButton.addEventListener('click', async () => {
            const question = aiQuestionInput.value.trim();
            if (!question) {
                // Display a message in the response box instead of using alert().
                aiResponseContainer.classList.remove('hidden');
                aiResponseDiv.textContent = 'Пожалуйста, введите ваш вопрос в поле выше.';
                return;
            }

            // --- UI update: Show loading state ---
            aiResponseContainer.classList.remove('hidden');
            aiResponseDiv.innerHTML = '<div class="flex items-center justify-center p-4"><div class="animate-spin rounded-full h-8 w-8 border-b-2 border-red-500"></div></div>';
            askAiButton.disabled = true;
            askAiButton.textContent = 'Обработка...';

            // --- Construct the prompt for the Gemini API ---
            const fullPrompt = `${projectRules}\n\nВопрос пользователя: "${question}"\n\nОтветь на вопрос пользователя, основываясь строго на приведенном выше уставе. Будь краток и ясен.`;

            // --- Call the API and get the response ---
            const responseText = await callGeminiAPI(fullPrompt);

            // --- UI update: Display response and restore button ---
            aiResponseDiv.textContent = responseText;
            askAiButton.disabled = false;
            askAiButton.textContent = 'Задать вопрос';
        });
    }
});
