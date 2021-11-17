from django.shortcuts import render, redirect
from General.models import *
from Posts.models import *
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from paymentgateway.models import *



@login_required(login_url='/')
def DashboardView(request):
    my_user = request.user
    if my_user.is_authenticated:  

        profile = Profile.objects.filter(Profile_incomplete=False, user=my_user)
        if profile.exists():
            if profile[0].Account_activated:
                profile_data = Profile.objects.filter(Profile_incomplete=False, user=my_user)
                #1print(profile_data.Avatar.url)
                
                notif=getNotifications(my_user)
                following=profile_data[0].Following.all()
                p = Paginator(following.order_by('username'), 12)
                page_num = request.GET.get('page', 1)
                try:
                    page = p.page(page_num)
                except:
                    pass
                context = {
                    'notifications':notif,
                    'following':page,
                    'profile':profile_data[0]
                }
                return render(request, 'Dashboard/main-dashboard.html', context)
            else:
                return redirect('general:verify')
        else: 
            return redirect('general:profile')   
    else:
        return redirect('general:login') 

@login_required(login_url='/')
def YourSupporting(request):
    my_user = request.user
    if my_user.is_authenticated:  

        profile = Profile.objects.filter(Profile_incomplete=False, user=my_user)
        if profile.exists():
            if profile[0].Account_activated:
                profile_data = Profile.objects.filter(Profile_incomplete=False, user=my_user)
                #1print(profile_data.Avatar.url)
                
                notif=getNotifications(my_user)
                following=profile_data[0].Following.all()
                p = Paginator(following.order_by('username'), 12)
                page_num = request.GET.get('page', 1)
                try:
                    page = p.page(page_num)
                except:
                    pass
                context = {
                    'notifications':notif,
                    'following':page,
                    'profile':profile_data[0]
                }
                return render(request, 'Dashboard/yourSupporting.html', context)
            else:
                return redirect('general:verify')
        else: 
            return redirect('general:profile')   
    else:
        return redirect('general:login') 

@login_required(login_url='/')
def FanpageView(request):
    my_user = request.user
    notif=getNotifications(my_user)
    profile_data = Profile.objects.filter(Profile_incomplete=False, user=my_user)
    fans_qs = profile_data[0].my_followers.all()
    p = Paginator(fans_qs.order_by('username'), 12)
    page_num = request.GET.get('page', 1)
    page = p.page(page_num)
    notif=getNotifications(my_user)
    context = {
        'notifications':notif,
        'profile':profile_data[0],
        'fans':page
        
        }
    if profile_data.exists():
        if profile_data[0].Account_activated:
                
                return render(request, 'Dashboard/Fanpage.html', context)
        else:
                return redirect('general:verify')

    else: 
        return redirect('general:profile')   


@login_required(login_url='/')
def SeachpageView(request):
    my_user = request.user
    notif=getNotifications(my_user)
    profile_data = Profile.objects.filter(Profile_incomplete=False, user=my_user)
    all_profiles= Profile.objects.all()
    print(all_profiles,"ok")
    for i in all_profiles:
        print(i.UserType)
        # if i.UserType=="test":
        #     all_profiles.remove(i)
    query = request.GET.get("q")
    print(query,"o")
    if query:
        all_profiles = all_profiles.filter(Q(username__icontains=query))
        all_profiles = all_profiles.filter(~Q(UserType="test"))
        print(all_profiles)

    # page_num = request.GET.get('page', 1)
    # page = p.page(page_num)
    context= {
        'query':query,
        'profile': profile_data[0],
        'notifications':notif,
        'pagination': False,
        'prof':  all_profiles
    }
    return render(request, 'Dashboard/search.html', context)
    # if profile_data.exists():
    #     if profile_data.Account_activated and profile_data.Mobile_no_activated:
    #             return render(request, 'Dashboard/Search.html',{'notifications':notif,'prof':profile_data})
    #     else:
    #             return redirect('general:verify')
    # else: 
    #     return redirect('general:profile') 
    
@login_required(login_url='/')
def Memberships(request):
    profile_data = Profile.objects.filter(Profile_incomplete=False, user=request.user)
        
    if profile_data.exists():
             my_memberships=Subscriptions.objects.filter(Customer_profile=profile_data[0])
             context = {
             'profile':profile_data[0],
             'my_memberships':my_memberships}
        
                
             return render(request, 'Dashboard/memberships.html', context)
    else:
                return redirect('general:verify')
 


# @login_required(login_url='/')
# def Memberships(request):
#     profile_data = Profile.objects.filter(Profile_incomplete=False, user=request.user)
#     context = {
#         'profile':profile_data[0],
#     }
#     if profile_data.exists():
#         if profile_data[0].Account_activated:
#             return render(request, 'Dashboard/memberships.html', context)
#         else:
#             return redirect('general:verify')
#     else: 
#         return redirect('general:profile')   


@login_required(login_url='/')
def RedeemPage(request):
    profile_data = Profile.objects.filter(Profile_incomplete=False, user=request.user)

    if profile_data.exists():
        if profile_data[0].Account_activated:
            amountRedeemed=AmountRedeemed.objects.filter(User=request.user)
            context = {
                'profile':profile_data[0],
                'amountRedeemed':amountRedeemed
            }
            return render(request, 'Dashboard/redeempage.html', context)
        else:
            return redirect('general:verify')
    else: 
        return redirect('general:profile')   
    

def getNotifications(for_user):
    profile=Profile.objects.filter(username=for_user)[0]    
    
    notifications=Notification.objects.filter(Send_to__in=[profile.user])
    
    
    return notifications
    