document.getElementById('intake-form').addEventListener('submit', function (event) {
  event.preventDefault();
  const fields = new FormData(event.currentTarget);
  const formats = ['Retainer and intensive', 'Subsidized Stewardship Subscription', 'Fixed project commission', 'Institutional advisory'];
  const selected = String(fields.get('format') || '').trim();
  const format = formats.includes(selected) ? selected : '';
  const prompts = [['message', 'Message'], ['work', 'Work'], ['name', 'Name']];
  const lines = prompts.map(([key, label]) => {
    const value = String(fields.get(key) || '').trim();
    return value ? label + ': ' + value : '';
  }).filter(Boolean);
  if (format) lines.unshift('Engagement format: ' + format);
  const destination = 'mailto:info@wildlakestudio.com';
  const subject = format ? 'Wild-Lake inquiry: ' + format : 'Wild-Lake: Let’s begin';
  const query = lines.length ? '?subject=' + encodeURIComponent(subject) + '&body=' + encodeURIComponent(lines.join('\n\n')) : '';
  window.location.href = destination + query;
  document.getElementById('intake-status').textContent = 'Your email app will open a draft. Review and send it there, or use the email link above.';
});
