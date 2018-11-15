from academy.models import Subscription

def get_subscription(request):
    if request.user.is_authenticated:
        try:
            subscription = Subscription.objects.get(user=request.user)
            # print(subscription[0])
            return { 'sub': subscription }
        except Exception as ex:
            print(ex)
            return { 'sub': None }
    else:
        return { 'sub': None }
