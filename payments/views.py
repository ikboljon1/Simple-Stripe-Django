import stripe
from django.conf import settings
from django.http.response import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import TemplateView


class HomePageView(TemplateView):
    template_name = 'home.html'


@csrf_exempt
def stripe_config(request):
    if request.method == 'GET':
        stripe_config = {'publicKey': settings.STRIPE_PUBLISHABLE_KEY}
        return JsonResponse(stripe_config, safe=False)


@csrf_exempt
def create_checkout_session(request):
    if request.method == 'GET':
        domain_url = 'http://localhost:8000/'
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
# Создать новую сессию оформления заказа для заказа
             # Другие необязательные параметры включают:
             # [billing_address_collection] - для отображения информации об адресе выставления счета на странице
             # [клиент] - если у вас есть идентификатор клиента Stripe
             # [payment_intent_data] - позволяет зафиксировать платеж позже
             # [customer_email] - позволяет предварительно заполнить адрес электронной почты в форме
             # Для получения полной информации см. https:#stripe.com/docs/api/checkout/sessions/create

             # ?session_id={CHECKOUT_SESSION_ID} означает, что перенаправление будет иметь идентификатор сеанса, установленный в качестве параметра запроса

             # Если мы хотим идентифицировать пользователя при использовании веб-хуков, мы можем передать client_reference_id для оформления заказа
             # конструктор сеанса. Затем мы сможем получить его и внести изменения в наши модели Django.
             #
             # Если мы предлагаем услугу SaaS, также было бы хорошо разрешить покупку только аутентифицированным пользователям
             # что-нибудь на нашем сайте.
             
            checkout_session = stripe.checkout.Session.create(
                # client_reference_id=request.user.id if request.user.is_authenticated else None,
                success_url=domain_url + 'success?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=domain_url + 'cancelled/',
                payment_method_types=['card'],
                mode='payment',
                line_items=[
                    {
                        'name': 'T-shirt',
                        'quantity': 1,
                        'currency': 'usd',
                        'amount': '2000',
                    }
                ]
            )
            return JsonResponse({'sessionId': checkout_session['id']})
        except Exception as e:
            return JsonResponse({'error': str(e)})


@csrf_exempt
def stripe_webhook(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    endpoint_secret = settings.STRIPE_ENDPOINT_SECRET
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Обработка события checkout.session.completed
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']

        # Этот метод будет вызываться, когда пользователь что-то успешно купит.
        handle_checkout_session(session)

    return HttpResponse(status=200)


def handle_checkout_session(session):
    # client_reference_id = user's id
    client_reference_id = session.get("client_reference_id")
    payment_intent = session.get("payment_intent")

    if client_reference_id is None:
        # Клиент не был авторизован при покупке
        return

    # Клиент вошел в систему, теперь мы можем получить пользователя Django и внести изменения в наши модели.
    try:
        user = User.objects.get(id=client_reference_id)
        print(user.username, "just purchased something.")

        # TODO: внести изменения в наши модели.

    except User.DoesNotExist:
        pass


class SuccessView(TemplateView):
    template_name = 'success.html'


class CancelledView(TemplateView):
    template_name = 'cancelled.html'


@csrf_exempt
def stripe_webhook(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    endpoint_secret = settings.STRIPE_ENDPOINT_SECRET
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Недопустимая payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Неверная подпись
        return HttpResponse(status=400)

   # Обработка события checkout.session.completed
    if event['type'] == 'checkout.session.completed':
        print("Payment was successful.")
        # TODO: запустите здесь некоторый пользовательский код

    return HttpResponse(status=200)
