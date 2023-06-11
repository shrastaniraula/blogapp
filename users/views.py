from django.http import HttpResponse
from django.shortcuts import render
import smtplib
from django.core.mail import send_mail
import random
import traceback
from django.shortcuts import redirect, render
from .models import User
from adminWorks.models import Blog
from .models import Likes

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
            OTTP = mail_sender(request, email)
            return render(request, 'users/OTTP.html', {'OTTP': OTTP, 'name': name, 'email': email, 'password': password1})

        except:
            traceback.print_exc()
            print("Error")
            return render(request, 'users/signup.html', {'message': 'An error occured'})

def checkOTTP(request):
    name = request.POST.get("name")
    email = request.POST.get("email")
    password = request.POST.get("password")
    OTTP1 = request.POST.get("OTTP1")
    OTTP2 = request.POST.get("OTTP2")

    print(f"\n\n\n\n\n {OTTP1} \n {OTTP2} \n\n\n\n\n")

    if OTTP1 == OTTP2:
        blog = User.objects.create(name=name, email=email, password= password)
        print("Data sent successfully")
        print(blog)
        return render(request, 'users/login.html', {'message': 'Signup Successful'})
    else:
        return render(request, 'users/signup.html', {'message': 'OTTP doesnt match'})


def doLoginUser(request):
    print("This is login page")
    email = request.POST.get("email")
    password = request.POST.get("password")
    print(email)
    print(password)

    user_login = User.objects.filter(email=email, password= password)

    if user_login.exists():
        for i in user_login:
            userId = i.id
            print(userId)

        request.session['user_id'] = userId
        request.session.save()

        return redirect('/users/visitHome')

    else:
        return render(request, 'users/Login.html', {'message': 'Email or password do not match'})
    
    
def visitHome(request):
    print("This is from view.....\n")
    blog = Blog.objects.all()
    print(blog)
    return render(request, 'users/main.html', {'blog': blog})

def readBlog(request):
    id = request.GET.get('id')
    details = Blog.objects.filter(id=id)
    user_id = request.session['user_id']


    # checking total likes and dislikes and appeding it in the blogs table
    like_count = Likes.objects.filter(liked=True, blogId_id=id).count()
    dislike_count = Likes.objects.filter(disliked=True, blogId_id=id).count()
    details.update(dislikeCount = dislike_count, likeCount= like_count)

    # getting all the details so as to display in the blog page
    show = Blog.objects.get(id=id)

    # checking the liked or disliked situtation of that blog by logged in user to display
    like_dislike = Likes.objects.filter(blogId_id = id, userId_id = user_id)

    # getting the like and disliked of that specific blog id and user
    if like_dislike.exists():
        for i in like_dislike:
            like_situation = i.liked
            dislike_situation = i.disliked
        return render(request, 'users/blog.html', {'details': show, 'like_situation': like_situation, 'dislike_situation': dislike_situation})
    
    return render(request, 'users/blog.html', {'details': show})

def addView(request):
    id = request.GET.get('id')
    object = Blog.objects.filter(id=id)
    for i in object:
        views= i.viewCount
    
    newview = int(views)+1
    object.update(viewCount=newview)

    return render(request, status=200)


def mail_sender(request, email):
    # server = smtplib.SMTP('smtp.gmail.com', 587)
    print("THis is email clss")

    receiver_add = [email]  # storing the receiver's mail id
    sender_add = 'shrastaniraula@gmail.com'  # storing the sender's mail id
    password = 'your_password_here'  # got app and send email

    # storing the password to log in
    # creating the SMTP server object by giving SMPT server address and port number
    smtp_server = smtplib.SMTP("smtp.gmail.com", 587)
    print("smpt connection")

    smtp_server.ehlo()  # setting the ESMTP protocol
    smtp_server.starttls()  # setting up to TLS connection
    smtp_server.ehlo()  # calling the ehlo() again as encryption happens on calling startttls()
    print("HELO")

    newStr = ""
    try:

        for i in range(0, 6):
            ran_number = random.randint(0, 9)
            newStr = newStr + str(ran_number)

        smtp_server.login(sender_add, password)  # logging into out email id
        msg_to_be_sent = f"""
        HI, Thanks joining our system. We are glad to welcome you to our family. However you need to enter verification code to continue.
        Your Verification code is {newStr}
        """
        send_mail('Hello Hi', msg_to_be_sent, sender_add, receiver_add)
    # subject,
    # message,
    # from_email,
    # recipient_list,

    except Exception as e:
        traceback.print_exc()
        # piting a message on sending the mail
    
    print('Successfully the mail is sent')

    smtp_server.quit()  # terminating the server
    return newStr

def liked(request):
    situation = request.GET.get('situation')
    blogid = request.GET.get('id')
    user = request.session['user_id']

    print("This is user like or dislike of ")

    liked = False
    disliked = False
    neutral = False


    object = Likes.objects.filter(blogId_id=blogid, userId_id=user)

    if object.exists():
        if (situation == "liked"):
            object.update(liked=True, disliked=False, neutral=False)
            print(situation)

        elif (situation == "disliked"):
            object.update(liked=False, disliked=True, neutral=False)
            print(situation)

        elif (situation == "neutral"):
            object.update(liked=False, disliked=False, neutral=True)
            print(situation)
    else:
        if (situation == "liked"):
            Likes.objects.create(blogId_id=blogid, userId_id=user, liked=True)
            object.update(liked=True, disliked=False, neutral=False)
            print(situation)

        elif (situation == "disliked"):
            Likes.objects.create(
                blogId_id=blogid, userId_id=user, disliked=True)

            print(situation)
        elif (situation == "neutral"):
            Likes.objects.create(blogId_id=blogid, userId_id=user, neutral=True)
            print(situation)

    print(f"\n\n\n{user}\n\n\n")

    # return redirect('http://127.0.0.1:8000/users/readBlog?id=1')
