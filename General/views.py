from django.shortcuts import render,redirect
from django.contrib import auth, messages
from .models import *
from Posts.models import *
from Store.models import *
from django.core.files.storage import FileSystemStorage
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from zocaya_new.settings import *
# from Zocaya.settings import *
import json,uuid
from Posts.models import Notification
import time, threading
from django.core.mail import send_mail
import random
from django.core.paginator import Paginator
from django.template import loader
from imagekitio import ImageKit
from media import *

imagekit = ImageKit(
    private_key='private_lLLidL7grmjC6y/uuR98dEGlvPM=',
    public_key='public_2e8JMemRIR9zGN+aIQB3dSRPnK0=',
    url_endpoint='https://ik.imagekit.io/xfu94rzcsoi/'
)


def UpdateShippingAddr(request,product_id,creator_profileId):
    if request.user.is_authenticated:
      shiping_addr=ShippingAddress.objects.filter(User=request.user)
      if request.method=='POST':
        state=request.POST['state']
        pincode=request.POST['pincode']
        city=request.POST['city']
        address=request.POST['address']
        shiping_addr.update(
            address_line=address,
            state=state,
            pin_code=pincode,
            city=city
        )
        customer_profileId=Profile.objects.get(user=request.user).Id.hex
        return redirect("paymentgateway:paymentgateway",creator_profileId,customer_profileId,product_id)
    
    else:
        return redirect("general:login")

def LoginForm(request):
    my_user = request.user
    #If you want to know if the user is logged in
    is_user_logged = my_user.is_authenticated
    if is_user_logged:
        return redirect('dashboard:dashboard')
    if request.method=="POST":
        email=request.POST['uname']
        try:
            uname=User.objects.get(email=email).username
        except:
            return render(request,'General/index.html',{'error':'Invalid Email Address'})
        pwd=request.POST['pass']
        user=auth.authenticate(username=uname,password=pwd)
        if user is not None:
            auth.login(request,user)
            return redirect(request.path)
        else:
            return render(request,'General/index.html',{'error':'Invalid Credentials'})
    return render(request,'General/index.html')

    # return render(request, 'General/login.html', {})


def signup(request, backend='django.contrib.auth.backends.ModelBackend'):
     if request.method=="POST":
          # Create a user
          print("ok1")
     
          if request.POST['pass']==request.POST['passConfirm']:
               print("ok2")
               # Both the passwords have been matched
               # Now check if user exist or not
               try:

                    username = request.POST['username']
                    print("ok2")
                    if " " in username:
                        return render(request,'General/signup.html',{'error':'username cannot have spaces'})
                        
                    user=User.objects.get(username=username)
                    return render(request,'General/signup.html',{'error':'user already exist'})
                    
               except User.DoesNotExist:
                    try:
                        print("ok3")
                        email=request.POST['email']
                        temp=User.objects.get(email=email)
                        return render(request,'General/signup.html',{'error':'Email exist'})
                    except:
                        print("ok4")
                        user=User.objects.create_user(username=request.POST['username'],
                                                    password=request.POST['pass'],
                                                    email=email
                                                    )                                        
                        auth.login(request,user, backend='django.contrib.auth.backends.ModelBackend')
                        print(user)
                        return redirect('general:profile')
          else:
               return render(request,'General/signup.html',{'error':'password does not match'})
                                 
     return render(request,'General/signup.html')

def Verify(request):
    my_user=request.user
    if request.method=="POST":
        otpMail=request.POST['otpmail']
        # otpSms=request.POST['otpsms']
        print(otpMail)
        # print(otpSms)
        profile=Profile.objects.get(user=my_user)
        if int(profile.otp_for_email)==int(otpMail):
            Profile.objects.filter(user=my_user).update(Account_activated=True)
            return redirect('dashboard:dashboard')
        else:
             return render(request,'General/otpEmail.html',{'profile':profile,'message':'Invalid OTP,Please Try Again'})
            
            
    if my_user.is_authenticated:
        profile=Profile.objects.get(user=my_user)
        if not profile.Account_activated:
            return render(request,'General/otpEmail.html',{'profile':profile})
        else:
            return redirect('dashboard:dashboard')
        
