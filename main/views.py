from django.shortcuts import render, HttpResponse, redirect
from .models import image, Category
from django.db.models import Q
import urllib.request
import random
from winreg import *
import json
from django.contrib import messages
from django.utils.encoding import smart_str
from django.contrib.auth.models import User
from django.contrib.auth import login as auth_login, authenticate, logout
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import datetime
from PIL import Image
from validate_email import validate_email
# Create your views here.

def home(request, category=None):
    images=image.objects.all()
    query=request.GET.get("query")
    if query:
        products=image.objects.filter(
            Q(title__icontains=query) |
            Q(tags__icontains=query) |
            Q(category__icontains=query)
            ).distinct()
        return render(request, 'home.html', {'images':products, 'query':query})
    return render(request, 'home.html', {'images':images})

def category(request, category):
    images=image.objects.filter(category=category)
    return render(request, 'home.html', {'images':images, 'cat':category})

def login(request):
    return render(request, 'login.html')

def login_signin(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        is_valid = validate_email(email)
        if is_valid == True:
            u = User.objects.filter(email=email)
            if len(u) > 0:
                user=authenticate(username=u[0],password=password)
                if user is not None:
                    if user.is_active:
                        auth_login(request, user)
                        return redirect("main:home")
                    else:
                        messages.info(request,"Your account has been deactivated!")
                        return redirect("main:login")
                else:
                    messages.info(request,"Wrong Email ID or password!")
                    return redirect("main:login")
            else:

                messages.info(request,"User does not exists!")
                return redirect("main:login")
        else:
            user=authenticate(username=email,password=password)
            if user is not None:
                if user.is_active:
                    auth_login(request, user)
                    return redirect("main:home")
                else:
                    messages.info(request,"Your account has been deactivated!")
                    return redirect("main:login")
            else:
                messages.info(request,"Wrong username or password!")
                return redirect("main:login")
    return render(request, 'login.html')

def signup(request):
    if request.method == "POST":
        fname = request.POST.get("fname")
        lname = request.POST.get("lname")
        email = request.POST.get("email")
        password = request.POST.get("password")
        username = request.POST.get("username")

        u=User.objects.filter(username=username)
        if len(u) != 0:
            messages.error(request,"Username already exists!")
            context={
                'fname':fname,
                'lname':lname,
                'email':email,
                'password':password
            }
            return render(request, 'login.html', context)
        else: 
            if fname != "" and lname != "" and email != "" and password != "":
                user=User.objects.create_user(username, email ,password)
                user.save()
                return redirect("main:home")
            else:
                messages.error(request,"All fields are required!")
                context={
                    'fname':fname,
                    'lname':lname,
                    'email':email,
                    'password':password
                }
                return render(request, 'login.html', context)
    else:
        return redirect("main:login")

def logouts(request):
    logout(request)
    return redirect("main:home")

@login_required
@csrf_exempt
def like(request,pid):
    if request.method == "POST":
        like = "like"
        picid = pid
        like = request.POST.get("liked")
        response_data = {}

        pic = image.objects.get(id=picid)
        if like == "like":
            if pic.likes is not None:
                pic.likes =pic.likes+"/"+str(request.user.id)
            else: pic.likes = request.user.id
        else:
            sp=pic.likes.split("/")
            spnew=[]
            for s in sp:
                if s != str(request.user.id):
                    spnew.append(s)
            st="/".join(spnew)
            pic.likes = st

        pic.save()

        im=image.objects.get(id=pid)
        lk = im.likes
        sp = lk.split("/")
        count=0
        for s in sp:
            if s != "":
                count = count+1

        response_data['like_count'] = count
        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )
        #return HttpResponse('')

@login_required
@csrf_exempt
def comment(request, pid):
    if request.method == "POST":
        comment = request.POST.get("comment")
        picid = pid
        response_data = {}

        pic = image.objects.get(id = picid)
        com = pic.comments
        currentDT = datetime.datetime.now()
        cdt=str(currentDT.year)+"-"+str(currentDT.month)+"-"+str(currentDT.day)+"("+str(currentDT.hour)+":"+str(currentDT.minute)+")"
        if com != None:
            pic.comments = pic.comments + "," +str(request.user.id)+"/"+comment+"/"+cdt
            pic.save()
        else:
            pic.comments = str(request.user.id) + "/"+comment+"/"+cdt
            pic.save()

        nm=User.objects.get(id=request.user.id)
        response_data['name'] = nm.username
        response_data['comment'] = comment
        response_data['time'] = cdt
        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )

def detail(request, pid):
    pic = image.objects.get(id = pid)
    print(request.path)
    return render(request, 'detail.html', {'pic':pic})

def admin_page(request):
    pic = image.objects.all()
    like_count=0
    pic_count=0
    comment_count=0
    for p in pic:
        pic_count=pic_count+1
        lk=p.likes
        cm=p.comments
        if lk != None:
            sp=lk.split("/")
            for s in sp:
                if s != "":
                    like_count = like_count + 1
        if cm != None:
            c=cm.split(",")
            for cc in c:
                if cc != "":
                    comment_count = comment_count + 1
    context={
        'like_count':like_count,
        'comment_count':comment_count,
        'pic_count':pic_count
    }

    return render(request, "admin.html", context)

def upload_image(request):
    if request.method == "POST":
        ti=request.POST.get('title')
        cat=request.POST.get('cat')
        gid=request.POST.get('id')
        photog=request.POST.get('photographer')
        tags=request.POST.get('tags')

        if ti != "" and cat != "Select category..." and gid != "" and photog != "" and tags != "":
            im=image()
            im.title = ti
            im.category = cat
            im.url = "https://drive.google.com/uc?export=download&id="+gid
            im.photographer = photog
            im.tags = tags
            im.save()
            messages.success(request, "Image upload successful!")
            return render(request, 'upload.html')
        else:
            messages.error(request, "All fields are required!")
            return redirect('main:upload_image')
    else:
        cat=Category.objects.all()
        return render(request, 'upload.html', {'category':cat})

def add_category(request):
    if request.method == "POST":
        cat = request.POST.get("cat")
        c=Category()
        c.name=cat
        c.save()
        return redirect("main:admin_page")
    else:
        return redirect("main:admin_page")

@csrf_exempt
def update_category(request):
    if request.method == "POST":
        response_data = {}
        cid=request.POST.get("cid")
        categ=Category.objects.get(id=cid)
        cat=request.POST.get("cat")
        categ.name=cat
        categ.save()

        c=Category.objects.all()
        response_data['cat_count']=len(c) 
        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )

@csrf_exempt
def count_download(request,picid):
    if request.method == "POST":
        pid = request.POST.get("picid")
        pic = image.objects.get(id=picid)
        c=pic.downloads
        cnew=c+1
        pic.downloads = cnew
        pic.save()
        return HttpResponse('')