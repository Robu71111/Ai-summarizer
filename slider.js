document.addEventListener('DOMContentLoaded', function() {
    const lengthRange = document.getElementById('lengthRange');
    const lengthInput = document.getElementById('lengthInput');
    const lengthLabel = document.getElementById('lengthLabel');
  
    function updateLabel(val) {
      if (val === '1') lengthLabel.textContent = 'Short';
      else if (val === '3') lengthLabel.textContent = 'Long';
      else lengthLabel.textContent = 'Medium';
    }
  
    updateLabel(lengthRange.value);
  
    lengthRange.addEventListener('input', (e) => {
      lengthInput.value = e.target.value;
      updateLabel(e.target.value);
    });
  });
  