@csrf_exempt
def GenerateOtp(request):
    my_user=request.user
    print(my_user)
    profile=Profile.objects.get(user=my_user)
    print(my_user)
    if request.method=='POST' and my_user.is_authenticated and profile.otp_for_email==0 :
        print("ok",my_user)
        received_json_data= json.loads(request.body)
        username=received_json_data['username']    
        thread=threading.Thread(target=create_timeout,args=(username,))
        thread.start()
        account_sid = 'xxxxxxxxxxxxxxxxxxx'
        auth_token = 'xxxxxxxxxxxxxxxxxxxxxxxx'
        # client = Client(account_sid, auth_token)
        # otp_mob=random.randint(111111,999999)
        otp_mail=random.randint(111111,999999)
        Profile.objects.filter(user=my_user).update(otp_for_email=otp_mail)
        # message = client.messages \
        #                 .create(
        #                     body="Your OTP is "+str(otp_mob),
        #                     from_='+xxxxx33',
        #                     to=str(profile.Phone_no)
        #                 )
        send_mail(
        "Verification Mail",
        "Hi Zocaya User\nYour Zocaya OTP is :"+str(otp_mail)+"\n\n You are receiving this OTP because your email has been used to sign up on zocaya.com\n\nIf you have not signed up on zocaya, please contact us on zocayamedia@gmail.com and we will investigate the issue further \n\n Thanks,\nZocaya Team",
        "zocayamedia@gmail.com",
        [str(profile.user.email)],
        fail_silently=True
            )
        print(username)
        return JsonResponse({'success':True})
    else:
        return JsonResponse({'success':False}) 

@login_required(login_url='/')
def ChangeEmailNumber(request):
    my_user=request.user
    if my_user.is_authenticated:
            if request.method=='POST':
                email=request.POST['mail']
                # mob_no=request.POST['number']
                User.objects.filter(username=my_user).update(email=email)
                # Profile.objects.filter(user=my_user).update(Phone_no=mob_no)
                profile=Profile.objects.get(user=my_user)
                return render(request,'General/changeEmailNumber.html',{'profile':profile,'message':'change successfully!'})
            else:
                profile=Profile.objects.get(user=my_user)
                return render(request,'General/changeEmailNumber.html',{'profile':profile})
    else:
            return redirect('general:login')
@login_required(login_url='/')
def logout(request):
    my_user = request.user
        #If you want to know if the user is logged in
    is_user_logged = my_user.is_authenticated
    if is_user_logged:
        auth.logout(request)
    return redirect('general:login')

@login_required(login_url='/')
def CreateProfile(request):
    my_user = request.user

    profile = Profile.objects.filter(Profile_incomplete=False, user=my_user)
    if profile.exists():
        return redirect('dashboard:dashboard')
    else:
        if request.method=="POST":

            if 'dp_input' in request.FILES:
                f=request.FILES
                f = f['dp_input']

                upload = imagekit.upload(
                    file=open(f.temporary_file_path(), "rb"),
                    file_name="image-post/" + str(my_user.email) + "/" + str(f),
                    options={
                        "response_fields": ["is_private_file", "tags"],

                    },
                )
                src = upload['response']['url']
                fileid=upload['response']['fileId']
            else:
                upload = imagekit.upload(
                    file=open('./media/avatar.jpg', "rb"),
                    file_name="image-post/" + str(my_user.email) + "/" +'dp',
                    options={
                        "response_fields": ["is_private_file", "tags"],

                    },
                )
                src = upload['response']['url']
                fileid = upload['response']['fileId']

            profile=Profile.objects.create(
                Name= request.POST['username'],
                username= my_user.username,
                Gender = request.POST['gender'],
                UserType=request.POST['usertype'],
                user = my_user,
                Avatar=src,
                fileid=fileid,
                DateOfBirth = request.POST['dob'],
                URL="/"+str(my_user),
                tab_order='image,videos,articles',
                Country = request.POST['country'],
                
                Phone_no = request.POST['num'],
                Bio = request.POST['aboutme'],
                Profile_incomplete=False,
            )
            shipping_addr=ShippingAddress.objects.create(User=my_user)
            shipping_addr.save()
            profile.save()
            trace=ImageTrace.objects.filter(User=my_user,type='avatar')
            if trace.exists():
                    trace[0].delete()
            
            return redirect('dashboard:dashboard')
    trace=ImageTrace.objects.filter(User=my_user,type='avatar')
    if not trace.exists():
                trace=ImageTrace.objects.create(User=my_user,type='avatar')
                trace.save()
    else:
                trace.update(Last_Image_Upload="",Current_Image="")
    return render(request,'General/create-profile.html', {'id':my_user.id})

