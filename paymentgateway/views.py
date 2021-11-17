from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
import json,requests
from General.models import *
from .models import *
import uuid
import razorpay
import hmac
import datetime
from Store.models import *
from django.template import loader
from zocaya_new import settings
# from Zocaya.settings import *
from django.core.mail import send_mail


# Create your views here.

@csrf_exempt
def Webhook(request):
    if request.method=="POST":
        print("------------------------+++++-----------------------------")
        signature=request.headers['X-Razorpay-Signature']
        client = razorpay.Client(auth=("rzp_test_J9Lxu7OB8M6GR3", "NOj4sb6Sp0YBIG30XLkwOhOc"))
        payload_body = json.dumps(json.loads(request.body), separators=(',', ':'))
        try:        
            client.utility.verify_webhook_signature(payload_body,signature, "Abrar.786ahmed")
            body=json.loads(request.body)
            event=body['event']
            subscriptionId=body['payload']['subscription']['entity']['id']
            print(event)
            print(subscriptionId)
            if event=='subscription.cancelled' or event=='subscription.completed':
                subscriptionObj=Subscriptions.objects.get(subscriptionId=subscriptionId)
                customer=subscriptionObj.Customer_profile
                creator=subscriptionObj.Creator_profile
                customer.Subscribed.remove(creator.user)
                creator.My_subscribers.remove(customer.user)
                customer.save()
                creator.save()
                subscriptionObj.delete()
                return JsonResponse({"success":True})
            elif event=='subscription.activated':
                subscriptionObj=Subscriptions.objects.get(subscriptionId=subscriptionId)
                customer=subscriptionObj.Customer_profile
                creator=subscriptionObj.Creator_profile
                notification=Notification.objects.create(
                                
                                Message="Congratulation! You Got A New Paid Subscriber " +
                                str(customer.username),
                                Link="/"+str(customer.username)
                            )
                notification.Send_to.add(creator.user)
                notification.save()
                return JsonResponse({"success":True})
            elif event=='subscription.charged':
                subscriptionObj=Subscriptions.objects.get(subscriptionId=subscriptionId)
                customer=subscriptionObj.Customer_profile
                creator=subscriptionObj.Creator_profile
                subscriptionObj.status='active'
                subscriptionObj.save()
                customer.Subscribed.add(creator.user)
                customer.Following.add(creator.user)
                creator.My_subscribers.add(customer.user)
                creator.my_followers.add(customer.user)
                creator.Revenue+=round((subscriptionObj.amount/100)*0.92,2)
                creator.save()
                print("revenue----")
                print(creator.Revenue)
                customer.save()
                notification=Notification.objects.create(
                                
                                Message="You Got A New Subscription Amount Of "+str(round((subscriptionObj.amount/100)*0.92,2))+"/-INR From " +
                                str(customer.username),
                                Link="/"+str(customer.username)
                            )
                notification.Send_to.add(creator.user)
                notification.save()
                return JsonResponse({"success":True})
            elif event=='subscription.pending':
                subscriptionObj=Subscriptions.objects.get(subscriptionId=subscriptionId)
                subscriptionObj.status='pending'
                subscriptionObj.save()
                customer=subscriptionObj.Customer_profile
                creator=subscriptionObj.Creator_profile
                send_mail( "Charge Failed","Hi Zocaya User,\nYour recent payment for "+str(subscriptionObj.Creator.username)+" failed. To avoid having your subscription canceled, please complete the payment to change the linked card at:"+str(subscriptionObj.subscriptionLink)+"\n\nRegards,\nZocaya Team", 'zocayamedia@gmail.com',[customer.user.email] ) 
                return JsonResponse({"success":True})
            elif event=='subscription.halted':
                subscriptionObj=Subscriptions.objects.get(subscriptionId=subscriptionId)
                customer=subscriptionObj.Customer_profile
                creator=subscriptionObj.Creator_profile
                send_mail( "Hi user\nAll Charge Attempts Failed","After Regular attempt and due to payment failure we have to cancelled your subscription Thankyou For Using our service!\nTeam Zocaya", 'zocayamedia@gmail.com',[customer.user.email] )
                url = "https://api.razorpay.com/v1/subscriptions/"+subscriptionId+"/cancel"

                payload = json.dumps({
                "cancel_at_cycle_end": 0
                })
                headers = {
                'Content-Type': 'application/json',
                'Authorization': 'Basic cnpwX3Rlc3RfMms1TXF6VW9pSHFoYm46clNjMzdJUlNtWW1lY3Noa3gwZ3U1cWsw'
                }

                response = requests.request("POST", url, headers=headers, data=payload)
                json_response=response.json()
                if json_response['status']!='cancelled':
                        response = requests.request("POST", url, headers=headers, data=payload)
                        return JsonResponse({"success":True})
                       
                else:  
                        return JsonResponse({"success":True})
            else:
                return JsonResponse({"success":True})    
                
                
                                
                
            
        except:
            return JsonResponse({"success":False})
            
