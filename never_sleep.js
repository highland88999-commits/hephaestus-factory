// Never Sleep - Keep Three.js Renderer Active
if ('wakeLock' in navigator) {
  navigator.wakeLock.request('screen').then(lock => {
    // Lock acquired - renderer stays active
  });
}
// Skip frames if tab inactive
document.addEventListener('visibilitychange', () => {
  if (document.hidden) renderer.setAnimationLoop(null);
  else renderer.setAnimationLoop(animate);
});
