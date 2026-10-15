// Decorative rotation only: this illustration is not driven by engine data.
const motionButton = document.querySelector('.motion-toggle');
const enginePanel = document.querySelector('.engine-panel');
const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
let paused = reducedMotion.matches;

function updateMotion() {
  enginePanel.classList.toggle('motion-paused', paused);
  motionButton.hidden = reducedMotion.matches;
  motionButton.setAttribute('aria-pressed', String(paused));
  motionButton.textContent = paused ? 'Resume rotation ▶' : 'Pause rotation Ⅱ';
}

if (motionButton && enginePanel) {
  enginePanel.classList.add('motion-ready');
  updateMotion();
  motionButton.addEventListener('click', () => {
    paused = !paused;
    updateMotion();
  });
  reducedMotion.addEventListener('change', () => {
    paused = reducedMotion.matches;
    updateMotion();
  });
}
