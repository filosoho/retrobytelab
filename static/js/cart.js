// CSRF helper (Django safe)
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let cookie of cookies) {
      cookie = cookie.trim();
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

const csrftoken = getCookie("csrftoken");

// ADD TO CART
$(document).on("click", "#add-button", function (e) {
  e.preventDefault();

  $.ajax({
    type: "POST",
    url: "/cart/add/",
    data: {
      product_id: $("#add-button").val(),
      product_quantity: $("#qty-input").val(),
      csrfmiddlewaretoken: csrftoken,
      action: "post",
    },
    success: function (json) {
      $("#cart-qty").text(json.qty);
    },
  });
});

// UPDATE CART
$(document).on("click", ".update-button", function (e) {
  e.preventDefault();

  const productId = $(this).data("index");

  $.ajax({
    type: "POST",
    url: "/cart/update/",
    data: {
      product_id: productId,
      product_quantity: $("#qty-" + productId).val(),
      csrfmiddlewaretoken: csrftoken,
      action: "post",
    },
    success: function (json) {
      location.reload();
    },
  });
});

// DELETE FROM CART
$(document).on("click", ".fa-trash", function (e) {
  e.preventDefault();

  $.ajax({
    type: "POST",
    url: "/cart/delete/",
    data: {
      product_id: $(this).data("index"),
      csrfmiddlewaretoken: csrftoken,
      action: "post",
    },
    success: function () {
      location.reload();
    },
  });
});
