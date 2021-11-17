from django.shortcuts import render,redirect
from .models import *
from Store.models import *
from General.models import *
import os,subprocess
# from Zocaya.settings import *
from django.contrib.auth.decorators import login_required
import datetime
from Dashboard.views import getNotifications
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse
from imagekitio import ImageKit
from media import *

imagekit = ImageKit(
    private_key='private_lLLidL7grmjC6y/uuR98dEGlvPM=',
    public_key='public_2e8JMemRIR9zGN+aIQB3dSRPnK0=',
    url_endpoint='https://ik.imagekit.io/xfu94rzcsoi/'
)
import vimeo

client = vimeo.VimeoClient(
  token='2677c11391e2747411b269d6f27c305a',
  key='b1ce5e5f0283e9b0e76b5adaeedccc8bb3f6151b',
  secret='YAyEoOidYAozvBZteK/1aLdbosoO4zW1KA6JM/AWwvwheLGkoJB9Z0U/9TmewNmIXOscnSncJDyNsn/4AUSkJ8btWrXXhbix50cnSDi4XM4nA7qBB68fWZvIr5hIN4Zo'
)

@login_required(login_url='/')
def CreatePostView(request):
    my_user = request.user
    #If you want to know if the user is logged in
    is_user_logged = my_user.is_authenticated
    if is_user_logged:
        profile=Profile.objects.get(user=my_user)
        profile_data = Profile.objects.filter(Profile_incomplete=False, user=my_user)[0]
        notif=getNotifications(my_user)
        print(profile.Id)
        if profile.Account_activated:
                trace=ImageTrace.objects.filter(User=my_user,type='article-post')
                if not trace.exists():
                    trace=ImageTrace.objects.create(User=my_user,type='article-post')
                    trace.save()
                else:
                    trace.update(Last_Image_Upload="",Current_Image="")
                return render(request, 'posts/create-posts.html',{'id':profile.Id,'notifications':notif,'profile':profile_data})
        else:
                return redirect('genral:verify')
    else:
        return redirect('general:login')


# @login_required(login_url='/')
# def DeletePostView(request):
#     my_user = request.user
#     #If you want to know if the user is logged in
#     is_user_logged = my_user.is_authenticated
#     if is_user_logged:
#         return render(request, 'posts/delete-posts.html',{})
#     else:
#         return redirect('general:login')

@login_required(login_url='/')
def ArticleView(request):
    my_user = request.user
    #If you want to know if the user is logged in
    is_user_logged = my_user.is_authenticated
    if is_user_logged:
        profile=Profile.objects.get(user=my_user, Profile_incomplete=False)
        notif=getNotifications(my_user)
        profile_data = Profile.objects.get(Profile_incomplete=False, user=my_user)
        if profile_data.exists():
            if profile_data.Account_activated :
                return render(request, 'posts/articles.html',{'id':profile.Id,'notifications':notif,'profile':profile})
            else:
                return redirect('general:verify')
        
        else: 
            return redirect('general:profile') 
        
    else:
        return redirect('general:login')

@login_required(login_url='/')
def ImagePostView(request):
    my_user = request.user
    #If you want to know if the user is logged in
    is_user_logged = my_user.is_authenticated
    if is_user_logged:
        profile=Profile.objects.get(user=my_user)
        notif=getNotifications(my_user)
        profile_data = Profile.objects.filter(user=my_user, Profile_incomplete=False)
        if profile_data.exists():
            if profile_data[0].Account_activated:
                trace=ImageTrace.objects.filter(User=my_user,type='image-post')
                if not trace.exists():
                    trace=ImageTrace.objects.create(User=my_user,type='image-post')
                    trace.save()
                else:
                    trace.update(Last_Image_Upload="",Current_Image="")
                return render(request, 'posts/image-posts.html',{'id':profile.Id,'notifications':notif,'profile':profile})
            else:
                return redirect('general:verify')
        
        else: 
            return redirect('general:profile')
        
    else:
        return redirect('general:login')

@login_required(login_url='/')
def VideoPostView(request):
    my_user = request.user
    #If you want to know if the user is logged in
    is_user_logged = my_user.is_authenticated
    if is_user_logged:
        print('ok')
        notif=getNotifications(my_user)
        profile=Profile.objects.filter(Profile_incomplete=False, user=my_user)[0]
        profile_data = Profile.objects.filter(Profile_incomplete=False, user=my_user)
        if profile_data.exists():
            if profile_data[0].Account_activated:
                trace=ImageTrace.objects.filter(User=my_user,type='video-post')
                if not trace.exists():
                    trace=ImageTrace.objects.create(User=my_user,type='video-post')
                    trace.save()
                else:
                    trace.update(Last_Image_Upload="",Current_Image="")
                return render(request, 'posts/video-posts.html',{'id':profile.Id,'notifications':notif,'profile':profile})
            else:
                return redirect('general:verify')
        
        else: 
            return redirect('general:profile')

    else:
        return redirect('general:login')