@csrf_exempt
def Subscribe(request,creator_username):

  if request.method=='POST':
    print("-----------------PPPPP------------")    
    if request.user.is_authenticated: #authenticate
        try:
            visitor_profile=Profile.objects.get(user=request.user)
        except:
            return JsonResponse({"response":False})
        creator_profile=Profile.objects.get(username=creator_username)
        if creator_profile.user in visitor_profile.Subscribed.all() or visitor_profile==creator_profile:
            return redirect('/'+creator_username+'/')
        amount=creator_profile.Subscription_price
        require_plan=Plan.objects.filter(amount=amount*100)
        subscription=Subscriptions.objects.filter(Customer_profile=visitor_profile,Creator_profile=creator_profile)
        print(subscription[0].planId,)
        if subscription.exists():
           print("In Exist")
           print({'id':subscription[0].subscriptionId,"name":visitor_profile.Name,"email":visitor_profile.user.email,"phone":str(visitor_profile.Phone_no)})
           return JsonResponse({'id':subscription[0].subscriptionId,"name":visitor_profile.Name,"email":visitor_profile.user.email,"phone":str(visitor_profile.Phone_no)})
        if require_plan.exists(): # Check If Plan Already Exists
                plan_id=require_plan[0].planId
                subs_response=create_subscription(plan_id)
                print(subs_response)
                if subs_response['status'] == 'created':
                        subscription=Subscriptions.objects.create(
                            Customer_profile=visitor_profile,
                            Creator_profile=creator_profile,
                            amount=require_plan[0].amount,
                            subscriptionId=subs_response['id'],
                            planId=subs_response['plan_id'],
                            status=subs_response['status'],
                            subscriptionLink=subs_response['short_url']
                            )

                        subscription.save()
                        print("--------  ++++  ++++  ----")
                        return JsonResponse({'id':subscription.subscriptionId,"name":visitor_profile.Name,"email":visitor_profile.user.email,"phone":str(visitor_profile.Phone_no)})
                        
                      
                else:
                    return JsonResponse(subs_response)
 
        
        
        else : # Create Plan If Not Exists
            plan=Plan.objects.create(
            planName=str(amount)+"plan",
            period="monthly",
            interval=1,
            amount=amount*100,
            description="simple plan for creating subscription using razorpay",
            )
            plan.save()
            url = "https://api.razorpay.com/v1/plans"

            payload = json.dumps({
                "period": plan.period,
                "interval": plan.interval,
                "item": {
                    "name": plan.planName,
                    "amount":plan.amount,
                    "currency": "INR",
                    "description": plan.description
                }
                })
            headers = {
                'Content-Type': 'application/json',
                'Authorization': 'Basic    cnpwX3Rlc3RfMms1TXF6VW9pSHFoYm46clNjMzdJUlNtWW1lY3Noa3gwZ3U1cWsw'
            }

            response = requests.request("POST", url, headers=headers, data=payload)
            print("+++++++++++++++++++++++++++++++++++")
            print(response.text)
            res=response.json()
            try:
                res['item']['active']
            except:
                return JsonResponse(res)
            if res['item']['active']: #IF Plan created Successfully
                plan_id=res['id']
                plan.planId=plan_id
                plan.save()
                subs_response=create_subscription(plan_id)
                print(subs_response)
                if subs_response['status']=='created':
                #    Create subscription
                        subscription=Subscriptions.objects.create(
                            Customer_profile=visitor_profile,
                            Creator_profile=creator_profile,
                            amount=plan.amount,
                            subscriptionId=subs_response['id'],
                            planId=subs_response['plan_id'],
                            status=subs_response['status'],
                            subscriptionLink=subs_response['short_url']
                            )
                        subscription.save()
                        
                        return JsonResponse(subs_response)
                else:
                   return JsonResponse(subs_response)
            
            
            
    else:
        return redirect('dashboard:dashboard')
    print(amount)
    
    return JsonResponse({"plan created for":creator_username})


