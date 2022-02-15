import json,stripe
from django.http import HttpResponse
from applications.order.models import Order
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from applications.order.views import render_to_pdf
from django.conf import settings
from .cart import Cart

@csrf_exempt
def webhook(request):
    payload = request.body
    event = None

    stripe.api_key = settings.STRIPE_API_KEY_HIDDEN

    try:
        event = stripe.Event.construct_from(
        json.loads(payload), stripe.api_key
        )
    except ValueError as e:
        return HttpResponse(status=400)

    # Handle the event
    if event.type == 'payment_intent.succeeded':
        payment_intent = event.data.object 

        print('payment_intent:',payment_intent.id)

        order = Order.objects.get(payment_intent= payment_intent.id)
        order.paid = True
        order.save()

        for item in order.items.all():
            product = item.product
            product.num_available = product.num_available - item.quantity
            product.save()

        subject = 'order_confirmation'
        text_content = 'Your Order has been sent!'
        from_email = settings.EMAIL_HOST_USER
        to = ['sivaganeshcsetec20@gmail.com',order.email]

        html_content = render_to_string('order_confirmation.html',{'order':order})
        pdf = render_to_pdf('order_pdf.html',{'order':order})

        msg = EmailMultiAlternatives(subject, text_content, from_email, to)
        msg.attach_alternative(html_content, "text/html")

        if pdf:
            name = 'order_%s.pdf' % order.id
            msg.attach(name,pdf,'applications/pdf')
        
        msg.send()
        print('msg_sent') 

    

        '''send_mail(
            'order_confirmation',
            'Your Order has been sent!',
            'sivag0503@gmail.com',
            ['kathikamani11@gmail.com',order.email],
            fail_silently=False,
            html_message=html)'''

    return HttpResponse(status=200)