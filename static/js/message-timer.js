const message = document.getElementById("message-timer");

if (message) {
  const wrapper = message.closest(".message-wrapper");
  const overlay = wrapper.querySelector(".message-overlay");

  setTimeout(() => {
    message.style.opacity = "0";
    overlay.style.opacity = "0";
  }, 2130);

  setTimeout(() => {
    wrapper.remove();
  }, 2400);
}