@csrf_exempt
def Donate(request, creator_username):
    if request.method == 'POST':
        print("-----------------dddddd------------")
        if request.user.is_authenticated:  # authenticate
            try:
                visitor_profile = Profile.objects.get(user=request.user)
            except:
                return JsonResponse({"response": False})
            creator_profile = Profile.objects.get(username=creator_username)
            print(request.FILES)
            print(request.POST)

            amount = request.POST['amount']
            print(amount)

            data={
                'amount':int(amount)*100,
                'currency':"INR",
                'receipt':str(visitor_profile),
                'notes':{
                    'by':str(visitor_profile),
                    "to":str(creator_profile),
                    'type':'donation'
                }

            }

            client = razorpay.Client(auth=("rzp_test_J9Lxu7OB8M6GR3", "NOj4sb6Sp0YBIG30XLkwOhOc"))
            order=client.order.create(data=data)
            print(order)
            donation = Donations.objects.create(
                Customer_profile=visitor_profile,
                Creator_profile=creator_profile,
                amount=(order['amount'] * 92)/100,
                order_id=order['id'],
            )
            donation.save()

        return JsonResponse({"id": order['id'],"name":visitor_profile.Name,"email":visitor_profile.user.email,"phone":str(visitor_profile.Phone_no)}, safe=True)

@csrf_exempt
def DonationVerify(request,creator_username):
    if request.method == 'POST':
        print("-----------------ddddddvvvvvv------------")
        if request.user.is_authenticated:  # authenticate
            try:
                visitor_profile = Profile.objects.get(user=request.user)
            except:
                return JsonResponse({"response": False})

            creator_profile = Profile.objects.get(username=creator_username)
            print(request.FILES)
            print(request.POST)
            donation = Donations.objects.get(order_id=request.POST['razorpay_order_id'])
            print(donation)
            razorpay_payment_id=request.POST['razorpay_payment_id']
            razorpay_order_id=request.POST['razorpay_order_id']
            razorpay_signature=request.POST['razorpay_signature']
            datadict={"razorpay_payment_id":razorpay_payment_id,
                      "razorpay_order_id":razorpay_order_id,
                      "razorpay_signature":razorpay_signature}
            client = razorpay.Client(auth=("rzp_test_J9Lxu7OB8M6GR3", "NOj4sb6Sp0YBIG30XLkwOhOc"))
            var=client.utility.verify_payment_signature(datadict)
            print('var',var)
            if var ==None:
                donation.payment_id=request.POST['razorpay_payment_id']
                donation.signature=request.POST['razorpay_signature']
                donation.status='paid'
                donation.save()

                creator_profile.total_donations=creator_profile.total_donations+((donation.amount * 92)/100)
                creator_profile.save()
                print(creator_profile.total_donations)

            return JsonResponse({"status":"paid"})
        return redirect("general:login")


