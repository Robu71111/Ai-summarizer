// modes.js
document.addEventListener('DOMContentLoaded', function() {
    const modeTabs = document.querySelectorAll('.mode-tab');
    const modeInput = document.getElementById('modeInput');
  
    modeTabs.forEach(tab => {
      tab.addEventListener('click', (e) => {
        e.preventDefault(); // prevent link navigation
        // Remove 'active' from all tabs
        modeTabs.forEach(t => t.classList.remove('active'));
  
        // Add 'active' to clicked tab
        tab.classList.add('active');
  
        // Update hidden input with data-mode
        const selectedMode = tab.getAttribute('data-mode') || 'paragraph';
        modeInput.value = selectedMode;
      });
    });
  });
  