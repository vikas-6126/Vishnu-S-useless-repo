document.addEventListener("DOMContentLoaded", () => {
  const input = document.getElementById("passwordInput");
  const bar = document.getElementById("strengthBar");
  const label = document.getElementById("strengthLabel");
  if (!input) return;

  let timer;
  input.addEventListener("input", () => {
    clearTimeout(timer);
    const value = input.value;
    if (!value) {
      bar.style.width = "0%";
      label.textContent = "Strength: Not checked";
      return;
    }
    timer = setTimeout(async () => {
      try {
        const response = await fetch("/api/password-strength", {
          method: "POST",
          headers: {"Content-Type": "application/json"},
          body: JSON.stringify({password: value})
        });
        const data = await response.json();
        const percent = Math.min(100, Math.round((data.score / 6) * 100));
        bar.style.width = percent + "%";
        label.textContent = "Strength estimate: " + data.label;
      } catch {
        label.textContent = "Unable to check strength. Try again.";
      }
    }, 180);
  });
});