@login_required(login_url='/')
def MyPostView(request):#all Article view is also here
    my_user = request.user
    is_user_logged = my_user.is_authenticated
    if is_user_logged:
        articles=TextContent.objects.filter(User=my_user,Published=False)
        notif=getNotifications(my_user)
        profile= Profile.objects.filter(Profile_incomplete=False, user=my_user)[0]
        profile_data = Profile.objects.filter(Profile_incomplete=False, user=my_user)
        p = Paginator(articles.order_by('-Created_on'), 9)
        page_num = request.GET.get('page', 1)
        page = p.page(page_num)
        context={
            "articles":articles,
            'notifications':notif,
            'profile':profile,
            "pagination": page
             }
        if profile_data.exists():
            if profile_data[0].Account_activated:
                return render(request, 'posts/my-posts.html',context)
            else:
                return redirect('general:verify')
        else: 
            return redirect('general:profile')        
    else:
        return redirect('general:login')

@login_required(login_url='/')
def EditPostView(request,post_category,Id):
    my_user = request.user
    is_user_logged = my_user.is_authenticated
    notif=getNotifications(my_user)    
    profile= Profile.objects.filter(Profile_incomplete=False, user=my_user)[0]
    profile_data = Profile.objects.get(Profile_incomplete=False, user=my_user)
    if profile_data.Account_activated:
            if is_user_logged:
                if post_category=='article':
                    require_article=TextContent.objects.filter(User=my_user,Id=Id)[0]
                    img_name=os.path.basename(str(require_article.Feature_Image.url))
                    trace=ImageTrace.objects.filter(User=my_user,type='article-post')
                    if not trace.exists():
                        trace=ImageTrace.objects.create(User=my_user,Current_Image=img_name,type='article-post')
                        trace.save()
                    else:
                        trace.update(Current_Image=img_name)
                    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
                    print(img_name)   
                        
                    return render(request, 'posts/create-posts.html',{"article":require_article,"img_name":img_name,"notifications":notif,'profile':profile,'id':profile_data.Id})
                if post_category=='image':
                    require_img=ImageContent.objects.filter(User=my_user,Id=Id)[0]
                    img_name=(require_img.Image)
                    fileid=require_img.fileid
                    print("--------------------------------iiii----iii---iii-------")
                    print(img_name)
                    trace=ImageTrace.objects.filter(User=my_user,type='image-post')
                    if not trace.exists():
                        trace=ImageTrace.objects.create(User=my_user,Current_Image=img_name,type='image-post',fileid=fileid)
                        t=trace.save()
                        print(t)
                    else:
                        t=trace.update(Current_Image=img_name)
                        print(t)
                    return render(request, 'posts/image-posts.html',{"image":require_img,"img_name":img_name,'notifications':notif,'profile':profile,'id':profile_data.Id})
                if post_category=='video':
                    require_video=VideoContent.objects.filter(User=my_user,Id=Id)[0]
                    img_name=os.path.basename(str(require_video.Thumbnail))
                    trace=ImageTrace.objects.filter(User=my_user,type='video-post')
                    if not trace.exists():
                        trace=ImageTrace.objects.create(User=my_user,Current_Image=img_name,type='video-post')
                        trace.save()
                    else:
                        trace.update(Current_Image=img_name)
                    print(img_name)   
                    return render(request, 'posts/video-posts.html',{"video":require_video,"img_name":img_name,'notifications':notif,'profile':profile,'id':profile_data.Id})
                if post_category=='product':
                    require_products=StoreItem.objects.filter(User=my_user,Id=Id)[0]
                    img_name=os.path.basename(str(require_products.Image.url))
                    trace=ImageTrace.objects.filter(User=my_user,type='products')
                    if not trace.exists():
                        trace=ImageTrace.objects.create(User=my_user,Current_Image=img_name,type='products')
                        trace.save()
                    else:
                        trace.update(Current_Image=img_name)
                    print(img_name)

                    return render(request, 'Store/store.html',{"product":require_products,"img_name":img_name,'notifications':notif,'profile':profile,'id':profile_data.Id})
    else:
        return redirect('general:verify')
