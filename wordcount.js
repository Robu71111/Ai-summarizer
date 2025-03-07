// wordcount.js
document.addEventListener('DOMContentLoaded', function() {
    const userTextArea = document.getElementById('user_text');
    const wordCountLabel = document.getElementById('wordCountLabel');
  
    function updateWordCount(text) {
      const words = text.trim().split(/\s+/).filter(Boolean).length;
      const sentences = text.split(/[.!?]+/).filter(Boolean).length;
      wordCountLabel.textContent = `${sentences} sentences • ${words} words`;
    }
  
    userTextArea.addEventListener('input', () => {
      updateWordCount(userTextArea.value);
    });
  });
  