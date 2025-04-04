document.getElementById("submit").disabled = true;

        const stripe = Stripe('pk_test_51QkVEiQ03ifYEgfTAZa9CN0SaNx6WigSag5wWD1Jh6kyWJm6BMXXYFR2pUjPB0QmHNUP8FM7n5kxnV878Ieecur6005etaGyp3');
        let card;

        // Получаем JWT токен из cookies
        function getJWTToken() {
            const match = document.cookie.match(/access_token=([^;]+)/);
            return match ? match[1] : null;
        }

        // Инициализация Stripe Elements
        const elements = stripe.elements();
        card = elements.create('card', {
            style: {
                base: {
                    color: "#32325d",
                    fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
                    fontSmoothing: "antialiased",
                    fontSize: "16px",
                    "::placeholder": { color: "#aab7c4" }
                },
                invalid: { color: "#fa755a", iconColor: "#fa755a" }
            }
        });
        card.mount('#card-element');

        // Обработчик изменений карты
        card.on('change', (event) => {
            const errorElement = document.getElementById('card-errors');
            errorElement.textContent = event.error ? event.error.message : '';
        });

        // Выбор плана
        function planSelect(name, price, priceId) {
            document.getElementById("plan").textContent = name;
            document.getElementById("price").textContent = price;
            document.getElementById("priceId").textContent = priceId;
            document.getElementById("submit").disabled = false;
        }

        // Отправка формы
        document.getElementById('subscription-form').addEventListener('submit', async (e) => {
            e.preventDefault();
            const submitBtn = document.getElementById("submit");
            submitBtn.disabled = true;

            const jwtToken = getJWTToken();
            if (!jwtToken) {
                showError('Authentication required. Please login.');
                return;
            }

            try {
                // Создаем PaymentMethod
                const { paymentMethod, error } = await stripe.createPaymentMethod({
                    type: 'card',
                    card: card,
                    billing_details: {
                        name: '{{ user.username }}',
                        email: '{{ user.email }}'
                    }
                });

                if (error) throw error;

                // Отправляем запрос на сервер
                const response = await fetch("/create-sub/", {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${jwtToken}`,
                        'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                    },
                    body: JSON.stringify({
                        payment_method: paymentMethod.id,
                        price_id: document.getElementById("priceId").textContent
                    })
                });

                if (!response.ok) {
                    const errorData = await response.json();
                    throw new Error(errorData.error || 'Payment failed');
                }

                window.location.href = '/complete/';
            } catch (error) {
                showError(error.message);
                submitBtn.disabled = false;
            }
        });

        function showError(message) {
            document.getElementById('card-errors').textContent = message;
        }



// document.getElementById("submit").disabled = true;

// // Инициализация Stripe
// const stripe = Stripe('pk_test_51QkVEiQ03ifYEgfTAZa9CN0SaNx6WigSag5wWD1Jh6kyWJm6BMXXYFR2pUjPB0QmHNUP8FM7n5kxnV878Ieecur6005etaGyp3');
// let card;

// // Функция для получения CSRF токена
// function getCSRFToken() {
//     const csrfToken = document.cookie.match(/csrftoken=([^;]+)/);
//     return csrfToken ? csrfToken[1] : null;
// }

// // Инициализация элементов Stripe
// function initStripeElements() {
//     const elements = stripe.elements();
//     const style = {
//         base: {
//             color: "#32325d",
//             fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
//             fontSmoothing: "antialiased",
//             fontSize: "16px",
//             "::placeholder": { color: "#aab7c4" }
//         },
//         invalid: { color: "#fa755a", iconColor: "#fa755a" }
//     };

//     card = elements.create('card', { style });
//     card.mount('#card-element');
    
//     card.on('change', (event) => {
//         const displayError = document.getElementById('card-errors');
//         displayError.textContent = event.error ? event.error.message : '';
//     });
// }

// // Обработчик выбора плана
// function planSelect(name, price, priceId) {
//     document.getElementById("plan").textContent = name;
//     document.getElementById("price").textContent = price;
//     document.getElementById("priceId").textContent = priceId;
//     document.getElementById("submit").disabled = false;
// }

// // Создание платежного метода
// async function createPaymentMethod() {
//     const csrfToken = getCSRFToken();
//     if (!csrfToken) {
//         showError('CSRF token not found');
//         return;
//     }

//     const { paymentMethod, error } = await stripe.createPaymentMethod({
//         type: 'card',
//         card: card,
//         billing_details: { name: '{{user.username}}' }
//     });

//     if (error) {
//         showError(error.message);
//     } else {
//         try {
//             const response = await fetch("/create-sub/", {
//                 method: 'POST',
//                 headers: {
//                     'Content-Type': 'application/json',
//                     'X-CSRFToken': csrfToken,
//                     'X-Requested-With': 'XMLHttpRequest'
//                 },
//                 credentials: 'include',
//                 body: JSON.stringify({
//                     payment_method: paymentMethod.id,
//                     price_id: document.getElementById("priceId").textContent
//                 })
//             });

//             if (!response.ok) {
//                 const errorData = await response.json();
//                 throw new Error(errorData.error || 'Payment failed');
//             }

//             window.location.href = '/complete/';
//         } catch (error) {
//             showError(error.message);
//         }
//     }
// }

// // Показать ошибку
// function showError(message) {
//     const errorElement = document.getElementById('card-errors');
//     errorElement.textContent = message;
//     changeLoadingState(false);
// }

// // Изменение состояния загрузки
// function changeLoadingState(isLoading) {
//     const submitBtn = document.getElementById("submit");
//     const spinner = document.querySelector("#spinner");
//     const buttonText = document.querySelector("#button-text");
    
//     submitBtn.disabled = isLoading;
//     spinner.classList.toggle("hidden", !isLoading);
//     buttonText.classList.toggle("hidden", isLoading);
// }

// // Инициализация
// document.addEventListener('DOMContentLoaded', () => {
//     initStripeElements();
    
//     const paymentForm = document.getElementById('subscription-form');
//     if (paymentForm) {
//         paymentForm.addEventListener('submit', async (e) => {
//             e.preventDefault();
//             changeLoadingState(true);
//             await createPaymentMethod();
//         });
//     }
// });




// document.getElementById("submit").disabled = true;

//         stripeElements();
        
//         function stripeElements() {
//           stripe = Stripe('pk_test_51QkVEiQ03ifYEgfTAZa9CN0SaNx6WigSag5wWD1Jh6kyWJm6BMXXYFR2pUjPB0QmHNUP8FM7n5kxnV878Ieecur6005etaGyp3');
        
//           if (document.getElementById('card-element')) {
//             let elements = stripe.elements();
        
//             // Card Element styles
//             let style = {
//               base: {
//                 color: "#32325d",
//                 fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
//                 fontSmoothing: "antialiased",
//                 fontSize: "16px",
//                 "::placeholder": {
//                   color: "#aab7c4"
//                 }
//               },
//               invalid: {
//                 color: "#fa755a",
//                 iconColor: "#fa755a"
//               }
//             };
        
        
//             card = elements.create('card', { style: style });
        
//             card.mount('#card-element');
        
//             card.on('focus', function () {
//               let el = document.getElementById('card-errors');
//               el.classList.add('focused');
//             });
        
//             card.on('blur', function () {
//               let el = document.getElementById('card-errors');
//               el.classList.remove('focused');
//             });
        
//             card.on('change', function (event) {
//               displayError(event);
//             });
//           }
//           //we'll add payment form handling here
//         }
        
//         function displayError(event) {
         
//           let displayError = document.getElementById('card-errors');
//           if (event.error) {
//             displayError.textContent = event.error.message;
//           } else {
//             displayError.textContent = '';
//           }
//         }

//         function planSelect(name, price, priceId) {
//             var inputs = document.getElementsByTagName('input');
        
//             for(var i = 0; i<inputs.length; i++){
//               inputs[i].checked = false;
//               if(inputs[i].name== name){
        
//                 inputs[i].checked = true;
//               }
//             }
        
//             var n = document.getElementById('plan');
//             var p = document.getElementById('price');
//             var pid = document.getElementById('priceId');
//             n.innerHTML = name;
//             p.innerHTML = price;
//             pid.innerHTML = priceId;
//                 document.getElementById("submit").disabled = false;
//           }

//           let paymentForm = document.getElementById('subscription-form');
//           if (paymentForm) {
        
//             paymentForm.addEventListener('submit', function (evt) {
//               evt.preventDefault();
//               changeLoadingState(true);
        
        
//                 // create new payment method & create subscription
//                 createPaymentMethod({ card });
//             });
//           }

//           function createPaymentMethod({ card }) {

//             // Set up payment method for recurring usage
//             let billingName = '{{user.username}}';
          
//             stripe
//               .createPaymentMethod({
//                 type: 'card',
//                 card: card,
//                 billing_details: {
//                   name: billingName,
//                 },
//               })
//               .then((result) => {
//                 if (result.error) {
//                   displayError(result);
//                 } else {
//                  const paymentParams = {
//                     price_id: document.getElementById("priceId").innerHTML,
//                     payment_method: result.paymentMethod.id,
//                 };
//                 fetch("/create-sub/", {
//                   method: 'POST',
//                   headers: {
//                     'Content-Type': 'application/json',
//                     'X-CSRFToken':'{{ csrf_token }}',
//                   },
//                   credentials: 'same-origin',
//                   body: JSON.stringify(paymentParams),
//                 }).then((response) => {
//                   return response.json(); 
//                 }).then((result) => {
//                   if (result.error) {
//                     // The card had an error when trying to attach it to a customer
//                     throw result;
//                   }
//                   return result;
//                 }).then((result) => {
//                   if (result && result.status === 'active') {
          
//                    window.location.href = '/complete/';
//                   };
//                 }).catch(function (error) {
//                     displayError(result.error.message);
          
//                 });
//                 }
//               });
//           }
          
          
//           var changeLoadingState = function(isLoading) {
//             if (isLoading) {
//               document.getElementById("submit").disabled = true;
//               document.querySelector("#spinner").classList.remove("hidden");
//               document.querySelector("#button-text").classList.add("hidden");
//             } else {
//               document.getElementById("submit").disabled = false;
//               document.querySelector("#spinner").classList.add("hidden");
//               document.querySelector("#button-text").classList.remove("hidden");
//             }
//           };