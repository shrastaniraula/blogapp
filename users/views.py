import traceback
from django.shortcuts import redirect, render
from .models import User
from adminWorks.models import Blog

# Create your views here.

def seeLogin(request):
    return render(request, 'users/login.html')

def seeSignup(request):
    return render(request, 'users/signup.html')

def signupUser(request):
    name = request.POST.get("name")
    email = request.POST.get("email")
    password1 = request.POST.get("password1")
    password2 = request.POST.get("password2")


    User_check = User.objects.filter(email = email)

    if password1 !=password2:
        return render (request, 'users/signup.html', {'message': 'Password doesnt match confirm password.'})

    if User_check.exists():
        return render(request, 'users/signup.html',{'message': 'This User already exists, login instead?'})

    else:
        try:
            blog = User.objects.create(name=name, email=email, password= password1)
            print("Data sent successfully")
            print(blog)
            return render(request, 'users/login.html', {'message': 'Signup Successful'})


        except:
            traceback.print_exc()
            print("Error")
            return render(request, 'users/signup.html', {'message': 'An error occured'})


def doLoginUser(request):
    print("This is login page")
    email = request.POST.get("email")
    password = request.POST.get("password")
    print(email)
    print(password)

    user_login = User.objects.filter(email=email, password= password)

    if user_login.exists():
        print("Insideee iffffff")
        return redirect('/users/visitHome')

    else:
        print("Insideee elsseeeee")
        return render(request, 'users/Login.html', {'message': 'Email or password do not match'})
    
    
def visitHome(request):
    print("This is from view.....\n")
    blog = Blog.objects.all()
    print(blog)
    return render(request, 'users/main.html', {'blog': blog})

def readBlog():
    return render("users/main.html")