@login_required(login_url='/')
def UpdatePostView(request,post_category,Id):
    my_user = request.user
    is_user_logged = my_user.is_authenticated
    if is_user_logged and request.method=='POST':
        if post_category=='article':
               print("==============================================")
               complete_path= str(BASE_DIR)
               print(complete_path)
               headline=request.POST['headline']
               blog=request.POST['blog']
               option=request.POST['options']
               description=request.POST['description']
               trace=ImageTrace.objects.filter(User=my_user,type='article-post')  
               print("This is article category of the update Post section")
               print(request.POST)
               owner=Profile.objects.get(user=my_user)
               print(request.FILES)
               if option=='public':
                   is_free=True
               else:
                   is_free=False
               if 'image'in request.FILES:
                   t = request.FILES['image']
                   image = t.temporary_file_path()
                   upload = imagekit.upload(
                       file=open(image, "rb"),
                       file_name="image-post/" + str(my_user.email) + "/" + str(t),
                       options={
                           "response_fields": ["is_private_file", "tags"],

                       },
                   )
                   print('hy')
                   update_article=TextContent.objects.filter(User=my_user,Id=Id).update(
                        Headline=request.POST['headline'],
                       Feature_Image=upload['response']['url'],
                       fileid=upload["response"]['fileId'],
                        Description=description,
                        Content=blog,
                        Is_free=is_free,
                        Updated_on=str(datetime.datetime.now())


                    )
                   de = trace[0].fileid
                   print(de)
                   delete = imagekit.delete_file(de)
                   print(delete)
               else:
                   update_article = TextContent.objects.filter(User=my_user, Id=Id).update(
                   Headline=request.POST['headline'],
                   Description=description,
                   Content=blog,
                   Is_free=is_free,
                   Updated_on=str(datetime.datetime.now()))



               trace.delete()
               return redirect('post:mypost')
        if post_category=='image':
               print("+++++iiiiii+++mmmmmm+++aaaaaa+++gggggg+++eeeee++++")

               print(request.POST)
               headline=request.POST['headline'] 
               option=request.POST['options']

               description=request.POST['description']
               trace=ImageTrace.objects.filter(User=my_user,type='image-post')            
               owner=Profile.objects.get(user=my_user)
               print(request.FILES)
               if option=='public':
                   is_free=True
               else:
                   is_free=False
               if 'image' in request.FILES:
                   t = request.FILES['image']
                   image = t.temporary_file_path()
                   upload = imagekit.upload(
                       file=open(image, "rb"),
                       file_name="image-post/" + str(my_user.email) + "/" + str(t),
                       options={
                           "response_fields": ["is_private_file", "tags"],

                       },
                   )
                   update = ImageContent.objects.filter(User=my_user, Id=Id)
                   print(update[0].fileid)

                   delete = imagekit.delete_file(update[0].fileid)
                   print(delete)
                   print(upload['response']['url'])
                   update=ImageContent.objects.filter(User=my_user,Id=Id).update(
                        Headline=request.POST['headline'],
                       Image=upload['response']['url'],
                       fileid=upload["response"]['fileId'],
                       Description=description,
                        Is_free=is_free,
                        Updated_on=str(datetime.datetime.now())
                    )
                   print(trace[0].fileid)
                   de = trace[0].fileid
                   delete = imagekit.delete_file(de)
                   print(delete)
               else:
                   update = ImageContent.objects.filter(User=my_user, Id=Id).update(
                       Headline=request.POST['headline'],
                       Description=description,
                       Is_free=is_free,
                       Updated_on=str(datetime.datetime.now()))

               trace.delete()

               return redirect('post:allimagepost')
        if post_category=='video':
               ("-------vvvvvvvvvv---------iiiiiiii----ddddd-----------iiiiii-------oooooo------")
               complete_path= str(BASE_DIR)
               print(complete_path)
               headline=request.POST['headline']
               option=request.POST['options']
               description=request.POST['blog']
               trace=ImageTrace.objects.filter(User=my_user,type='video-post') 
               print("This is Video category of the update Post section")
               owner=Profile.objects.get(user=my_user)
               if option=='public':
                   is_free=True
               else:
                   is_free=False


               update = VideoContent.objects.filter(User=my_user, Id=Id)
               print(update[0].Link)

               print(request.FILES.getlist)

               if 'image' in request.FILES :
                   # a=request.FILES.getlist
                   t = request.FILES['image']
                   thumbnail=t.temporary_file_path()
                   r=client.upload_picture(f"/videos/{update[0].Link}", thumbnail, activate=True)
                   print(r)
                   if update[0].fileid != None:
                       delete = imagekit.delete_file(update[0].fileid)
                       print(delete)

                   upload = imagekit.upload(
                       file=open(thumbnail,'rb'),
                       file_name="image-post/" + str(my_user.email) + "/" + str(t),
                       options={
                           "response_fields": ["is_private_file", "tags"],

                       },
                   )
                   print(upload)
                   VideoContent.objects.filter(User=my_user, Id=Id).update(
                       Thumbnail=upload['response']['url'],
                       fileid=upload["response"]['fileId'],
                       Updated_on=str(datetime.datetime.now())

                   )
               if 'video' in request.FILES:
                   file = (request.FILES['video'])
                   print(file)
                   path = file.temporary_file_path()
                   print(path)
                   print(update)
                   print(update[0].Link)
                   iid=(update[0].Link)
                   video_uri = client.replace(
                       video_uri="/videos/"+iid,
                       filename=path
                   )
                   print(video_uri)
               update=VideoContent.objects.filter(User=my_user,Id=Id).update(
                    Title=request.POST['headline'],
                    Description=description,
                    Is_free=is_free,
                    Updated_on=str(datetime.datetime.now())
                )
               trace.delete()
               return redirect('post:allvideopost')
        if post_category=='product':
               print("===========PRODUCT===================================")
               complete_path= str(BASE_DIR)
               print(complete_path)
               headline=request.POST['headline']
               feature_image=request.POST['image']
               description=request.POST['blog']
               price=request.POST['price']
               trace=ImageTrace.objects.filter(User=my_user,type='products')
               print("This is product category of the update Post section")

               owner=Profile.objects.get(user=my_user)
    
                           
               update=StoreItem.objects.filter(User=my_user,Id=Id).update(
                    Headline=request.POST['headline'],
                    Image="products/"+my_user.email+"/"+trace[0].Current_Image,
                    Description=description,
                
                    Price=price,
                    Updated_on=str(datetime.datetime.now())

                    
                )
               trace.delete()
               return redirect('store:allproductpost')
    else:
        return redirect('general:login')


