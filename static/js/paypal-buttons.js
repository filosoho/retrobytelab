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

// PayPal JS SDK
const container = document.getElementById("paypal-button-container");

if (container) {
  const paypalHint = document.getElementById("paypal-hint");
  const rawTotal = container.dataset.cartTotal;
  const CART_TOTAL = parseFloat(rawTotal);

  if (CART_TOTAL && CART_TOTAL > 0) {
    const openCard = () => {
      container.classList.add("card-open");
    };

    function allRequiredFieldsFilled() {
      return Array.from(document.querySelectorAll("input[required]")).every(
        (input) => input.value.trim() !== "",
      );
    }

    const closeCard = () => {
      // keep class for animation, then remove after a short delay
      container.style.transition =
        "background 0.2s ease, padding 0.2s ease, border-radius 0.2s ease";
      container.classList.remove("card-open");

      // delay removing styles to allow smooth animation
      setTimeout(() => {
        container.style.transition = "";
      }, 2500); // match transition duration
    };

    const paypalButtonsComponent = paypal.Buttons({
      // optional styling for buttons
      // https://developer.paypal.com/docs/checkout/standard/customize/buttons-style-guide/
      style: {
        shape: "pill",
        layout: "vertical",
        color: "silver",
        label: "paypal",
      },

      onInit: (data, actions) => {
        const updateState = () => {
          if (allRequiredFieldsFilled()) {
            actions.enable();
            container.classList.remove("is-disabled");
            paypalHint?.classList.add("d-none");
          } else {
            actions.disable();
            container.classList.add("is-disabled");
            paypalHint?.classList.remove("d-none");
          }
        };

        // Initial state (important for logged-in users)
        updateState();

        // Live validation
        document.querySelectorAll("input[required]").forEach((input) => {
          input.addEventListener("input", updateState);
        });
      },

      onClick: (data) => {
        if (data.fundingSource === paypal.FUNDING.CARD) {
          openCard();
        }
      },

      // set up the transaction
      createOrder: (data, actions) => {
        // pass in any options from the v2 orders create call:
        // https://developer.paypal.com/api/orders/v2/#orders-create-request-body
        const createOrderPayload = {
          purchase_units: [
            {
              amount: {
                value: CART_TOTAL,
              },
            },
          ],
        };

        return actions.order.create(createOrderPayload);
      },

      onApprove: (data, actions) => {
        closeCard();

        return actions.order.capture().then((details) => {
          const payerName = details.payer.name.given_name;
          console.log("Transaction completed by", payerName);

          $.ajax({
            type: "POST",
            url: "complete-order",
            data: {
              name: $("#name").val(),
              email: $("#email").val(),
              address1: $("#address1").val(),
              address2: $("#address2").val(),
              city: $("#city").val(),
              state: $("#state").val(),
              zipcode: $("#zipcode").val(),
              csrfmiddlewaretoken: csrftoken,
              action: "post",
            },
            success: function (json) {
              window.location.replace("payment-success");
            },
            error: function (xhr, errmsg, err) {
              console.log("error - failed payment ==> : ", err);
              console.log("errmsg - failed payment ==> : ", errmsg);
              window.location.replace("payment-failed");
            },
          });
        });
      },

      // User closes PayPal / clicks X
      onCancel: () => {
        setTimeout(() => {
          closeCard();
        }, 105);
      },

      onError: (err) => {
        console.error(
          "An error prevented the buyer from checking out with PayPal",
          err,
        );
      },
    });

    paypalButtonsComponent.render("#paypal-button-container").catch((err) => {
      console.error("PayPal Buttons failed to render", err);
    });
  }
} else {
  console.warn("PayPal skipped — container not found");
}
