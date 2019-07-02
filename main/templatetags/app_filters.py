from django import template
from django.template.defaultfilters import stringfilter
from django.shortcuts import HttpResponse
from django.contrib import messages
register = template.Library()

@register.filter(name='getlike')
@stringfilter
def splitname(picid, arg):
    from main.models import image
    like = "dislike" 
    pic = image.objects.get(id=picid)
    likelist = pic.likes
    if likelist != None:
        sp = likelist.split("/")
        for s in sp:
            if s == str(arg):
                like = "like"
    return like

@register.filter(name='get_comments')
@stringfilter
def get_comments(string):
    sp = string.split(",")
    return sp

@register.filter(name='getcomment')
@stringfilter
def getcomment(string):
    sp = string.split("/")
    return sp[1]

@register.filter(name='gettime')
@stringfilter
def gettime(string):
    t=""
    sp = string.split("/")
    if len(sp) >2:
        t=sp[2]
    return t

@register.filter(name='getname')
@stringfilter
def getname(string):
    from django.contrib.auth.models import User
    if string != "":
        sp = string.split("/")
        name = User.objects.get(id=sp[0]).username
        return name
    else:
        return ""

@register.filter(name='like_count')
@stringfilter
def like_count(string):
    from main.models import image
    im=image.objects.get(id=string)
    lk = im.likes
    count=0
    if lk is not None:
        sp = lk.split("/")
        for s in sp:
            if s != "":
                count = count+1
    return count