@login_required(login_url='/')
def AllVideosView(request):
    my_user = request.user
    is_user_logged = my_user.is_authenticated
    if is_user_logged:
        videos=VideoContent.objects.filter(User=my_user,Published=False)
        p = Paginator(videos.order_by('-Created_on'), 9)
        page_num = request.GET.get('page', 1)
        page = p.page(page_num)
        profile= Profile.objects.filter(Profile_incomplete=False, user=my_user)[0]
        profile_data = Profile.objects.filter(Profile_incomplete=False, user=my_user)
        context={
            "videos":videos,
            'profile': profile,
            "pagination": page
        }
        if profile_data.exists():
            if profile_data[0].Account_activated :
                return render(request, 'posts/myvideo-posts.html',context)
            else:
                return redirect('general:verify')
        else: 
            return redirect('general:profile')      
    else:
        return redirect('general:login')
    

@login_required(login_url='/')
def AllImagesView(request):    
    my_user = request.user
    is_user_logged = my_user.is_authenticated
    if is_user_logged:
        images=ImageContent.objects.filter(User=my_user,Published=False)
        p = Paginator(images.order_by("-Created_on"), 9)
        
        page_num = request.GET.get('page', 1)
        page = p.page(page_num)
        print(page)
        print(page)
        profile= Profile.objects.filter(Profile_incomplete=False, user=my_user)[0]
        profile_data = Profile.objects.filter(Profile_incomplete=False, user=my_user)
        context={
            "images":page,
            'profile': profile,
            "pagination": page
        }  
        if profile_data.exists():
            if profile_data[0].Account_activated:
                return render(request, 'posts/myimage-posts.html',context)
            else:
                return redirect('general:verify')
        
        else: 
            return redirect('general:profile')   
        
    else:
        return redirect('genral:login')
    
@login_required(login_url='/')
def DeletePostView(request,post_category,Id):
    if post_category=='article':
      p=TextContent.objects.get(Id=Id)
      delete = imagekit.delete_file(p.fileid)
      print(delete)
      # i=ImageTrace.objects.get(User=p.User)
      # delete = imagekit.delete_file(i.fileid)
      # print(delete)
      #
      # i.delete()
      p.delete()
      # complete_path=str(BASE_DIR)+"/media/"+str(p.Feature_Image)
      # subprocess.run(['rm',complete_path])
      return redirect("post:mypost")  
    elif post_category=='image':
      p=ImageContent.objects.get(Id=Id)
      print("--------------------------")
      print(p)
      delete = imagekit.delete_file(p.fileid)
      print(delete)
      p.delete()
      # complete_path=str(BASE_DIR)+"/media/"+str(p.Image)
      # subprocess.run(['rm',complete_path])
      return redirect("post:allimagepost")  
    elif post_category=='video':
      p=VideoContent.objects.get(Id=Id)
      print(p.Link)

      # complete_path=str(BASE_DIR)+"/media/"+str(p.Thumbnail)
      # subprocess.run(['rm',complete_path])
      u = client.delete(f"https://vimeo.com/manage/videos/{p.Link}")
      print(u.status_code)
      if u.status_code==200:
          p.delete()
      return redirect("post:allvideopost")     
    elif post_category=='product':
      p=StoreItem.objects.get(Id=Id)
      p.delete()
      complete_path=str(BASE_DIR)+"/media/"+str(p.Image)
      subprocess.run(['rm',complete_path])
      return redirect("store:allproductpost")
   
