from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from .models import User, UserManager
from ..schedules.models import Schedule, Day
from ..user_profile.models import Images, Profile

def index(request):
    # request.session.clear()
    # admin = User.objects.filter(email = 'ADMIN')
    # if not admin:
    #     adminUser = User.objects.create(userLevel = True, firstname = 'ADMIN', lastname = 'ADMIN', email = 'ADMIN', password = 'NishJakePris')
    #     Profile.objects.create(user = adminUser, birthday = '1992-08-01', occupation = 'ADMIN', company = 'ADMIN', street_number = '9503', route = 'Peniwill Drive', city = 'Lorton', state = 'VA', postal_code='22079', latitude = 38.7043715, longtitude = -77.2732501,
    #      about_me="ADMIN", distAway = 500)
    if not 'active_user_id' in request.session:
        return render(request, 'login_register/index.html')
    else:
        return redirect(reverse('main:index'))

def logout(request):
    del request.session['active_user_id']
    return redirect(reverse('login_register:index'))

def login(request):
    # if request.POST['email'] == 'ADMIN' and request.POST['password'] == 'NishJakePris':
    #     chk_email = request.POST['email']
    #     chk_password = request.POST['password']
    #     user_active = User.objects.get(email = chk_email)
    #     request.session['active_user_id'] = user_active.id
    #     Profile.objects.create(user = user_active, birthday = '1992-08-01', occupation = 'ADMIN', company = 'ADMIN', street_number = '9503', route = 'Peniwill Drive', city = 'Lorton', state = 'VA', postal_code='22079', latitude = 38.7043715, longtitude = -77.2732501,
    #      about_me="ADMIN", distAway = 500)
    #     return redirect(reverse('main:index'))
    if not 'active_user_id' in request.session:
        if request.method == "POST":
            chk_email = request.POST['email']
            chk_password = request.POST['password']

            if User.objects.filter(email = chk_email).exists():
                user_active = User.objects.get(email = chk_email)
                passwordMatch = User.objects.check_password_match(chk_password, user_active.password)
                if passwordMatch:
                    request.session['active_user_id'] = user_active.id
                    return redirect(reverse('main:index'))
                else:
                    messages.error(request,'Incorrect password')
            else:
                messages.error(request,'Email does not exist. Sign up?')

        return redirect(reverse('login_register:index'))
    else:
        return redirect(reverse('main:index'))

def register(request):
    if not 'active_user_id' in request.session:
        if request.method == "POST":
            firstname = request.POST['firstname']
            lastname = request.POST['lastname']
            email = request.POST['email']
            password = request.POST['password']
            cpassword = request.POST['cpassword']

            if email == 'nish8192@gmail.com' or email == 'hermanj13@me.com' or email == 'pmannuel@hotmail.com':
                userLevel = True
            else:
                userLevel = False

            error_messages = User.objects.register(firstname, lastname, email, password, cpassword)
            if error_messages == []:
                diffpassword = User.objects.encrypt(password)
                User.objects.create(
                    firstname = firstname,
                    lastname = lastname,
                    email = email,
                    password = diffpassword,
                    userLevel = userLevel
                )
                user_active = User.objects.get(email = email)
                request.session['active_user_id'] = user_active.id
                mon = Day.objects.create()
                tue = Day.objects.create()
                wed = Day.objects.create()
                thu = Day.objects.create()
                fri = Day.objects.create()
                sat = Day.objects.create()
                sun = Day.objects.create()
                schedule = Schedule.objects.create(user = user_active, mon = mon, tue = tue, wed = wed, thu = thu, fri = fri, sat = sat, sun = sun)

                default_avatar = Images.objects.create(user_id = request.session['active_user_id'])

                return redirect(reverse('main:index'))
            else:
                for i in range(0, len(error_messages)):
                    messages.error(request, error_messages[i])
        return redirect(reverse('login_register:index'))
    else:
        return redirect(reverse('main:index'))
