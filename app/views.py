from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from django.contrib import messages
from .models import PlaceImage
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    place_images = PlaceImage.objects.all()
    if request.method == 'POST':
        placename = request.POST.get('placename')
        comment = request.POST.get('comment')

        if placename == comment:
            condition_result = True
        else:
            condition_result = False

        return render(request, 'index.html', {'place_images': place_images,'condition_result': condition_result})
    return render(request, 'index.html', {'place_images': place_images})



def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            # User is authenticated, log them in
            auth.login(request, user)
            return redirect('/')
        else:
            # Authentication failed, handle it appropriately
            return render(request, 'login.html', {'error': 'Invalid credentials'})

    return render(request, 'login.html')


def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        email = request.POST['email']

        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request,'name Taken')
                return redirect('login')
            elif User.objects.filter(email=email).exists():
               messages.info(request,'Email Taken')
               return redirect('login')
            else:
               user = User.objects.create_user(username=username, password=password1, email=email)
               user.save();
                             
               print('user created')
               return redirect('login')
        else:
           messages.info(request, 'password not matching')
           return redirect('index')

    return render(request,'signup.html')


def logout(request):
    auth.logout(request)
    return redirect('signup')

@login_required
def uploadImage(request):
    print("sgnbdsbjvjsdvcugshv")
    if request.method == 'POST':
        image = request.FILES.get('image')
        place = request.POST.get('place')

        # Ensure that an image is provided before proceeding
        if image:
            # Create a new PlaceImage instance and associate it with the logged-in user
            placeImage = PlaceImage(user=request.user, image=image, location_name=place)
            placeImage.save()
            return redirect('index')  # Replace 'index' with the actual URL or name of your index page

    return render(request, 'index.html')  # Replace 'index.html' with the actual template name