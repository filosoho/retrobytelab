// Quantity increment / decrement
$(document).on("click", ".qty-btn", function () {
  const wrapper = $(this).closest(".qty-stepper");
  const input = wrapper.find("input");

  let value = parseInt(input.val(), 10);

  if ($(this).data("action") === "increment") {
    value++;
  } else if ($(this).data("action") === "decrement" && value > 1) {
    value--;
  }

  input.val(value);
});
