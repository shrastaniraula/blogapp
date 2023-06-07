import traceback
from django.shortcuts import redirect, render
from adminWorks.models import Admin
from adminWorks.models import Blog


# Create your views here.
def seeLogin(request):
    return render(request, 'admin/login.html')

def seeAddBlog(request):
    return render(request, 'admin/addBlog.html')




def home(request):
    return render(request, 'admin/adminHome.html')

def doLoginAdmin(request):
    print("This is login page")
    email = request.POST.get("email")
    password = request.POST.get("password")
    print(email)
    print(password)

    teacher_login = Admin.objects.filter(email=email, password= password)

    if teacher_login.exists():
        return render(request, 'admin/adminHome.html')

    else:
        return render(request, 'admin/login.html', {'message': 'Passwords do not match'})
    

def viewBlog(request):
    print("This is from view.....\n")
    blog = Blog.objects.all()
    print(blog)
    return render(request, 'admin/viewBlog.html', {'blog': blog})

def addBlog(request):
    title = request.POST.get("title")
    description = request.POST.get("description")

    Blog_check = Blog.objects.filter(title = title)

    if Blog_check.exists():
        return render(request, 'admin/addBlog.html',{'message': 'This Blog already exists'})

    else:
        try:
            blog = Blog.objects.create(title=title, description= description)
            print("Data sent successfully")
            print(blog)
            return render(request, 'admin/addBlog', {'message': 'Created Successfully'})


        except:
            traceback.print_exc()
            print("Error")
            return render(request, 'admin/addBlog', {'message': 'An error occured'})


def deleteBlog(request):
    id = request.GET.get('id')
    print("This is get method")

    blog = Blog.objects.get(id=id).delete()
    return redirect('/adminWork/viewBlog')