@login_required(login_url='/')
def EditProfile(request):
    my_user = request.user
    banksettings= BankDetail.objects.filter(user=my_user)
    if request.method=="POST":
        u = User.objects.get(username=my_user)
        print(request.POST)
        youtube=request.POST['YouTube']
        instagram=request.POST['Instagram']
        twitter=request.POST['Twitter']
        facebook=request.POST['Facebook']
        linkedin=request.POST['LinkedIn']
        takatak=request.POST['Takatak']
        social_data = SocialMediaAccounts.objects.filter(user=my_user)
        print('s', social_data)
        if not social_data.exists():
            social_data=SocialMediaAccounts.objects.create(user=my_user,
                                          YouTube=youtube,
                                          Instagram=instagram,
                                          Facebook=facebook,
                                          LinkedIn=linkedin,
                                          Twitter=twitter,
                                          Takatak=takatak)
            print(social_data)
        else:
            social_data = SocialMediaAccounts.objects.filter(user=my_user)
            print(social_data)
            social_data.update(
                                        YouTube=youtube,
                                        Instagram=instagram,
                                        Facebook=facebook,
                                        LinkedIn=linkedin,
                                        Twitter=twitter,
                                        Takatak=takatak)
            print(social_data)

        new_username=request.POST['newusername']
        existing_username = User.objects.filter(username=new_username)
        if existing_username.exists() and str(new_username)!=str(my_user):
            messages.warning(request, "Username already exists please try a new one.")
        else:
            u.username=new_username
            current_profile=Profile.objects.filter(user=my_user, Profile_incomplete=False)
            current_profile.update(username=new_username)
            u.save()
            current_profile.update(
                Name= request.POST['newname'],
                Country = request.POST['country'],
                Phone_no = request.POST['newnum'],
                Bio = request.POST['newbio'],
                tab_order=request.POST['od'],
                )
            if existing_username.exists():
                messages.success(request, "Your profile is Updated Successfully.")
            else:
                messages.success(request, "Your profile is Updated Successfully.")
            return redirect("/profile/edit-profile/")
    current_profile=Profile.objects.filter(user=my_user, Profile_incomplete=False)
    try:
        social_data = SocialMediaAccounts.objects.get(user=my_user)
    except:
        social_data=[]

    print(social_data)
    context = {
        'profile': current_profile[0],
        'banksetting':banksettings,
        'social':social_data
    }
    if current_profile.exists():
        if current_profile[0].Account_activated:
           return render(request,'General/edit-profile.html', context)
        else:
            return redirect('general:verify')

    else: 
        return redirect('general:profile')   
    
@login_required(login_url='/')
def ChangePassword(request):
    my_user = request.user
    banksettings= BankDetail.objects.filter(user=my_user)
    profile=Profile.objects.filter(user=my_user, Profile_incomplete=False)
    if request.method=="POST":
        if request.POST['newpass']==request.POST['newpassConfirm']:
            new_password = request.POST['newpass']
            u = User.objects.get(username=my_user)
            u.set_password(new_password)
            u.save()
        else:
            messages.warning(request, "Password Not Match")
    if profile.exists():
        if profile[0].Account_activated:
           return render(request,'General/password-reset.html', {'profile':profile[0], 'banksetting':banksettings})
        else:
            return redirect('general:verify')
    else: 
        return redirect('general:profile')   