@login_required(login_url='/')     
def PublishPostView(request,post_category,Id):
    my_user=request.user
    if post_category=='article':
            p=TextContent.objects.filter(User=my_user,Id=Id).update(Published=True)
            is_free=TextContent.objects.get(User=my_user,Id=Id).Is_free
            created_on=TextContent.objects.get(User=my_user,Id=Id).Created_on
            updated_on=TextContent.objects.get(User=my_user,Id=Id).Updated_on
            created_on=list(created_on.timetuple())
            updated_on=list(updated_on.timetuple())
            for item in range(0,3):
                created_on.pop()
                updated_on.pop()
            profile=Profile.objects.get(user=my_user)
            my_followers=profile.my_followers.filter()
            my_subscribers=profile.My_subscribers.filter()
            post=TextContent.objects.get(User=my_user,Id=Id)
            
            print(my_followers)
            print(my_subscribers)

            if created_on == updated_on:#New Post Notification
                
                    if is_free:
                        notification=Notification.objects.create(
                            
                            Message="New Article Post Has Been Added By The " +str(my_user)+ " Have A Look To It",
                            Link="/post/"+str(my_user)+"/articles/"+str(post.Id)
                        )
                        notification.Send_to.set(my_followers)
                    else :
                        notification=Notification.objects.create(
                            Message="New Article Post Has Been Added By The " +str(my_user)+ " Have A Look To It",
                            Link="/post/"+str(my_user)+"/articles/"+str(post.Id)
                        )
                        notification.Send_to.set(my_subscribers)
            else :#Updated Post Notification
                
                    if is_free:
                        notification=Notification.objects.create(
                            
                            Message="Article  Has Been Updated By The " +str(my_user)+ " Have A Look To It",
                            Link="/post/"+str(my_user)+"/articles/"+str(post.Id)
                        )
                        notification.Send_to.set(my_followers)
                    else :
                        notification=Notification.objects.create(
                            Message="Article  Has Been Updated By The " +str(my_user)+ " Have A Look",
                            Link="/post/"+str(my_user)+"/articles/"+str(post.Id)
                        )
                        notification.Send_to.set(my_subscribers)
                
            return redirect("post:mypost")  
  
    elif post_category=='image':
            p=ImageContent.objects.filter(User=my_user,Id=Id).update(Published=True)
            is_free=ImageContent.objects.get(User=my_user,Id=Id).Is_free
            created_on=ImageContent.objects.get(User=my_user,Id=Id).Created_on
            updated_on=ImageContent.objects.get(User=my_user,Id=Id).Updated_on
            created_on=list(created_on.timetuple())
            updated_on=list(updated_on.timetuple())
            for item in range(0,3):
                created_on.pop()
                updated_on.pop()
            profile=Profile.objects.get(user=my_user)
            my_followers=profile.my_followers.filter()
            my_subscribers=profile.My_subscribers.filter()
            
            print(my_followers)
            print(my_subscribers)
            post=ImageContent.objects.get(User=my_user,Id=Id)
            if created_on == updated_on:#New Post Notification
                
                    if is_free:
                        notification=Notification.objects.create(
                            
                            Message="New Image Post Has Been Added By The " +str(my_user)+ " Have A Look To It",
                            Link="/post/"+str(my_user)+"/images/"+str(post.Id)
                        )
                        notification.Send_to.set(my_followers)
                    else :
                        notification=Notification.objects.create(
                            Message="New Image Post Has Been Added By The " +str(my_user)+ " Have A Look To It",
                            Link="/post/"+str(my_user)+"/images/"+str(post.Id)
                        )
                        notification.Send_to.set(my_subscribers)
            else :#Updated Post Notification
                
                    if is_free:
                        notification=Notification.objects.create(
                            
                            Message="Image Post  Has Been Updated By The " +str(my_user)+ " Have A Look To It"
                        )
                        notification.Send_to.set(my_followers)
                    else :
                        notification=Notification.objects.create(
                            Message="Image Post  Has Been Updated By The " +str(my_user)+ " Have A Look"
                        )
                        notification.Send_to.set(my_subscribers)
            return redirect("post:allimagepost")
    
    elif post_category=='video':
            p=VideoContent.objects.filter(User=my_user,Id=Id).update(Published=True)
            is_free=VideoContent.objects.get(User=my_user,Id=Id).Is_free
            created_on=VideoContent.objects.get(User=my_user,Id=Id).Created_on
            updated_on=VideoContent.objects.get(User=my_user,Id=Id).Updated_on
            created_on=list(created_on.timetuple())
            updated_on=list(updated_on.timetuple())
            for item in range(0,3):
                created_on.pop()
                updated_on.pop()
            profile=Profile.objects.get(user=my_user)
            my_followers=profile.my_followers.filter()
            my_subscribers=profile.My_subscribers.filter()
            print(my_followers)
            print(my_subscribers)
            post=VideoContent.objects.get(User=my_user,Id=Id)

            if created_on == updated_on:#New Post Notification
                
                    if is_free:
                        notification=Notification.objects.create(
                            
                            Message="New Video Post Has Been Added By The " +str(my_user)+ " Have A Look To It",
                            Link="/post/"+str(my_user)+"/videos/"+str(post.Id)
                            
                        )
                        notification.Send_to.set(my_followers)
                    else :
                        notification=Notification.objects.create(
                            Message="New Video Post Has Been Added By The " +str(my_user)+ " Have A Look To It",
                            Link="/post/"+str(my_user)+"/videos/"+str(post.Id)
                            
                        )
                        notification.Send_to.set(my_subscribers)
            else :#Updated Post Notification
                
                    if is_free:
                        notification=Notification.objects.create(
                            
                            Message="Video Post Has Been Updated By The " +str(my_user)+ " Have A Look To It",
                            Link="/post/"+str(my_user)+"/videos/"+str(post.Id)
                            
                        )
                        notification.Send_to.set(my_followers)
                    else :
                        notification=Notification.objects.create(
                            Message="Video Post  Has Been Updated By The " +str(my_user)+ " Have A Look",
                            Link="/post/"+str(my_user)+"/videos/"+str(post.Id)
                            
                        )
                        notification.Send_to.set(my_subscribers)      
            return redirect("post:allvideopost")
       
    elif post_category=='product':
            StoreItem.objects.filter(User=my_user,Id=Id).update(Published=True)
            p=StoreItem.objects.get(User=my_user,Id=Id)
           
            created_on=StoreItem.objects.get(User=my_user,Id=Id).Created_on
            updated_on=StoreItem.objects.get(User=my_user,Id=Id).Updated_on
            created_on=list(created_on.timetuple())
            updated_on=list(updated_on.timetuple())
            for item in range(0,3):
                created_on.pop()
                updated_on.pop()
            profile=Profile.objects.get(user=my_user)
            my_followers=profile.my_followers.filter()
            my_subscribers=profile.My_subscribers.filter()
            print(my_followers)
            print(my_subscribers)

            if created_on == updated_on:#New Post Notification
                
                    
                        notification=Notification.objects.create(
                            
                            Message="New Product Has Been Added By The " +str(my_user)+ " Have A Look To It",
                            Link="/post/"+str(my_user)+"/products/"+str(p.Id)
                            
                        )
                        notification.Send_to.set(my_followers)
    
            else :#Updated Post Notification
                
               
                        notification=Notification.objects.create(
                            
                            Message="Product Has Been Updated By The " +str(my_user)+ " Have A Look To It",
                            Link="/"+ str(my_user) +"/user-profile/products/"
                            
                        )
                        notification.Send_to.set(my_followers)
 
  
            return redirect("store:allproductpost")

