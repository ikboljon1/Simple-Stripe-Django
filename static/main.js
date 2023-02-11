console.log("Sanity check!");

// Получить Stripe публикуемый ключ
fetch("/config/")
    .then((result) => { return result.json(); })
    .then((data) => {
        // Инициализировать Stripe.js
        const stripe = Stripe(data.publicKey);

        // Обработчик события
        document.querySelector("#submitBtn").addEventListener("click", () => {
            // Получить идентификатор сеанса оформления заказа
            fetch("/create-checkout-session/")
                .then((result) => { return result.json(); })
                .then((data) => {
                    console.log(data);
                    // Перенаправление на Stripe Checkout
                    return stripe.redirectToCheckout({ sessionId: data.sessionId })
                })
                .then((res) => {
                    console.log(res);
                });
        });
    });