@login_required(login_url='/')
def ChangeAvatar(request):
    my_user = request.user
    banksettings= BankDetail.objects.filter(user=my_user)
    profile_data=Profile.objects.get(user=my_user, Profile_incomplete=False)
    img=(profile_data.Avatar)
    if request.method=="POST":
        current_profile=Profile.objects.filter(user=my_user, Profile_incomplete=False)
        print(request.FILES)
        t = request.FILES['image']
        dp = t.temporary_file_path()

        upload = imagekit.upload(
            file=open(dp, 'rb'),
            file_name="image-post/" + str(my_user.email) + "/" + str(request.FILES['image']),
            options={
                "response_fields": ["is_private_file", "tags"],

            },
        )
        print(upload)
        current_profile.update(
            Avatar = upload['response']['url'],
            fileid=upload["response"]['fileId'],
        )


        profile_data=Profile.objects.get(user=my_user, Profile_incomplete=False)
       
        trace=ImageTrace.objects.filter(User=my_user,type='avatar')
        if not trace.exists():
            trace[0].delete()

        return render(request,'General/change-avatar.html', {'profile':profile_data,'id':my_user.id, 'banksetting':banksettings, 'message':"Updated Successfully"})
    trace=ImageTrace.objects.filter(User=my_user,type='avatar')
    if not trace.exists():
            trace=ImageTrace.objects.create(User=my_user,type='avatar',Current_Image=img)
            trace.save()
    else:
        trace.update(Current_Image=img)
    
    return render(request,'General/change-avatar.html', {'profile':profile_data,'id':my_user.id, 'banksetting':banksettings,})

@login_required(login_url='/')
@csrf_exempt
def BankSetting(request):
    my_user = request.user
    banksettings= BankDetail.objects.filter(user=my_user)
    profile=Profile.objects.filter(user=my_user, Profile_incomplete=False)
    if request.method=="POST":
        bank_details= BankDetail.objects.create(
            user=my_user,
            Account_Number= request.POST['AccNum'],
            IFSC_Code = request.POST['code'],
            Account_holder_name = request.POST['AccName'],
            Street_Address = request.POST['street'],
            City = request.POST['city'],
            State = request.POST['state'],
            Pincode = request.POST['pincode'],
        )
        bank_details.save()
        print(bank_details)
        messages.success(request, "Your Bank Account details are saved Successfully.")
    context = {
        'profile': profile[0],
        'banksetting':banksettings,
        'banksettings':banksettings,
        
        }
    if profile.exists():
        if profile[0].Account_activated:
           return render(request,'General/bankSetting.html', context)
        else:
            return redirect('general:verify')
    else: 
        return redirect('general:profile')   
    

@login_required(login_url='/')
def BankEditSetting(request):
    my_user = request.user
    profile=Profile.objects.filter(user=my_user, Profile_incomplete=False)
    if profile.exists():
        banksettings= BankDetail.objects.filter(user=my_user)
        if not banksettings.exists():
           return redirect('/profile/edit-profile/banksettings/')
        if profile[0].Account_activated:
            if request.method=="POST":
                banksettings.update(
                    user=my_user,
                    Account_Number= request.POST['AccNum'],
                    IFSC_Code = request.POST['code'],
                    Account_holder_name = request.POST['AccName'],
                    Street_Address = request.POST['street'],
                    City = request.POST['city'],
                    State = request.POST['state'],
                    Pincode = request.POST['pincode'],
                )
            
   
                messages.success(request, "Your Bank Account details are saved Successfully.")
                context = {
                'banksetting':banksettings[0],
                'banksettings':banksettings,
                'profile': profile[0],
                }
                return render(request,'General/editBankSetting.html', context)
            else:
                context = {
                'banksetting':banksettings[0],
                'banksettings':banksettings,
                'profile': profile[0],
                }
                return render(request,'General/editBankSetting.html', context)
        else:
            return redirect('general:verify')
    else: 
        return redirect('general:profile')   
    
@login_required(login_url='/')
@csrf_exempt
def PublicProfileSubscriptionSetting(request):
    my_user = request.user
    banksettings= BankDetail.objects.filter(user=my_user)
    profile=Profile.objects.filter(user=my_user, Profile_incomplete=False)
    if request.method=="POST":
        Subscription_price= request.POST['subprice']
        print(Subscription_price)
        profile.update(
            Subscription_price= request.POST['subprice'],
        )
    context = {
        'profile':profile[0],
        'banksetting':banksettings,
        }
    if profile.exists():
        if profile[0].Account_activated:
            return render(request,'General/publicProfileSetting.html', context)
        else:
            return redirect('general:verify')
    else: 
        return redirect('general:profile')   


