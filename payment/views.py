from django.conf import settings
from django.shortcuts import redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from .models import Payment_placed
import stripe, os

stripe.api_key = settings.STRIPE_SECRET_KEY
class StripeCheckoutView(APIView):
    def post(self, request):
        data = request.data
        # global quantity
        # quantity = data['quantity']
        
        try:
            #here the  after hiting url the session is created  and the line items contain price id and quantity what you what to 
            # purchase
            checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                        'price': 'price_1LQC6wSATJm7rfeWxygWhohA',  # Here price_id  which is created on the dashboard
                        'quantity':2,
                    },
                ],
                #In which method you what to pay the amount of Product
                payment_method_types=['card', ],
                # here we have get the mode od payment
                mode='payment',  

                # if the payment is successful than it will redirect to home page with successfull pop
                success_url=settings.SITE_URL + '/?success=true&session_id={CHECKOUT_SESSION_ID}',
                # the payment is cancel
                cancel_url=settings.SITE_URL + '/?canceled=true',
            )

        
            return redirect(checkout_session.url)
        except:
            #if the try block is not successfully exeuted that this error will display
            return Response({"error": "Something went wrong while creating payment checkout session"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR
                            )


# using webhook to comppletd the checkout and storing data in database
@csrf_exempt
def stripe_webhook(request):
    payload = request.body  # payload contains all the data that is returned after
    # successful payment
    header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    
    try:
        event = stripe.Webhook.construct_event(
            payload, header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        # Invalid 
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # this will handle the completed checkout session
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']

        #calling a function to store the data in database
        create_order_succssfully(session)

    
    return HttpResponse(status=200)


# Function for  to fetch the data from completed checkout session and also to store the data in badatabse
def create_order_succssfully(session):
    customer_name = session["customer_details"]["name"]
    customer_email = session["customer_details"]["email"]
    order_total = session["amount_total"]
    payment_method = session["payment_method_types"][0]
    

    
    # here storing the data in database
    Payment_placed.objects.create( name=customer_name,  email=customer_email, amount_paid =order_total,py_mode =payment_method)