document.addEventListener('DOMContentLoaded', () => {
    const startButton = document.getElementById('start-button');
    const coverPage = document.getElementById('cover-page');
    const mainContent = document.getElementById('main-content');
    
    startButton.addEventListener('click', () => {
        coverPage.style.display = 'none';
        mainContent.style.display = 'block';
    });

    document.getElementById('send-btn').addEventListener('click', async () => {
        const prompt = document.getElementById('setup-textarea').value;

        if (prompt.trim() === "") return;
        
        const userSpeechBubble = document.createElement('div');
        userSpeechBubble.className = 'user-speech-bubble';
        userSpeechBubble.textContent = prompt;

        const chatContainer = document.getElementById('chat-container');
        chatContainer.appendChild(userSpeechBubble);
        document.getElementById('setup-textarea').value = '';
        chatContainer.scrollTop = chatContainer.scrollHeight;

        const response = await fetch('/submit', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ prompt })
        });

        const data = await response.json();
        const aiMessageContainer = document.createElement('div');
        aiMessageContainer.className = 'ai-message';

        const aiSpeechBubble = document.createElement('div');
        aiSpeechBubble.className = 'speech-bubble-ai';
        let responseText = data.response.replace(/\n/g, '<br>');
        aiSpeechBubble.innerHTML = responseText;
        aiMessageContainer.appendChild(aiSpeechBubble);

        chatContainer.appendChild(aiMessageContainer);
        chatContainer.scrollTop = chatContainer.scrollHeight;
    });

    // Image Generation (using OpenAI)
    const imagePromptInput = document.getElementById('image-prompt');
    const generateImageButton = document.getElementById('generate-image-button');
    const imageContainer = document.getElementById('image-container');

    generateImageButton.addEventListener('click', async () => {
        const prompt = imagePromptInput.value;
        if (prompt) {
            // Show loading message
            imageContainer.innerHTML = '<p>Generating image...</p>';

            const response = await fetch('/generate_image', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ prompt })
            });

            const data = await response.json();

            imageContainer.innerHTML = '';

            if (data.image_url) {
                setTimeout(() => {
                    imageContainer.innerHTML = `<img src="${data.image_url}" alt="Generated Image">`;
                }, 5000);
            } else {
                imageContainer.innerHTML = `<p>${data.error || 'Error generating image.'}</p>`;
            }
        } else {
            imageContainer.innerHTML = `<p>Please enter an image prompt.</p>`;
        }
    });
});
