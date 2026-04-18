// Fade-in cards on page load
document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('#product-grid > div').forEach((card, i) => {
    card.style.opacity = '0';
    setTimeout(() => {
      card.classList.add('fade-in');
      card.style.opacity = '';
    }, i * 60);
  });

  // Auto-dismiss flash messages after 4s
  document.querySelectorAll('[data-alert]').forEach(el => {
    setTimeout(() => {
      el.style.transition = 'opacity 0.5s';
      el.style.opacity = '0';
      setTimeout(() => el.remove(), 500);
    }, 4000);
  });
});

// Quantity stepper helper (product detail page)
function changeQty(delta) {
  const input = document.getElementById('qty-input');
  if (!input) return;
  const max = parseInt(input.max) || 999;
  const newVal = Math.max(1, Math.min(max, parseInt(input.value || 1) + delta));
  input.value = newVal;
}