def CancelSubscription(request,creator_profileId):
    my_user=request.user
    if my_user.is_authenticated:
        customer_profile=Profile.objects.get(user=my_user)
        creator_profile=Profile.objects.get(Id=uuid.UUID(creator_profileId))
        subscription=Subscriptions.objects.get(
            Customer_profile=customer_profile,
            Creator_profile=creator_profile)
        print(subscription.subscriptionId)
        url = "https://api.razorpay.com/v1/subscriptions/"+subscription.subscriptionId+"/cancel"

        payload = json.dumps({
        "cancel_at_cycle_end": 1
        })
        headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Basic cnpwX3Rlc3RfMms1TXF6VW9pSHFoYm46clNjMzdJUlNtWW1lY3Noa3gwZ3U1cWsw'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        print(response.text)
        json_response=response.json()
        if json_response['status']=="active":
                subscription.cancelled=True
                subscription.save()
                return redirect('dashboard:memberships')
         
        return JsonResponse(response.json())
    else:
        return redirect('genral:login')

def BuyProduct(request,creator_profileId,customer_profileId,productId):
    if request.user.is_authenticated:
        product=StoreItem.objects.get(Id=uuid.UUID(productId))
        creator_profile=Profile.objects.get(Id=uuid.UUID(creator_profileId))
        customer_profile=Profile.objects.get(Id=uuid.UUID(customer_profileId))
        
        orderId=str(datetime.datetime.now())
        orderId=orderId.replace(" ","")
        orderId=orderId.replace(":","")
        orderId=orderId.replace(".","")
        orderId=orderId.replace("-","")
        orderId="order"+orderId
        url = "https://api.razorpay.com/v1/payment_links"

        payload = json.dumps({
        "amount": product.Price*100,
        "currency": "INR",
        "accept_partial": False,
        "reference_id":orderId,
        "description": "Payment for buying product from "+str(request.user.username),
        "customer": {
            "name": customer_profile.Name,
            "contact": customer_profile.Phone_no,
            "email":customer_profile.user.email
        },
        "notify": {
            "sms": True,
            "email": True
        },
        "reminder_enable": True,
        "notes": {
            "policy_name": "Product Buying From Zocaya"
        },
        "callback_url": "https://zocaya.com/payment/product/thankyou/"+str(customer_profile.user.id)+"/"+str(creator_profile.user.id)+"/"+str(product.Price)+"/"+product.Id.hex,
        "callback_method": "get"
        })
        headers = {
        'Authorization': 'Basic cnpwX3Rlc3RfMms1TXF6VW9pSHFoYm46clNjMzdJUlNtWW1lY3Noa3gwZ3U1cWsw',
        'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        json_response=response.json()
        



        if  json_response['status']=='created':
            return redirect(json_response['short_url'])
        else:
            return JsonResponse(json_response)
        return JsonResponse(response.json())
    else:
        return redirect("general:login")


                
def RedeemAmount(request):
    my_user=request.user
    if my_user.is_authenticated:
      profile=Profile.objects.get(user=my_user)
      if profile.Account_activated:
                    if int(profile.Revenue)==0:
                        return redirect('dashboard:redeempage') 
                    bank=BankDetail.objects.get(user=my_user)
                    redeem_message = loader.render_to_string(
                        str(settings.BASE_DIR) + '/paymentgateway/templates/redeemTemplateAkshat.html',
                    {
                        'accountnumber':bank.Account_Number,
                        'accountholdername':bank.Account_holder_name,
                        'ifsccode':bank.IFSC_Code,
                        'amount':profile.Revenue,
                        'date':str(datetime.datetime.now()),
                        'username':str(profile.username),
                        'email':str(profile.user.email),
                        'phone':str(profile.Phone_no),
                    }
                    )
                    
                    send_mail("Amount Redeem Request  | Zocaya.com ","Hi Admin,\nThe creator "+str(profile.username)+" has requested you to redeem his amount to the following account details:",'zocayamedia@gmail.com',['akshatgupta218@gmail.com'],fail_silently=False,html_message=redeem_message)
                    amountRedeemed=AmountRedeemed.objects.create(
                        Amount=profile.Revenue,
                        Date=datetime.datetime.date(datetime.datetime.now()),
                        User=profile.user
                    ) 
                    amountRedeemed.save()       
                    profile.Revenue=0
                    profile.total_donations=0
                    profile.save()
                    return redirect('dashboard:redeempage')

      else:
          return redirect('general:verify')
 
    else:
         return redirect('general:login')
def create_subscription(plan_id):
    plan=Plan.objects.get(planId=plan_id)
    url = "https://api.razorpay.com/v1/subscriptions"

    payload = json.dumps({
    "plan_id": plan_id,
    "total_count": 12,
    "quantity": 1,
    "customer_notify": 1


    })
    headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Basic cnpwX3Rlc3RfMms1TXF6VW9pSHFoYm46clNjMzdJUlNtWW1lY3Noa3gwZ3U1cWsw'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)
    return response.json()
 
@csrf_exempt
def ThankyouForProduct(request,customer_id,creator_id,amount,productId):
    print("%=======++++++====++++++======%")
    customer=User.objects.get(id=customer_id)
    creator=User.objects.get(id=creator_id)
    signature=request.GET.get('razorpay_signature')
    status=request.GET.get('razorpay_payment_link_status')
    linkRefrence_id=request.GET.get('razorpay_payment_link_reference_id')
    payment_id=request.GET.get('razorpay_payment_id')
    link_id=request.GET.get('razorpay_payment_link_id')
    payload=link_id+"|"+linkRefrence_id+"|"+status+"|"+payment_id
    computedSignature=hmac.new(b'NOj4sb6Sp0YBIG30XLkwOhOc',bytes(payload, 'UTF-8'),'sha256').hexdigest()

    if computedSignature==signature:
        print("---------------------------Signature Verified--------------------")
        print(status)
        if status=="paid":
            print("-------------------------------------------")
            print(amount)
            
          
            productPurchased=ProductPurchased.objects.create(
                Customer_profile=customer.profile,
                Creator_profile=creator.profile,
                linkRefrence_id=linkRefrence_id,
                payment_id=payment_id,
                link_id=link_id,
                status=status,
                amount=float(amount)
                
            )
            productPurchased.save()
            creator_profile=Profile.objects.get(user=creator)
            creator_profile.Revenue+=round(float(amount)*0.92,2)
            creator_profile.save()
      
            product=StoreItem.objects.get(Id=uuid.UUID(productId))
            # todo -------------------- send mail
            customer_message = loader.render_to_string(
                str(settings.BASE_DIR) + '/paymentgateway/templates/orderInvoiceEmailTemplate_Customer.html',
            {
                'date': str(datetime.datetime.now()),
                'orderId':linkRefrence_id,
                'productId':productId,
                 'amount':float(amount),
                 'name':creator.profile.Name,
                 'mail':creator.profile.user.email,
                 'phone':creator.profile.Phone_no,
                 'headline':product.Headline,
                 'description':product.Description,
                 
                 
            }
           )
            send_mail("Thanks For Purchasing|Zocaya.com ","Your Invoice is Here",'zocayamedia@gmail.com',[customer.email],fail_silently=True,html_message=customer_message)
            
            shippingAddr=ShippingAddress.objects.get(User=customer)
            
            creator_message = loader.render_to_string(
                str(settings.BASE_DIR) + '/paymentgateway/templates/orderInvoiceEmailTemplate_Creator.html',
            {
                'date': str(datetime.datetime.now()),
                'orderId':linkRefrence_id,
                'productId':productId,
                 'amount':float(amount),
                 'name':customer.profile.Name,
                 'mail':customer.profile.user.email,
                 'phone':customer.profile.Phone_no,
                 'headline':product.Headline,
                 'description':product.Description,
                 'address':shippingAddr.address_line,
                 'city':shippingAddr.city,
                 'state':shippingAddr.state,
                  'pincode':   shippingAddr.pin_code
            }
           )
            send_mail("Great News! You Have New Purchase |Zocaya.com ","Your Delivery Address is Here",'zocayamedia@gmail.com',[creator.email],fail_silently=True,html_message=creator_message) 
               
        else:
            JsonResponse({'message':'Payment Failed, Contact us if your amount get diduced and not return back to your account'})
    else:
        JsonResponse({'response':'Bad Request!'})
      
    return render(request,'ThankyouForOrder.html')