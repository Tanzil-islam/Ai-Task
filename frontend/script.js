// Global variables
let currentTask = 'qa';
let authToken = null;

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    selectTask('qa');
});

// Authentication function
async function authenticateUser() {
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const statusElement = document.getElementById('auth-status');
    
    if (!username || !password) {
        showStatus('Please enter both username and password', 'error');
        return;
    }
    
    try {
        const response = await fetch('/token', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                username: username,
                password: password
            })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            authToken = data.access_token;
            showStatus('✅ Authentication successful! Token saved.', 'success');
        } else {
            showStatus(`❌ Authentication failed: ${data.detail}`, 'error');
        }
    } catch (error) {
        showStatus(`❌ Authentication error: ${error.message}`, 'error');
    }
}

// Show status messages
function showStatus(message, type) {
    const statusElement = document.getElementById('auth-status');
    statusElement.textContent = message;
    statusElement.className = `status-message ${type}`;
    statusElement.style.display = 'block';
    
    // Auto-hide after 5 seconds
    setTimeout(() => {
        statusElement.style.display = 'none';
    }, 5000);
}

// Task selection
function selectTask(taskType) {
    currentTask = taskType;
    
    // Update active button
    document.querySelectorAll('.task-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    event.target.classList.add('active');
    
    // Show corresponding form
    document.querySelectorAll('.task-form').forEach(form => {
        form.classList.remove('active');
    });
    document.getElementById(`${taskType.replace('_', '-')}-form`).classList.add('active');
}

// Execute the selected task
async function executeTask() {
    const loadingElement = document.getElementById('loading');
    const resultsElement = document.getElementById('results-content');
    
    // Show loading indicator
    loadingElement.style.display = 'block';
    resultsElement.innerHTML = '<p class="placeholder">Processing...</p>';
    
    try {
        let requestBody = { task: currentTask };
        
        // Prepare request body based on task type
        switch (currentTask) {
            case 'qa':
                const question = document.getElementById('question-input').value.trim();
                if (!question) {
                    throw new Error('Please enter a question');
                }
                requestBody.question = question;
                break;
                
            case 'generate_image':
                const imagePrompt = document.getElementById('image-prompt').value.trim();
                if (!imagePrompt) {
                    throw new Error('Please enter an image description');
                }
                requestBody.prompt = imagePrompt;
                break;
                
            case 'generate_content':
                const contentPrompt = document.getElementById('content-prompt').value.trim();
                const platform = document.getElementById('platform-select').value;
                if (!contentPrompt) {
                    throw new Error('Please enter content topic');
                }
                requestBody.prompt = contentPrompt;
                requestBody.platform = platform;
                break;
                
            case 'fetch_latest':
                // No additional parameters needed
                break;
                
            default:
                throw new Error('Unknown task type');
        }
        
        // Prepare headers
        const headers = {
            'Content-Type': 'application/json'
        };
        
        // Add authorization header if token exists
        if (authToken) {
            headers['Authorization'] = `Bearer ${authToken}`;
        }
        
        // Make API request
        const response = await fetch('/ai-task', {
            method: 'POST',
            headers: headers,
            body: JSON.stringify(requestBody)
        });
        
        const data = await response.json();
        
        // Hide loading indicator
        loadingElement.style.display = 'none';
        
        // Display results
        if (data.success) {
            displayResults(data);
        } else {
            resultsElement.innerHTML = `
                <div class="result-item">
                    <h5>❌ Error</h5>
                    <p>${data.message}</p>
                </div>
            `;
        }
        
    } catch (error) {
        loadingElement.style.display = 'none';
        resultsElement.innerHTML = `
            <div class="result-item">
                <h5>❌ Request Failed</h5>
                <p>${error.message}</p>
            </div>
        `;
    }
}

// Display results based on task type
function displayResults(data) {
    const resultsElement = document.getElementById('results-content');
    let html = '';
    
    switch (data.task) {
        case 'qa':
            html = `
                <div class="result-item">
                    <h5>❓ Question</h5>
                    <p>${data.data.question}</p>
                </div>
                <div class="result-item">
                    <h5>💡 Answer</h5>
                    <p>${data.data.answer}</p>
                </div>
                <div class="result-item">
                    <h5>📊 Details</h5>
                    <p><strong>ID:</strong> ${data.data.id}</p>
                    <p><strong>Timestamp:</strong> ${data.data.timestamp}</p>
                    ${data.data.mcp_enhancement ? `<p><strong>MCP Enhancement:</strong> ${data.data.mcp_enhancement}</p>` : ''}
                    ${data.data.note ? `<p><strong>Note:</strong> ${data.data.note}</p>` : ''}
                </div>
            `;
            break;
            
        case 'fetch_latest':
            if (data.data.found) {
                html = `
                    <div class="result-item">
                        <h5>📤 Latest Q&A Retrieved</h5>
                        <p><strong>Question:</strong> ${data.data.qa.question}</p>
                        <p><strong>Answer:</strong> ${data.data.qa.answer}</p>
                        <p><strong>ID:</strong> ${data.data.qa.id}</p>
                        <p><strong>Timestamp:</strong> ${data.data.qa.timestamp}</p>
                    </div>
                `;
            } else {
                html = `
                    <div class="result-item">
                        <h5>📭 No Data Found</h5>
                        <p>${data.data.message}</p>
                    </div>
                `;
            }
            break;
            
        case 'generate_image':
            html = `
                <div class="result-item">
                    <h5>🎨 Generated Image</h5>
                    <p><strong>Prompt:</strong> ${data.data.prompt}</p>
                    ${data.data.image_url ? `<img src="${data.data.image_url}" alt="Generated Image" style="max-width: 100%; height: auto; border-radius: 8px; margin-top: 10px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);">` : ''}
                    ${data.data.image_base64 ? `<img src="${data.data.image_base64}" alt="Generated Image" style="max-width: 100%; height: auto; border-radius: 8px; margin-top: 10px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);">` : ''}
                    ${data.data.service ? `<p><strong>Service:</strong> <span style="background: #e2e8f0; padding: 2px 6px; border-radius: 4px; font-size: 12px;">${data.data.service}</span></p>` : ''}
                    ${data.data.note ? `<p><strong>Note:</strong> <em>${data.data.note}</em></p>` : ''}
                    ${data.data.mcp_info ? `<p><strong>MCP Info:</strong> ${data.data.mcp_info}</p>` : ''}
                </div>
            `;
            break;
            
        case 'generate_content':
            html = `
                <div class="result-item">
                    <h5>✍️ Generated Content for ${data.data.platform.charAt(0).toUpperCase() + data.data.platform.slice(1)}</h5>
                    <p><strong>Original Prompt:</strong> ${data.data.prompt}</p>
                    
                    <div style="background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); padding: 20px; border-radius: 10px; margin: 15px 0; border-left: 4px solid #28a745; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                        <strong style="color: #155724;">📝 Generated Content:</strong>
                        <div style="margin-top: 10px; line-height: 1.6; white-space: pre-wrap;">${data.data.content}</div>
                    </div>
                    
                    ${data.data.guidelines_used ? `
                        <details style="margin-top: 15px; background: #f1f3f4; padding: 15px; border-radius: 8px;">
                            <summary style="cursor: pointer; font-weight: bold; color: #495057; padding: 5px 0;">
                                📋 Platform Guidelines Applied
                            </summary>
                            <div style="margin-top: 10px;">
                                <div style="display: grid; gap: 8px; margin-top: 10px;">
                                    <div><strong>Tone:</strong> <span style="background: #fff; padding: 2px 8px; border-radius: 4px; margin-left: 5px;">${data.data.guidelines_used.tone || 'N/A'}</span></div>
                                    <div><strong>Length:</strong> <span style="background: #fff; padding: 2px 8px; border-radius: 4px; margin-left: 5px;">${data.data.guidelines_used.length || 'N/A'}</span></div>
                                    <div><strong>Features:</strong> <span style="background: #fff; padding: 2px 8px; border-radius: 4px; margin-left: 5px;">${data.data.guidelines_used.features || 'N/A'}</span></div>
                                    <div><strong>Hashtags:</strong> <span style="background: #fff; padding: 2px 8px; border-radius: 4px; margin-left: 5px;">${data.data.guidelines_used.hashtags || 'N/A'}</span></div>
                                    <div><strong>Call to Action:</strong> <span style="background: #fff; padding: 2px 8px; border-radius: 4px; margin-left: 5px;">${data.data.guidelines_used.call_to_action || 'N/A'}</span></div>
                                </div>
                            </div>
                        </details>
                    ` : ''}
                    
                    ${data.data.mcp_optimization ? `
                        <div style="background: #d4edda; border: 1px solid #c3e6cb; color: #155724; padding: 10px; border-radius: 6px; margin-top: 10px;">
                            <strong>🔧 MCP Optimization:</strong> ${data.data.mcp_optimization}
                        </div>
                    ` : ''}
                    
                    ${data.data.note ? `
                        <div style="background: #fff3cd; border: 1px solid #ffeaa7; color: #856404; padding: 10px; border-radius: 6px; margin-top: 10px;">
                            <strong>ℹ️ Note:</strong> ${data.data.note}
                        </div>
                    ` : ''}
                </div>
            `;
            break;
            
        default:
            html = `
                <div class="result-item">
                    <h5>📊 Task Results</h5>
                    <div style="background: #2d3748; color: #e2e8f0; padding: 15px; border-radius: 8px; font-family: 'Courier New', monospace; overflow-x: auto; margin-top: 10px;">
                        <pre style="margin: 0; white-space: pre-wrap; word-wrap: break-word;">${JSON.stringify(data.data, null, 2)}</pre>
                    </div>
                </div>
            `;
            break;
    }
    
    // Add a copy button for each result
    html += `
        <div style="text-align: center; margin-top: 20px;">
            <button onclick="copySpecificResult('${data.task}')" style="background: #6c757d; color: white; border: none; padding: 8px 16px; border-radius: 6px; cursor: pointer; font-size: 14px; transition: background 0.3s ease;">
                📋 Copy ${data.task.charAt(0).toUpperCase() + data.task.slice(1)} Result
            </button>
        </div>
    `;
    
    resultsElement.innerHTML = html;
}

// Helper function to copy specific result
function copySpecificResult(taskType) {
    const resultsContent = document.getElementById('results-content');
    const textToCopy = resultsContent.innerText;
    
    if (navigator.clipboard) {
        navigator.clipboard.writeText(textToCopy).then(() => {
            showStatus(`✅ ${taskType.charAt(0).toUpperCase() + taskType.slice(1)} result copied to clipboard!`, 'success');
        }).catch(() => {
            showStatus('❌ Failed to copy to clipboard', 'error');
        });
    } else {
        // Fallback for older browsers
        const textArea = document.createElement('textarea');
        textArea.value = textToCopy;
        textArea.style.position = 'fixed';
        textArea.style.left = '-999999px';
        textArea.style.top = '-999999px';
        document.body.appendChild(textArea);
        textArea.focus();
        textArea.select();
        
        try {
            document.execCommand('copy');
            showStatus(`✅ ${taskType.charAt(0).toUpperCase() + taskType.slice(1)} result copied to clipboard!`, 'success');
        } catch (err) {
            showStatus('❌ Failed to copy to clipboard', 'error');
        }
        
        document.body.removeChild(textArea);
    }
}