import stripe

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from basket.basket import Basket

@login_required
def BasketView(request):

    basket=Basket(request)
    total=str(basket.get_total_price())
    total=total.replace('.','')
    total=int(total)
    
 

    stripe.api_key = 'sk_test_51NC3oGCtDtbyYHLCDeXUvercuytY1cY1nPIaqnO00wfg3hups91VAl0nqxi3fRMIn2LtVReHzZNO8rEra9UHcHNp00YOefs5ML'
    intent = stripe.PaymentIntent.create(
        amount=total,
        currency='gbp',
        metadata={'userid': request.user.id}
    )

    return render(request,'payment/home.html',{'client_secret':intent.client_secret})



