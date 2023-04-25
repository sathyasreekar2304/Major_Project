from django.shortcuts import render, redirect

# Create your views here.

from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model
import numpy as np
from . models import *
import os


def add_doctor(request):
    if request.method == 'POST':
        lname=request.POST['docname']
        lemail=request.POST['email']
        lphone=request.POST['phnumber']
        laddress=request.POST['add']
        data=Doctor(dname=lname,demail=lemail,dphone=lphone,daddress=laddress)
        data.save()
        teext='Doctor Added'
        return render(request,'adddoctor.html',{"text":teext})
    return render(request, "adddoctor.html")

# Create your views here.

def login(request):
    if request.method=='POST':
        lemail=request.POST['email']
        lpassword=request.POST['psw']

        d=Register.objects.filter(remail=lemail,rpassword=lpassword).exists()
        print(d)
        return render (request,"upload.html")

    return render(request,'login.html',{})

def register(request):
    if request.method=='POST':
        email=request.POST['useremail']
        password=request.POST['psw']
        conpassword=request.POST['conpassword']
        print(email,password,conpassword)
        if password==conpassword:
            a=Register(remail=email,rpassword=password)
            a.save()
            msg="succesfully registered"
            return render(request,'login.html',{"message":msg})
        else:
            msg='Register failed!!'
            return render(request,'register.html')

        
    return render(request,'register.html')


          
    
def index(request):
    return render(request, "index.html")

def about(request):
    return render(request,"about.html")

def stages(request):
    if request.method=='POST':
        Classes=[]
        paths=os.listdir('app/data/')
        for i in paths:
            Classes.append(i)
        File=request.FILES['brain']
        print(File)
        s=Brain(image=File)
        s.save()
        path1='app/static/saved/' + s.Imagename()
        model=load_model('app/models/CNN_1.h5')
        x1=image.load_img(path1,target_size=(128,128))
        x1=image.img_to_array(x1)
        x1=np.expand_dims(x1,axis=0)
        x1/=255
        result= model.predict(x1)        
        # a = classes[]
        b = np.argmax(result)
        results=Classes[b]
        print(results)
        from random import randint
        # count = Doctor.objects.count()
        # print(count)
        dc = Doctor.objects.all().order_by('?')[:4]
        print(dc)

        return render(request,"result.html",{"message":results,"DOC":dc,"path":'/static/saved/' + s.Imagename()})
    return render(request,"stages.html")


def upload(request):
    if request.method=='POST':
        pdfs=request.FILES['pdf']
        p=Pdf(image=pdfs)
        p.save()
        wbc=15
        if wbc>= 16:
            text= "Acute Lymphoblastic Leukemia Disease Positive"
        else:		  
            text="Acute Lymphoblastic Leukemia Disease Negative"
        print(text)
        return render(request,"pdfresult.html",{'pdfr':text})

    return render (request,"upload.html")