@login_required(login_url='/') 
def UnPublishPostView(request,post_category,Id):
    my_user=request.user
    if post_category=='article':
      p=TextContent.objects.filter(User=my_user,Id=Id).update(Published=False)
      return redirect("post:mypost")  
  
    elif post_category=='image':
      p=ImageContent.objects.filter(User=my_user,Id=Id).update(Published=False)
      return redirect("post:allimagepost")
    
    elif post_category=='video':
      p=VideoContent.objects.filter(User=my_user,Id=Id).update(Published=False)
      return redirect("post:allvideopost")
       
    elif post_category=='product':
      p=StoreItem.objects.filter(User=my_user,Id=Id).update(Published=False)
      return redirect("store:allproductpost")


def PublishedPostView(request,post_category):
    my_user=request.user
    notif=getNotifications(my_user)
    profile= Profile.objects.filter(Profile_incomplete=False, user=my_user)[0]
    profile_data = Profile.objects.get(Profile_incomplete=False, user=my_user)
    if post_category=='article':
      p=TextContent.objects.filter(User=my_user,Published=True)
      context={
          "published_articles":p,
          "in_publish":True,
          'notifications':notif,
          'profile':profile
      }
      return render(request,'posts/my-posts.html',context) 
  
    elif post_category=='image':
      p=ImageContent.objects.filter(User=my_user,Published=True)
      context={
          "published_images":p,
          "in_publish":True,
          'notifications':notif,
          'profile':profile
      }
      return render(request,'posts/myimage-posts.html',context) 
      
    
    elif post_category=='video':
      p=VideoContent.objects.filter(User=my_user,Published=True)
      context={
          "published_videos":p,
          "in_publish":True,
          'notifications':notif,
          'profile':profile
      }
      print(p)
      return render(request,'posts/myvideo-posts.html',context) 
      
       
    elif post_category=='product':
      p=StoreItem.objects.filter(User=my_user,Published=True)
      context={
          "published_products":p,
          "in_publish":True,
          'notifications':notif,
          'profile':profile
      }
      return render(request,'Store/allitems.html',context) 
    



    