@login_required(login_url='/')
@csrf_exempt
def PublicProfileSetting(request):
    my_user = request.user
    banksettings= BankDetail.objects.filter(user=my_user)
    profile=Profile.objects.filter(user=my_user, Profile_incomplete=False)
    if request.method=="POST":
        points=request.POST['bpoints']
        print(points) 
        profile.update(
            Why_to_subscribe=points
            )
        messages.success(request, "Bullet Points added Successfully.")
    context = {
        'profile':profile[0],
        'banksetting':banksettings,
    }
    if profile.exists():
        if profile[0].Account_activated:
            return render(request,'General/publicProfileSetting.html', context)
        else:
            return redirect('general:verify')
    else: 
        return redirect('general:profile')  
   

@login_required(login_url='/')
def PublicProfileSettingDone(request):
    my_user=request.user
    banksettings= BankDetail.objects.filter(user=my_user)
    if request.method=='POST':
        Profile.objects.filter(user=request.user, Profile_incomplete=False).update(Subscription_price=float(request.POST['subprice']))
        profile=Profile.objects.filter(user=request.user, Profile_incomplete=False)
        return render(request, 'General/publicProfileSetting.html', {'profile':profile[0],'message':"Price Updated Successfully", 'banksetting':banksettings,})

@csrf_exempt
def SaveImage(request,location,prof_id):
    print("IN SAVE IMAGE")
    if request.method=='POST' and location!='avatar':
            profile_uuid=uuid.UUID(prof_id)
            require_profile=Profile.objects.get(Id=profile_uuid)
            email=require_profile.user.email
            print(email)
            print("saving")
            f=request.FILES

            print(request.POST)
            filename=str(f['files'])
            print(str(f))
            # if not filename.lower().endswith(('.png', '.jpg', '.jpeg','.mp4',)):
            #     return JsonResponse({'src': False})
            f=f['files']
            fs=FileSystemStorage()
            upload = imagekit.upload(
                file=open(f.temporary_file_path(), "rb"),
                file_name="image-post/" + str(email) + "/" + str(f),
                options={
                    "response_fields": ["is_private_file", "tags"],

                },
            )
            src=upload['response']['url']

            trace=ImageTrace.objects.get(User=require_profile.user,type=location)
            print(trace)
            if trace.fileid:
                de = trace.fileid
                print(de)
                delete = imagekit.delete_file(de)
                print(delete)
                # trace.fileid = upload['response']['fileid']
            # completePath=str(settings.BASE_DIR)+"/media/"+location+"/"+str(email)+"/"
            # print(completePath)

            print(upload)
            trace.fileid=upload["response"]['fileId']
            trace.Last_Image_Upload=trace.Current_Image
            trace.Current_Image=upload['response']['url']
            t=trace.save()
            print(t)
            # if trace.Last_Image_Upload:
            #     subprocess.run(['rm',completePath+trace.Last_Image_Upload])
            return JsonResponse({'src': src})
    elif request.method=='POST' and location=='avatar':
            require_user=User.objects.get(id=int(prof_id))
            email=require_user.email
            print(request.FILES)
            f=request.FILES

            f = f['files']
            fs = FileSystemStorage()
            upload = imagekit.upload(
                file=open(f.temporary_file_path(), "rb"),
                file_name="image-post/" + str(email) + "/" + str(f),
                options={
                    "response_fields": ["is_private_file", "tags"],

                },
            )
            trace = ImageTrace.objects.get(User=require_user, type=location)
            if trace.fileid:
                de = trace.fileid
                print(de)
                delete = imagekit.delete_file(de)
                print(delete)
            src = upload['response']['url']

            trace.fileid = upload["response"]['fileId']
            trace.Last_Image_Upload=trace.Current_Image
            trace.Current_Image=src
            trace.save()
            # if trace.Last_Image_Upload:
            #     subprocess.run(['rm',completePath+trace.Last_Image_Upload])
            return JsonResponse({'src': src})
           
            


    else:
            return JsonResponse({"WARNING!!":"Dont Try TO Hack The Site!!!!!"})
 
