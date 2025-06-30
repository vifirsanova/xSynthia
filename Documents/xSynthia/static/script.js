document.addEventListener('DOMContentLoaded', function() {
    // DOM Elements
    const chatMessages = document.getElementById('chatMessages');
    const userInput = document.getElementById('userInput');
    const sendMessageBtn = document.getElementById('sendMessageBtn');
    const attachFileBtn = document.getElementById('attachFileBtn');
    const fileInput = document.getElementById('fileInput');
    const generateGraphBtn = document.getElementById('generateGraphBtn');
    const samplePrompts = document.querySelectorAll('.prompt-example');
    
    // Settings elements
    const modelSelect = document.getElementById('modelSelect');
    const graphTypeSelect = document.getElementById('graphTypeSelect');
    const visualizationLevelSelect = document.getElementById('visualizationLevelSelect');
    const colorSchemeSelect = document.getElementById('colorSchemeSelect');
    
    // State
    let hasFirstMessage = false;
    
    // Event Listeners
    sendMessageBtn.addEventListener('click', sendMessage);
    userInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });
    
    attachFileBtn.addEventListener('click', function() {
        fileInput.click();
    });
    
    fileInput.addEventListener('change', function() {
        if (fileInput.files.length > 0) {
	    uploadFile(fileInput.files[0]);
        }
    });
    
    generateGraphBtn.addEventListener('click', generateGraph);
    
    // Sample prompt click handlers
    samplePrompts.forEach(prompt => {
        prompt.addEventListener('click', function() {
            userInput.value = this.getAttribute('data-prompt');
            userInput.focus();
        });
    });
    
    // Functions
    function sendMessage() {
        const message = userInput.value.trim();
        if (message === '') return;
        
        // Add user message to chat
        addMessage(message, 'user');
        // Clear input
        userInput.value = '';
        
        // Update placeholder if first message
        if (!hasFirstMessage) {
            hasFirstMessage = true;
            document.querySelector('.message-placeholder').style.display = 'none';
        }
	// Use the fetch API to get the data from Flask
        fetch('/send_message', {
		method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: message })})
		    .then(response => {
			    if (!response.ok) {
				    throw new Error('Network response was not ok');
			    }
			    return response.json();
		    })
		    .then(data => {
			    addMessage(data.message, 'bot');
		    })
		    .catch(error => {
			    console.error('Error fetching data:', error);
		    });
    }
 
    function uploadFile(file) {
        const formData = new FormData();
        formData.append('file', file);
        
        // Show uploading message
        addMessage(`Uploading file: ${file.name}...`, 'user');
        
        fetch('/upload_file', {
            method: 'POST',
            body: formData
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('File upload failed');
            }
            return response.json();
        })
        .then(data => {
            if (data.error) {
                addMessage(`Error processing file: ${data.error}`, 'bot');
            } else if (data.html) {
                const messageDiv = document.createElement('div');
                messageDiv.classList.add('chat-message', 'bot-message', 'graph-message');

		const contentDiv = document.createElement('div');
		contentDiv.classList.add('message-content');
		contentDiv.innerHTML = data.html;
                
                const timeDiv = document.createElement('div');
                timeDiv.classList.add('message-time');
                timeDiv.textContent = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
                
                messageDiv.appendChild(contentDiv);
                messageDiv.appendChild(timeDiv);
                
                chatMessages.appendChild(messageDiv);
                chatMessages.scrollTop = chatMessages.scrollHeight;
                
                addToHistory(`File: ${file.name}`);
            }
        })
        .catch(error => {
            addMessage(`Error uploading file: ${error.message}`, 'bot');
            console.error('Error uploading file:', error);
        });
    }	
    function addMessage(content, sender) {
        const messageDiv = document.createElement('div');
	messageDiv.classList.add('chat-message', `${sender}-message`);
        
        const contentDiv = document.createElement('div');
        contentDiv.classList.add('message-content');
        contentDiv.textContent = content;
        
        const timeDiv = document.createElement('div');
        timeDiv.classList.add('message-time');
        timeDiv.textContent = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
        
        messageDiv.appendChild(contentDiv);
        messageDiv.appendChild(timeDiv);
        
        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
	
	addToHistory(content);
    }
        
    function addToHistory(message) {
        const historyList = document.querySelector('.history-list');
        const emptyHistory = document.querySelector('.history-empty');
        
        if (emptyHistory) {
            emptyHistory.remove();
        }
        
        const historyItem = document.createElement('div');
        historyItem.classList.add('history-item');
        historyItem.textContent = message.length > 50 ? message.substring(0, 50) + '...' : message;
        
        // Add click handler to load history item
        historyItem.addEventListener('click', function() {
            userInput.value = message;
            userInput.focus();
        });
        
        historyList.insertBefore(historyItem, historyList.firstChild);
    }
    
    function generateGraph() {
        const settings = {
            model: modelSelect.value,
            graphType: graphTypeSelect.value,
            visualizationLevel: visualizationLevelSelect.value,
            colorScheme: colorSchemeSelect.value,
            showEdgeLabels: document.getElementById('showEdgeLabels').checked,
            showNodeWeights: document.getElementById('showNodeWeights').checked
        };
    
        fetch('/generate_graph', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(settings)
        })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                addMessage(data.message, 'bot');
            })
            .catch(error => {
                console.error('Error fetching data:', error);
            });
    }
});

