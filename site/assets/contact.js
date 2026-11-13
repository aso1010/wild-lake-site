document.getElementById('intake-form').addEventListener('submit', function (event) {
  event.preventDefault();
  const fields = new FormData(event.currentTarget);
  const prompts = [['message', 'Message'], ['work', 'Work'], ['name', 'Name']];
  const lines = prompts.map(([key, label]) => {
    const value = String(fields.get(key) || '').trim();
    return value ? label + ': ' + value : '';
  }).filter(Boolean);
  const destination = 'mailto:info@wildlakestudio.com';
  const query = lines.length ? '?subject=' + encodeURIComponent('Wild Lake — Let’s begin') + '&body=' + encodeURIComponent(lines.join('\n\n')) : '';
  window.location.href = destination + query;
  document.getElementById('intake-status').textContent = 'Your email app will open a draft. Review and send it there, or use the email link above.';
});