@login_required(login_url='/')
def SavePostView(request,post_category):
    print(post_category)
    my_user = request.user
    notif=getNotifications(my_user)
    profile= Profile.objects.filter(Profile_incomplete=False, user=my_user)[0]
    profile_data = Profile.objects.get(Profile_incomplete=False, user=my_user)
    #If you want to know if the user is logged in
    is_user_logged = my_user.is_authenticated
    if is_user_logged and request.method=="POST":
        if post_category=="image":

               try:
                   de = ImageTrace.objects.get(User=my_user,type="image-post")
                   print(de.fileid)
                   delete = imagekit.delete_file(de.fileid)
                   print(delete)
                   print('hello')
                   ImageTrace.objects.get(User=my_user,type="image-post").delete()
               except:
                   pass
               headline=request.POST['headline']
               t = request.FILES['image']
               image = t.temporary_file_path()
               # print(image)
               description=request.POST['description']
               option=request.POST['options']
               
               print("This is image category of the save Post section")
               print(headline,str(image),description,option)
               owner=Profile.objects.get(user=my_user)
               if option=='public':
                   is_free=True
               else:
                   is_free=False
               upload = imagekit.upload(
                   file=open(image, "rb"),
                   file_name="image-post/" + str(my_user.email) + "/" + str(image),
                   options={
                       "response_fields": ["is_private_file", "tags"],

                   },
               )
               print(upload)
               print(upload["response"]["url"])
               print(upload["response"]['fileId'])
               image_content_obj=ImageContent.objects.create(User=my_user,
                              Headline=headline,
                              Image=upload["response"]["url"],
                              Description=description,
                              fileid=upload["response"]['fileId'],
                              Is_free=is_free,
                              Owner=owner,
                              Created_on=str(datetime.datetime.now()),
                              Updated_on=str(datetime.datetime.now()),
                              )
               image_content_obj.save()
               # path = os.path.join("./media/image-post/",image)
               # image.save(path)
               print("Upload binary", upload)
               return redirect("/profile/dashboard/all-image-post/")                

        elif post_category=="article":

               try:
                    de=ImageTrace.objects.get(User=my_user, type="article-post")
                    print(de.fileid)
                    delete = imagekit.delete_file(de.fileid)
                    print(delete)
                    print('hello')
                    ImageTrace.objects.get(User=my_user,type="article-post").delete()
               except:
                   pass
               headline=request.POST['headline']

               blog=request.POST['blog']
               option=request.POST['options']
               description=request.POST['description']
               
               print("This is article category of the save Post section")
               print(headline,blog,option)
               owner=Profile.objects.get(user=my_user)
               if option=='public':
                   is_free=True
               else:
                   is_free=False
               print(request.FILES)
               t = request.FILES['image']
               image = t.temporary_file_path()
               upload = imagekit.upload(
                   file=open(image, "rb"),
                   file_name="image-post/" + str(my_user.email) + "/" + str(t),
                   options={
                       "response_fields": ["is_private_file", "tags"],

                   },
               )
               text_content_obj=TextContent.objects.create(
                              User=my_user,
                              
                              Feature_Image=upload['response']['url'],
                              fileid=upload["response"]['fileId'],
                              Headline=headline,
                              Content=blog,
                              Is_free=is_free,
                              Owner=owner,
                              Description=description,
                              Created_on=str(datetime.datetime.now()),
                              Updated_on=str(datetime.datetime.now()),
                              )
               text_content_obj.save()
               return redirect("/profile/dashboard/my-post/")

        elif post_category=="video":
               # ImageTrace.objects.get(User=my_user,type="video-post").delete()
               # yt_link = re.compile(r'(https?://)?(www\.)?((youtu\.be/)|(youtube\.com/watch/?\?v=))([A-Za-z0-9-_]+)', re.I)
               # yt_embed = "https://www.youtube.com/embed/{0}"
               upload=''
               try:
                    de=ImageTrace.objects.get(User=my_user, type="video-post")
                    print(de.fileid)
                    delete = imagekit.delete_file(de.fileid)
                    print(delete)
                    print('hello')
                    ImageTrace.objects.get(User=my_user,type="video-post").delete()
               except:
                   pass



               print(request.FILES.getlist)
               print(len(request.FILES))

               # if file:
               #     # filename = secure_filename(file.filename)
               #     file.save(os.path.join('./media', file))
               print(request.POST)
               # video_url=str(request.POST['video'])
               # video_url=yt_link.sub(lambda match: yt_embed.format(match.groups()[5]), video_url)
               headline=request.POST['headline']
               # thumbnail=request.POST['image']
               option=request.POST['options']
               description=request.POST['blog']
               # video = request.POST['video']
               print("This is video category of the save Post section")




               owner=Profile.objects.get(user=my_user)
               if option=='public':
                   is_free=True
               else:
                   is_free=False


               if  len(request.FILES)>1:
                   file = (request.FILES['video'])
                   print(request.FILES)
                   path = file.temporary_file_path()
                   # a=request.FILES.getlist
                   file_name = path
                   uri = client.upload(file_name)

                   print(uri)
                   a = uri.split("/")
                   print(a[2])
                   t = request.FILES['image']
                   thumbnail = t.temporary_file_path()
                   rs_picture = client.upload_picture(uri, thumbnail, activate=True)
                   print(rs_picture)
                   upload = imagekit.upload(
                       file=open(thumbnail,'rb'),
                       file_name="image-post/" + str(my_user.email) + "/" + str(file),
                       options={
                           "response_fields": ["is_private_file", "tags"],

                       },
                   )
                   print(upload)
                   video_content_obj = VideoContent.objects.create(
                       User=my_user,
                       Link=a[2],
                       Title=headline,
                       Thumbnail=upload['response']['url'],
                       fileid=upload["response"]['fileId'],
                       Description=description,
                       Is_free=is_free,
                       Owner=owner,
                       Created_on=str(datetime.datetime.now()),
                       Updated_on=str(datetime.datetime.now()),
                   )
                   video_content_obj.save()
               elif 'image' not in request.FILES:
                   file = (request.FILES['video'])
                   path = file.temporary_file_path()
                   file_name = path
                   uri = client.upload(file_name)

                   print(uri)
                   a = uri.split("/")
                   print(a[2])
                   video_content_obj = VideoContent.objects.create(
                       User=my_user,
                       Link=a[2],
                       Title=headline,
                       Description=description,
                       Is_free=is_free,
                       Owner=owner,
                       Created_on=str(datetime.datetime.now()),
                       Updated_on=str(datetime.datetime.now()),
                   )
                   video_content_obj.save()
               return redirect("/profile/dashboard/all-video-post/")                
                              
        elif post_category=="product":
               headline=request.POST['headline']
               thumbnail=request.POST['image']
             
               ImageTrace.objects.get(User=my_user,type="products").delete()
               description=request.POST['blog']
               price=request.POST['price']
               print("This is product category of the save Post section")
        
               owner=Profile.objects.get(user=my_user)

               store_content_obj=StoreItem.objects.create(
                              User=my_user,
                              Headline=headline,
                              Image="products/"+str(my_user.email)+"/"+thumbnail,
                              Description=description,
                              Created_on=str(datetime.datetime.now()),
                              Updated_on=str(datetime.datetime.now()),
                              Owner=owner,
                              Price=float(price)
                            
                              )
               store_content_obj.save()
               return redirect("/profile/dashboard/all-product-post/")                

    return redirect("general:login")

