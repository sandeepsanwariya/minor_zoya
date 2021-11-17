from django.shortcuts import render
from .models import *
from Posts.models import ImageTrace
from General.models import Profile
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator


@login_required(login_url='/')
def StoreView(request):
    my_user = request.user
    profile=Profile.objects.get(user=my_user, Profile_incomplete=False)
    if profile.Account_activated:
        trace=ImageTrace.objects.filter(User=my_user,type='products')
        if not trace.exists():
                        trace=ImageTrace.objects.create(User=my_user,type='products')
                        trace.save()
        else:
            trace.update(Last_Image_Upload="",Current_Image="")
        context = {
            'id':profile.Id,
            'profile':profile,
            'visitor':request.user
        }
        return render(request, 'Store/store.html', context)
    else:
        return redirect('general:verify')


def AllProductsView(request):
    my_user = request.user
    #If you want to know if the user is logged in
    is_user_logged = my_user.is_authenticated
    profile=Profile.objects.get(user=my_user, Profile_incomplete=False)
    if is_user_logged:
        items=StoreItem.objects.filter(User=my_user,Published=False)
        print("------------------------------")
        print(items)
        p = Paginator(items.order_by('-Created_on'), 9)
        page_num = request.GET.get('page', 1)
        page = p.page(page_num)
        context={
            "products": items,
            "pagination": page,
            "profile":profile,
             'visitor':request.user
        }

        return render(request,'Store/allitems.html', context)
