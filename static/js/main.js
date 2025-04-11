// Main JavaScript for Vibe Not Vibing GitHub Profile Viewer

document.addEventListener('DOMContentLoaded', function() {
    // Initialize Bootstrap tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    const tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // GitHub username form validation
    const githubForm = document.getElementById('github-form');
    if (githubForm) {
        githubForm.addEventListener('submit', function(event) {
            const usernameInput = document.getElementById('github_username');
            if (!usernameInput.value.trim()) {
                event.preventDefault();
                
                // Highlight the input field
                usernameInput.classList.add('is-invalid');
                
                // Show validation message if it doesn't exist
                if (!document.querySelector('.invalid-feedback')) {
                    const feedback = document.createElement('div');
                    feedback.className = 'invalid-feedback';
                    feedback.textContent = 'Please enter a GitHub username';
                    usernameInput.parentNode.appendChild(feedback);
                }
            }
        });
        
        // Remove validation message when user starts typing
        const usernameInput = document.getElementById('github_username');
        if (usernameInput) {
            usernameInput.addEventListener('input', function() {
                this.classList.remove('is-invalid');
            });
        }
    }
    
    // Auto-hide flash messages after 5 seconds
    const flashMessages = document.querySelectorAll('.alert');
    flashMessages.forEach(function(message) {
        setTimeout(function() {
            const alert = bootstrap.Alert.getOrCreateInstance(message);
            alert.close();
        }, 5000);
    });
    
    // Repository language bar hover effects
    const languageBars = document.querySelectorAll('.language-bar');
    languageBars.forEach(function(bar) {
        const languageItems = bar.querySelectorAll('.language-item');
        
        languageItems.forEach(function(item) {
            item.addEventListener('mouseenter', function() {
                const languageName = this.getAttribute('title');
                // Add glow effect
                this.style.opacity = '0.8';
                this.style.boxShadow = '0 0 8px ' + getComputedStyle(this).backgroundColor;
            });
            
            item.addEventListener('mouseleave', function() {
                this.style.opacity = '1';
                this.style.boxShadow = 'none';
            });
        });
    });
});