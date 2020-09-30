from django.shortcuts import render,redirect

# Create your views here.
from .models import Report,Doctor
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.http import HttpResponse, HttpResponseRedirect

from django.shortcuts import render
import pickle
model=pickle.load(open('./model/breast_cancer.pkl','rb+'))


import math
import pandas as pd








@login_required(login_url='welcome')
def result(request):
    if request.method=='POST':
        
        temp={}
        

        temp['texture']=float(request.POST.get('texture'))
        
        temp['radius']=float(request.POST.get('radius'))
        temp['perimeter']=float(request.POST.get('perimeter'))
        temp['smoothness']=float(request.POST.get('smoothness'))
        

        temp['area']=float(request.POST.get('area'))

        a=(request.POST.get('age'))
        n=(request.POST.get('name'))

        t=(request.POST.get('texture'))
        
        r=(request.POST.get('radius'))
        p=(request.POST.get('perimeter'))
        s=(request.POST.get('smoothness'))
        

        ar=request.POST.get('area')
        
        testdata=pd.DataFrame({'x':temp}).transpose()
        scoreval=model.predict(testdata)[0]
        if scoreval==0:
            ans="Benign"
        else:
            ans="Malignant"
        


        report=Report(user= request.user)

        
        report.age=a
        report.name=n
        report.texture=t
        report.radius=r
        report.perimeter=p
        report.smoothness=s
        report.area=ar
        report.result=ans
        
        
        
        
        report.save()
            
        return render(request,'result.html',{'ans':ans,'area':ar,'texture':t,'radius':r,'perimeter':p,'smoothness':s})
        


    else:
        return render(request,'index.html')


def register(request):
   
    return render (request,'signup.html')


@login_required(login_url='welcome')
def report(request):
    log_user=request.user
    report=Report.objects.filter(user=log_user)
    return render (request,"report.html",{'report':report})

@login_required(login_url='welcome')
def home(request):
     return render (request,"index.html")



def signup(request):
    
    if request.method=="POST":
        email=request.POST['email']
        pass1=request.POST['pass1']
        pass2=request.POST['pass2']
        username=request.POST['username']

        if pass1 == pass2:
            if User.objects.filter(username=username).exists():
                 messages.info(request,"Username already used. !!")
                 return render (request,"signup.html")
            
            if User.objects.filter(email=email).exists():
                    messages.info(request,"Email address already used. !!")
                    return render (request,"signup.html")
                
            else:
                user=User.objects.create_user(email=email,password=pass1,username=username)
                user.save()
                
                messages.info(request,"Congratulations your account is created successfully. !")
                return render (request,"login.html")

        else:
            messages.info(request,"OOPS! Password is not matching.")
            return render (request,"signup.html")
 
        return render (request,"signup.html")

def enter(request):
    return render(request,'login.html')


def login(request):
    username=request.POST['username']
    passw=request.POST['pass']

    user =auth.authenticate(username=username,password=passw)
    if user is not None:
        auth.login(request,user)
        return render (request,"about.html")
    else:
        messages.info(request,"Sorry! Account does not Exist.")
        return render (request,"login.html")


lat1=[[77.1354, 28.7243],[77.125747, 28.693297],[77.09444, 28.62],[77.055118, 28.616834],
[77.274074, 28.689589],[77.2688, 28.5149],[77.1775, 28.51583],[77.1886, 28.6516
],[77.1783, 28.7053],
[77.17189, 28.59153],[77.2198, 28.6328],[77.278787, 28.633606]]

lat2=[[80.91583, 26.86056],[77.6824, 28.9927],[78.08, 27.88],[83.00611, 25.30694],[78.56962, 25.44862],
[80.33111, 26.4725],[78.02, 27.18],[82.20056, 26.80361],[79.415, 28.364],
[81.85, 25.45],[77.32, 28.57],[77.41667, 28.66667]]


@login_required(login_url='welcome')
def searching(request):
    
    if request.method=='POST':
        
        an=(request.POST['city'])
        if an=="01":
            doctor=Doctor.objects.all().filter(state="Delhi")
            mapbox_access_token ='pk.eyJ1IjoiamF5YTIzMjAiLCJhIjoiY2tmZ3JtOHAxMGR0dDJ4czJ3NjB5OWh5aiJ9.nazMXRwj1p5pvDqbXArwrA'
            return render (request,'location1.html',
            {'mapbox_access_token':mapbox_access_token,'loc':lat1,'corn':[77.21667, 28.66667],'zoom':10.56,'doctor':doctor})
        elif an=="02":
            doctor=Doctor.objects.all().filter(state="U.P")
            mapbox_access_token ='pk.eyJ1IjoiamF5YTIzMjAiLCJhIjoiY2tmZ3JtOHAxMGR0dDJ4czJ3NjB5OWh5aiJ9.nazMXRwj1p5pvDqbXArwrA'
            return render (request,'location1.html',
            {'mapbox_access_token':mapbox_access_token,'loc':lat2,'corn':[80.50194282009, 27.3408313733408],'zoom':6,'doctor':doctor})
        
        else:
            mapbox_access_token ='pk.eyJ1IjoiamF5YTIzMjAiLCJhIjoiY2tmZ3JtOHAxMGR0dDJ4czJ3NjB5OWh5aiJ9.nazMXRwj1p5pvDqbXArwrA'
            return render (request,'location.html',{'mapbox_access_token':mapbox_access_token})
      

@login_required(login_url='welcome')
def find(request):
    mapbox_access_token ='pk.eyJ1IjoiamF5YTIzMjAiLCJhIjoiY2tmZ3JtOHAxMGR0dDJ4czJ3NjB5OWh5aiJ9.nazMXRwj1p5pvDqbXArwrA'
    return render (request,'location.html',{'mapbox_access_token':mapbox_access_token})

@login_required(login_url='welcome')
def submit(request):
    messages.info(request,"Your report is submitted successfully. Doctor will contact you soon.")
    mapbox_access_token ='pk.eyJ1IjoiamF5YTIzMjAiLCJhIjoiY2tmZ3JtOHAxMGR0dDJ4czJ3NjB5OWh5aiJ9.nazMXRwj1p5pvDqbXArwrA'
    return render (request,'location.html',{'mapbox_access_token':mapbox_access_token})

@login_required(login_url='welcome')
def logout(request):
    auth.logout(request)
    return render (request,'about.html')

def welcome(request):
    return render (request, "about.html")