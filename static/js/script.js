document.addEventListener('DOMContentLoaded', function() {
    // File upload interaction
    const fileInput = document.getElementById('image-upload');
    const fileNameDisplay = document.getElementById('file-name');
    
    if (fileInput && fileNameDisplay) {
        // Display filename when file is selected
        fileInput.addEventListener('change', function() {
            if (this.files && this.files[0]) {
                fileNameDisplay.textContent = this.files[0].name;
                fileNameDisplay.style.color = '#4CAF50';
            } else {
                fileNameDisplay.textContent = 'No file selected';
                fileNameDisplay.style.color = '#666';
            }
        });
        
        // Drag and drop functionality
        const uploadArea = document.querySelector('.upload-area');
        if (uploadArea) {
            // Highlight drop zone when item is dragged over it
            ['dragenter', 'dragover'].forEach(eventName => {
                uploadArea.addEventListener(eventName, highlight, false);
            });
            
            ['dragleave', 'drop'].forEach(eventName => {
                uploadArea.addEventListener(eventName, unhighlight, false);
            });
            
            function highlight(e) {
                e.preventDefault();
                e.stopPropagation();
                uploadArea.style.borderColor = '#4CAF50';
                uploadArea.style.backgroundColor = 'rgba(76, 175, 80, 0.1)';
            }
            
            function unhighlight(e) {
                e.preventDefault();
                e.stopPropagation();
                uploadArea.style.borderColor = '#ccc';
                uploadArea.style.backgroundColor = 'transparent';
            }
            
            // Handle dropped files
            uploadArea.addEventListener('drop', function(e) {
                const dt = e.dataTransfer;
                fileInput.files = dt.files;
                fileInput.dispatchEvent(new Event('change'));
            }, false);
        }
    }
    
    // Add any animations or additional interactions
    const featureCards = document.querySelectorAll('.feature-card');
    featureCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.querySelector('.feature-icon').style.transform = 'scale(1.1)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.querySelector('.feature-icon').style.transform = 'scale(1)';
        });
    });
    
    // Add smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            document.querySelector(this.getAttribute('href')).scrollIntoView({
                behavior: 'smooth'
            });
        });
    });
});