from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User,auth
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.views.decorators.cache import never_cache
from django.db.models import Q
import re

# Create your views here.

def is_valid_name(name):
    # Check if the name contains only letters and spaces
    return re.match("^[a-zA-Z\s]*$", name)

# user register_________________________________________________________________________________________________________________________


@never_cache
def user_register(request):
        if request.user.is_authenticated:
            return redirect(userhome)
        else:
           
           if request.method=='POST':
              username=request.POST['username']
              first_name=request.POST['first_name']
              last_name=request.POST['last_name']
              mail=request.POST['mail']
              password1=request.POST['password1']
              password2=request.POST['password2']
              if password1==password2:
                   if not is_valid_name(first_name) or not is_valid_name(last_name):
                    messages.info(request, "Invalid name. Please use only letters and spaces.")

                    return redirect(user_register)

                   elif User.objects.filter(username=username).exists():
                        messages.info(request,'Username already exists..')
                        return redirect(user_register)
                   elif User.objects.filter(email=mail).exists():
                        messages.info(request,'Mail already exists..')
                        return redirect(user_register)
                   else:
                        user=User.objects.create_user(username=username,first_name=first_name,last_name=last_name,email=mail,password=password1)
                        user.save()
                      
                        messages.info(request,'Registration Successful.')
                        return redirect(user_login)
                        
   
   
              else:
                messages.info(request,'Retype your Password Correctly')
                return redirect(user_register)
              
           else:
             
              return render(request,'reg.html')
   

# ______________________________________________________user login___________________________________________________________________________
@never_cache
def user_login(request):
       if request.user.is_authenticated:
           return redirect(userhome)
       else:
            
        if request.method=='POST':
            username=request.POST['username']
            password=request.POST['password']
            user=authenticate(username=username,password=password)
            if user is not None and not user.is_superuser:
                login(request,user)
                return redirect(userhome)
            else:
                messages.info(request,'Check your Username or Password')
                return redirect(user_login)
        else:
         
           return render(request,'login.html')
   


# ____________________________________________________admin login________________________________________________________________________________
@never_cache
def admin_login(request):
       if request.user.is_authenticated and request.user.is_superuser:
           return redirect(adminhome)
       elif request.user.is_authenticated and not request.user.is_superuser:
           return redirect(userhome)
       else:
           
         if request.method=='POST':
             username=request.POST['username']
             password=request.POST['password']
             user=authenticate(username=username,password=password)
             if user is not None and user.is_superuser:
                 login(request,user)
                 return redirect(adminhome)
             else:
                 messages.info(request,"Check your Username or Password")
                 return redirect(admin_login)
         else:
             return render(request,'admin.html')
   
       


# _________________________________________________________________user home____________________________________________________________________
@never_cache
def userhome(request):   
           
       if request.user.is_authenticated and not request.user.is_superuser:
          return render(request,'user_home_page.html',{'a':request.user})
       elif request.user.is_authenticated and request.user.is_superuser:
           return redirect(adminhome)
        
       else:
          
          return redirect(user_login)
   


# _____________________________________________________________________user log out___________________________________________________________
@never_cache
def userlogout(request):
    if request.user.is_authenticated:
     logout(request)
     return redirect(user_login)


# ______________________________________________________________________________admin home page________________________________________________

@never_cache
def adminhome(request):
          if request.user.is_authenticated and request.user.is_superuser:
              return render(request,'adminhome.html',{'a':request.user})
          else:
              return redirect(admin_login)
          


# _______________________________________________________________admin log out________________________________________________________________
@never_cache
def adminlogout(request):
    # print("hai")
    if request.user.is_authenticated and request.user.is_superuser:
     logout(request)
    #  print("hai")
     return redirect(admin_login)


# __________________________________________________________________user list_____________________________________________________________________
@never_cache
def userlist(request):
        if request.user.is_authenticated and request.user.is_superuser:
              userdata=User.objects.all().filter(is_superuser='False')
              return render(request,'userlist.html',{'useres':userdata})
        else:
              return redirect(admin_login)

# ______________________________________________________________________update page_________________________________________________________________    

def updation(request):
        if request.user.is_authenticated and request.user.is_superuser:
             if request.method=='POST':
               id=request.POST['id']
               upd_user=User.objects.all().filter(id=id)
               return render(request,'update.html',{'upd':upd_user})

             else:
                 return redirect(adminhome)
        else:
              return redirect(userlist)
def do_udpation(request):
    if request.user.is_authenticated and request.user.is_superuser:

       if request.method=='POST':
           id=request.POST['id']
           username=request.POST['username']
           first_name=request.POST['first_name']
           last_name=request.POST['last_name']
           email=request.POST['mail']
           if User.objects.exclude(id=id).filter(username=username).exists():
               messages.info(request,"Updation failed !,Username already taken...")
               return redirect(userlist)
           else:   
             User.objects.filter(id=id).update(username=username,first_name=first_name,last_name=last_name,email=email)
           return redirect(userlist)
       else:
           return redirect(userlist)
       
# __________________________________________________user deletion________________________________________________________________________________
def deletion(request):
    if request.user.is_authenticated and request.user.is_superuser:
      if request.method=='POST':
          id=request.POST['id']
          User.objects.filter(id=id).delete()
          return redirect(userlist)
      else:
          return redirect(adminhome)
      
# ________________________________________________________________________searching____________________________________________________________
def searching(request):
        if request.user.is_authenticated and request.user.is_superuser:
            if request.method=='POST':
                searchid=request.POST['searchid']
                searchdetail=User.objects.all().filter(Q(username__startswith=searchid)  &Q(is_superuser='False'))
                return render(request,'userlist.html',{'useres':searchdetail})
            else:
                return redirect(userlist)
            

# ____________________________________________________________________add user___________________________________________________________________
def adduser(request):
     if request.user.is_authenticated and request.user.is_superuser:
            if request.method=='POST':
                username=request.POST['username']
                first_name=request.POST['first_name']
                last_name=request.POST['last_name']
                email=request.POST['mail']
                password1=request.POST['password1']
                password2=request.POST['password2']
                if password1==password2:
                    if User.objects.filter(username=username).exists():
                         messages.info(request,'Username already exists..!')
                         return redirect(adduser)
                    elif User.objects.filter(email=email).exists():
                         messages.info(request,'Mail already exists...!')
                         return redirect(adduser)
                    else:
                     user=User.objects.create_user(username=username,first_name=first_name,last_name=last_name,email=email,password=password1)
                     user.save()
                     return redirect(userlist)
                     


                else:
                  messages.info(request,'Password does not match')
                  return redirect(adduser)
    
                    
            else:
               return render(request,'adduser.html')
     else:
         return redirect(userhome)
         