@csrf_exempt 
def ProfileFilterView(request, username):
    if request.method=="POST":
        try:
            email=request.POST['uname']
            pwd=request.POST['pass']
            uname=User.objects.get(email=email).username
            user=auth.authenticate(username=uname,password=pwd)
            if user is not None:
                auth.login(request,user)
                return redirect(request.path)
            else:
                return redirect(request.path)
        except:
            pass
   

    try:
        likes=Likes.objects.filter(Like_by=request.user.profile,type="image")
        post_ids=[]
        for obj in likes:
            post_ids.append(obj.Post_id)
        
    except:
        likes=[]
        post_ids=[]
    try:
        profile=Profile.objects.filter(username=username)[0]
        print(username)
        try:
            social_data = SocialMediaAccounts.objects.filter(user=profile.user)[0]
        except:
            social_data=[]
        print(social_data)
        total_likes=StoreItem.objects.filter(Owner=profile).count()
        post_count=TextContent.objects.filter(Owner=profile).count()+ImageContent.objects.filter(Owner=profile).count()+VideoContent.objects.filter(Owner=profile).count()
        print("-------------")
        print(post_count)
        user=profile.user
        image_content=ImageContent.objects.filter(User=user,Published=True)
        p = Paginator(image_content.order_by('-Updated_on'), 9)
        page_num = request.GET.get('page', 1)
        page = p.page(page_num)
        try:
            followed_profile=Profile.objects.filter(user=request.user, Following__in=[profile.user])
            loggedin_profile=Profile.objects.filter(user=request.user, Profile_incomplete=False)[0]

        except:
            followed_profile=[]
            loggedin_profile=[]

        print(social_data)
        print("--------------TEST________________----")
        # print(request.user not in image_content[0].Owner.Subscribed.all())
        context = {
            'profile': profile,
            "image_content":page,
            'pagination': page,
            'followed_profile':followed_profile,
            'visitor':request.user,
            'post_ids':post_ids,
            'logged_user':loggedin_profile,
            "total_likes":total_likes,
            "total_post":post_count,
            "social":social_data,
            }
        print(profile.tab_order)
        return render(request, 'General/user-profile.html', context)
    except IndexError:
        return JsonResponse({"res":False})
    
def UserProfilePages(request,username,type):
    profile=Profile.objects.filter(username=username)[0]
    try:
        social_data = SocialMediaAccounts.objects.filter(user=profile.user)[0]
    except:
        social_data = []
    total_likes=StoreItem.objects.filter(Owner=profile).count()
    user=profile.user
    visitor=request.user
    post_count=TextContent.objects.filter(Owner=profile).count()+ImageContent.objects.filter(Owner=profile).count()+VideoContent.objects.filter(Owner=profile).count()

    if type=="videos":
        try:
            likes=Likes.objects.filter(Like_by=visitor.profile,type="video")
            post_ids=[]
            for obj in likes:
                post_ids.append(obj.Post_id)
            
        except:
            likes=[]
            post_ids=[]
        video_content=VideoContent.objects.filter(User=user,Published=True)
        p = Paginator(video_content.order_by('-Updated_on'), 9)
        page_num = request.GET.get('page', 1)
        page = p.page(page_num)
        print(post_ids)
        context = {
            'profile': profile,
            'pagination': page,
            'post_ids':post_ids, 
            "video_content":page,
            "visitor":request.user,
            "total_likes":total_likes,
            "total_post":post_count,
            "social": social_data,
        }
        return render(request, 'General/userprofile-videos.html', context)
    elif type=="articles":
        try:
            likes=Likes.objects.filter(Like_by=visitor.profile,type="article")
            post_ids=[]
            for obj in likes:
                post_ids.append(obj.Post_id)
            
        except:
            likes=[]
            post_ids=[]
        text_content=TextContent.objects.filter(User=user,Published=True)
        p = Paginator(text_content.order_by('-Updated_on'), 9)
        page_num = request.GET.get('page', 1)
        page = p.page(page_num)
        for text in page :
            print(text.Headline)
        context = {
            'profile': profile,
            'pagination': page,
            'post_ids':post_ids,
            "text_content":page,
            "visitor":request.user,
            "total_likes":total_likes,
            "total_post":post_count,
            "social": social_data,
        }
        return render(request, 'General/userprofile-articles.html', context)
    # elif type=="products":
    #     products=StoreItem.objects.filter(User=user, Published=True)
    #     if visitor.is_authenticated:
    #         visitor_profile=Profile.objects.get(user=visitor)
    #         address=ShippingAddress.objects.get(User=request.user)
    #
    #     else:
    #         visitor_profile=""
    #         address=""
    #
    #     p = Paginator(products.order_by('-Updated_on'), 9)
    #     page_num = request.GET.get('page', 1)
    #     page = p.page(page_num)
    #     context = {
    #         'profile': profile,
    #         'pagination': page,
    #         "addr":address,
    #         "products":page,
    #         "visitor_profile":visitor_profile,
    #         "visitor":request.user,
    #         "total_likes":total_likes,
    #         "total_post":post_count
    #     }
    #     return render(request, 'General/userprofile-products.html', context)


