function copyCode() {
  const codeText = document.getElementById("myCode").innerText;

  if (navigator.clipboard && window.isSecureContext) {
    navigator.clipboard.writeText(codeText);
  } else {
    // Fallback untuk file lokal (file:///)
    const textArea = document.createElement("textarea");
    textArea.value = codeText;
    document.body.appendChild(textArea);
    textArea.select();
    document.execCommand("copy");
    document.body.removeChild(textArea);
  }
}