#all checked. Just that liking doesn't redirects and works only in new tab.
@csrf_exempt
@login_required(login_url='/')
def LikeBtnView(request):
    if request.method=='POST':
        json_data=json.loads(request.body)
        visitor_profile=Profile.objects.get(user=request.user)
        profile=Profile.objects.get(username=json_data['username'])

        profile_data = Profile.objects.filter(Profile_incomplete=False, user=request.user)

        post_id=json_data['postId']
        post_category=json_data['type']
        if profile_data.exists():
            if profile_data[0].Account_activated:
                if post_category=='article':
                    like=Likes.objects.filter(Post_id=json_data['postId'], Like_by=visitor_profile,type='article')
                    post=TextContent.objects.get(Id=uuid.UUID(post_id))
                    if like.exists():
                        post.Like_count -= 1
                        post.save()
                        like[0].delete()
                        return JsonResponse({'res':False})
                        
                    else:
                        new_like=Likes.objects.create(
                            Like_by=visitor_profile,
                            Like_To=profile,
                            Post_id=post_id,
                            type='article'
                            )
                        new_like.save()
                        post.Like_count+= 1
                        post.save()
                        return JsonResponse({'res':True})
                        
                elif post_category=='video':
                    like=Likes.objects.filter(Post_id=json_data['postId'], Like_by=visitor_profile,type="video")
                    post=VideoContent.objects.get(Id=uuid.UUID(post_id))
                    if like.exists():
                        post.Like_count -= 1
                        post.save()
                        like[0].delete()
              
                        return JsonResponse({'res':False})

                    else:
                        new_like=Likes.objects.create(
                            Like_by=visitor_profile,
                            Like_To=profile,
                            Post_id=post_id,
                            type='video'
                            
                            )
                        new_like.save()
                        post.Like_count+= 1
                        post.save()
                    
                        return JsonResponse({'res':True})
                elif post_category=='image':
                    like=Likes.objects.filter(Post_id=json_data['postId'], Like_by=visitor_profile,type="image")
                    post=ImageContent.objects.get(Id=uuid.UUID(post_id))
                    if like.exists():
                        post.Like_count -= 1
                        post.save()
                        like[0].delete()
                   
                        return JsonResponse({'res':False})
                    else:
                        new_like=Likes.objects.create(
                            Like_by=visitor_profile,
                            Like_To=profile,
                            Post_id=post_id,
                            type='image'
                            
                            )
                        new_like.save()
                        post.Like_count+= 1
                        post.save()
              
                        return JsonResponse({'res':True})
                elif post_category=='product':
                    post=StoreItem.objects.get(Id=uuid.UUID(post_id))
                    if like.exists():
                        post.Like_count -= 1
                        post.save()
                        like[0].delete()
                    
                        return JsonResponse({'res':True})
                    else:
                        new_like=Likes.objects.create(
                            Like_by=visitor_profile,
                            Like_To=profile,
                            Post_id=post_id
                            )
                        new_like.save()
                        post.Like_count+= 1
                        post.save()
              
                        return JsonResponse({'res':True})
            else:
                return redirect('general:verify')
        else:
            return redirect('general:profile')