def TestUrl(request):
    html_message = loader.render_to_string(
                str(settings.BASE_DIR)+"/paymentgateway"+"/templates"+"/orderInvoiceEmailTemplate_Creator.html",
                {
                    'amount': '500',
                    'creator':  "Abrar",
                    'date':str(datetime.datetime.now()),
                    'headline':"Simple Blue Hat",
                    'description':"This is leather amde Simple Black Hat witgh cowboy style",
                    'address':"216, cst station , ",
                    'city':"Mumbai",
                    'pincode':"4001",
                    'state':"Maharashtra",
                    'phone':"9529693800",
                    'name':"Akshat",
                    'orderId':"12312434",
                    'productId':"`213jjjd3",
                    'mail':'akshat218@gmail.com'
                  
                 }
                )
    send_mail("Great New! New Purchase From Zocaya",
                          "You Get A New Order From"+"Akshat",
                          "zocayamedia@gmail.com",
                          ['9529693800aa@gmail.com'],fail_silently=False,html_message=html_message)
    return JsonResponse({'res':True})
    # my_user=request.user
    # thread=threading.Thread(target=create_timeout,args=(str(my_user),))
    # thread.start()
    
    # send_mail(
    #     "This Is Sample Subject",
    #     "This Is A Test Sample MESSAGE",
    #     "testmailabrar@gmail.com",
    #     ['areeb.fiverr47@gmail.com'],
    #     fail_silently=False
    # )



# Your Account Sid and Auth Token from twilio.com/console
# and set the environment variables. See http://twil.io/secure


    # 
        # return JsonResponse({})
    # return render(request,'General/otpEmail.html')
    # return render(request,'General/user-post.html')
    
@csrf_exempt
def MarkAsRead(request,notifi_id,userprofile_id):
    notification_uuid=uuid.UUID(notifi_id)
    notif_obj=Notification.objects.get(Id=notification_uuid)
    profile_obj=Profile.objects.get(username=userprofile_id)
    notif_obj.Send_to.remove(profile_obj.user)
    if not notif_obj.Send_to.exists(): #Delete If All Have Read The Message
          notif_obj.delete()
    print(notif_obj)
    print(profile_obj)
    # notif_obj=Notification.objects.get(Id=notifi_id)
    # user_profile=Profile.objects.get(Id=userprofile_id)
    return JsonResponse({"res":True})
@csrf_exempt
def MarkAllAsRead(request,userprofile_id):
    require_profile=Profile.objects.get(username=userprofile_id)
    notif_obj=Notification.objects.filter(Send_to__in=[require_profile.user])
    for obj in notif_obj:
        obj.Send_to.remove(require_profile.user)
        if not obj.Send_to.exists(): #Delete If All Have Read The Message
                obj.delete()
    return JsonResponse({"res":True})

def create_timeout(user):
    my_timer=120
    for x in range(120):
        my_timer=my_timer - 1
        time.sleep(1)
    Profile.objects.filter(username=user).update(otp_for_email=0,otp_for_number=0)
    profile=Profile.objects.get(username=user)
        
    print("-----------------TIME UP FOR "+user+"---------------------")       


@login_required(login_url='/')
def Follow(request,username):
    logged_in_user=request.user
    print("In follow function")
    viewed_profile=Profile.objects.get(username=username)
    visitor_profile=Profile.objects.get(user=request.user)
    if visitor_profile==viewed_profile:
        messages.warning(request, "You cannot Follow yourself")
        return redirect('/'+str(username))
    else:
        print('Profile WALA USER: ', username)
        print('Jisne Click Kiya: ', request.user)
        visitor_profile.Following.add(viewed_profile.user)
        viewed_profile.my_followers.add(visitor_profile.user) 
        notification=Notification.objects.create(
            Message="You Got A New Follower "+str(request.user),
            Link="/"+str(request.user)
        )
        notification.Send_to.add(viewed_profile.user)
        notification.save() 
        visitor_profile.save()
        viewed_profile.save()
        print('login WALAy USER ki following: ',visitor_profile.Following.all())
        print('Profile WALA USER ke followers: ',viewed_profile.my_followers.all())
        messages.success(request, "You've followed "+str(username))
        return redirect('/'+str(username))


@login_required(login_url='/')
def Unfollow(request,username):
    logged_in_user=request.user
    viewed_profile=Profile.objects.get(username=username)
    visitor_profile=Profile.objects.get(user=request.user)
    if visitor_profile==viewed_profile:
        messages.warning(request, "You cannot Unfollow yourself")
        return redirect('/'+str(username))
    else:
        visitor_profile.Following.remove(viewed_profile.user)
        viewed_profile.my_followers.remove(visitor_profile.user)
        visitor_profile.save()
        viewed_profile.save()
        messages.success(request, "You've unfollowed "+str(username))
        return redirect('/'+str(username))

def PostsDetailPage(request, username, type, post_id):
    visitor=request.user
    print('id',post_id)
    try:
        visitor_profile=Profile.objects.get(user=request.user)
        like=Likes.objects.filter(Post_id=int(post_id), Like_by=visitor_profile)
        followed_profile=Profile.objects.filter(user=visitor, Following__in=[profile.user])
        
        
        
    except:
        visitor_profile=""
        like=[]
        followed_profile=""
      
    profile=Profile.objects.filter(username=username)[0]
    profile_data=Profile.objects.get(username=username)
    post_count=TextContent.objects.filter(Owner=profile_data).count()+ImageContent.objects.filter(Owner=profile_data).count()+VideoContent.objects.filter(Owner=profile_data).count()
    total_likes=StoreItem.objects.filter(Owner=profile_data).count()
    
    user=profile.user
    print("--------")
    print(post_count)
    print(total_likes)
    if type=="videos":
        video_content=VideoContent.objects.filter(User=user, Id=post_id )[0]
        print('v',video_content.Link)
        context = {
            'like':like,
            'profile': profile,
            'content':video_content,
            'followed_profile': followed_profile,
              "visitor":visitor,
              "total_post":post_count,
              "total_likes":total_likes
        }
        return render(request, 'General/videodetailpage.html', context)
    elif type=="articles":
        text_content=TextContent.objects.filter(User=user, Id=post_id )[0]
        context = {
            'like':like,
            'profile': profile,
            "content":text_content,
            'followed_profile': followed_profile,
            "visitor":visitor,
             "total_post":post_count,
              "total_likes":total_likes
        }
        return render(request, 'General/articledetailpage.html', context)
    elif type=="images":
        image_content=ImageContent.objects.filter(User=user, Id=post_id )[0]
        context = {
            'like':like,
            'profile': profile,
            "content":image_content,
            'followed_profile': followed_profile,
              "visitor":visitor,
                            "total_post":post_count,
              "total_likes":total_likes
        }
        return render(request, 'General/imagedetailpage.html', context)
    elif type=="products":
        products=StoreItem.objects.filter(User=user, Id=post_id)[0]
        context = {
            'like':like,
            'profile': profile,
            "content":products,
            'followed_profile': followed_profile,
              "visitor":visitor,
                            "total_post":post_count,
              "total_likes":total_likes
        }
        return render(request, 'General/productdetailpage.html', context)


# todo  #6) forgot password = NOT Possible because the form comes from allauth. Not editable.  
        #7) profile_pic = DONE
        #8)Pagination in all pages = Done [showes error in terminal, should be sorted somehow.]
        #11)Remove Heading For CrateNewPost Section = Done
        #13)Set Profile Image =Done
        #14) Set redeem page with table with icon <i class="fa fa-exchange" aria-hidden="true"></i> = Done
        #12)Edit Search Rsult Page Enter "Search Result For <username>", Change Cards and Pagination view = Done
        #10)Why to subscribe content using ck editor  http://localhost:8000/profile/edit-profile/publicProfileSetting/ = Done csrf prob, do test once  
        #9)If Condition For Bank Setting Page using .exist by filtering bank model for specific user. = Done
        #15)Set Sharing Link In the my posts section = Done
        # ----------------------------------------------------------
        # forgot pass = done
        # login pass hide = done
        # bank settings = bnk settings needs fix
        # mark all as read = done
