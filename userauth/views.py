import os
from django.shortcuts import redirect, render
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect, JsonResponse
#---- for BUILT-IN user Model --------------
from django.contrib.auth.models import User

# ------ for authentication of using existing auth_user model -----
from django.contrib.auth import authenticate, login, logout
# to keep the user in session after password change
from django.contrib.auth import update_session_auth_hash

#----- for messages framework -------
from django.contrib import messages


# ---- for custom  forms ------
from . import forms

from . import utilities
from .models import CuisineCategory, ProdVideo, MenuItem

from home.models import Feedback

#===========================================
#           signin page
#===========================================
def signin_user(request):
    if request.method == "POST":
        uname = request.POST['txtUName']
        passwd = request.POST['txtPass']
        print(uname, ' == ', passwd )


        # authenticate with built in function authenticate() from django.contrib.auth
        myuser = authenticate(username = uname, password = passwd) # model / table has columns named username & password

        if myuser is not None: # credentials found
            # login with built in function login() from django.contrib.auth
            login(request, myuser)

            # ename = myuser.first_name + ' ' + myuser.last_name
            # return render(request, 'dashboard.html', {'emp_name': ename})
            return redirect('/restroapp/dash') # url for dashboard
        else:
            messages.warning(request, "Bad credentials")
            return redirect('login')

    return render(request, 'signin.html')

#===========================================
#           SIGN UP page
#===========================================
def signup_page(request):
    if request.method == "POST":
        
        uname = request.POST['txtUName'] 
        fname = request.POST['txtFName']
        lname = request.POST['txtLName']
        uemail = request.POST['txtEmail']
        passwd = request.POST['txtPass']
        confpass = request.POST['txtConfPass']

        #============= server-side validation ==============

        # user validation - fetch record from auth_user table & filter based on username column
        if User.objects.filter(username = uname):
            messages.warning(request, "Username already exists !! please try some other username")
            return redirect('/restroapp/signin')
        
        if len(uname) < 3:
            messages.error(request, "Username must be atleast 3 characters")
            return redirect('/restroapp/signin')
        
        if not uname.isalnum():
            messages.error(request, "Username must alpha-numeric")
            return redirect('/restroapp/signin')

        # email validation
        if User.objects.filter(email = uemail):
            messages.error(request, "Email already registered")
            return redirect('/restroapp/signin')
        
        if passwd != confpass :
            messages.error(request, "Password and confirm password did not match!!")
            return redirect('/restroapp/signin')
        
        #============= End server-side validation ==============

        #---- create an instance of the BUILT -IN USER Model (checkout auth_user table in db-browser)-----
        myuser = User.objects.create_user(uname, uemail, passwd)
        myuser.first_name = fname  # first_name is present in auth_user table
        myuser.last_name = lname
        # myuser.is_active = False  # don't activate now, activate when the user clicks on activation link

        myuser.save() # save in db

        messages.success(request, "User registered successfully.")

        # ++++++ welcome email +++++++++
        # ======================================
        # subject = "Welcome to RestroApp !!"
        # message = '''Hello ' + myuser.first_name + ', Thank you for registering in our application.
        # \n This is a verification mail.
        # \n Thank you,
        # \n P.D.'''
        # myutils.send_custom_email(subject, message, myuser.email)

        # redirect to login page
        return redirect('/restroapp/signin')  # * * * * * * /restroapp/ is required ...

    return render(request, 'signup.html')

#===========================================
#           DASHBOARD page 
# for staff user open admin panel
# for non-staff user open bookings page
#===========================================
def dashboard_page(request):
    
    if request.user.is_authenticated:
        if request.user.is_staff:
            ctx = {} # empty dictionary

            allfbk = Feedback.objects.all()
            ctx['allfbk']  = allfbk

            # admin can see all users
            if request.user.is_superuser:
                allusers = User.objects.all()
                ctx['allusers'] = allusers

            return render(request, 'dashboard.html', ctx)
        else:   
            return redirect('/restroapp/allbookings')
    else:
        messages.error(request, "You must login to access this page.")
    
        # redirect to login page
        return redirect('/restroapp/signin')
    
    #return render(request, 'dashboard.html')
   
#===========================================
#           SIGNOUT page
#===========================================
def signout_page(request):
    logout(request)
    messages.info(request, "logout successfull.")
    return redirect('/restroapp/signin')

#===========================================
#           CHANGE PASSWORD page
#===========================================
def changepwd_page(request):

    if request.user.is_authenticated:
        if request.method == "POST": 
        # checks for existing user login, so it will change password for that user
            opasswd = request.POST['txtOPass']
            passwd = request.POST['txtPass']
            confpass = request.POST['txtConfPass']

            uname = request.user.username   # get existing username

            #print('username ',uname, 'password', opasswd, ' new =', passwd)
            #u = User.objects.get(username = uname)   # get db user object based on username
            u = authenticate(username = uname, password = opasswd)  # get db user object based on username & password
            
            if u is not None:
                u.set_password(passwd)
                u.save()
                # * * * * * * update the session after changing password so that the user isn't logged off. * * * * * 
                update_session_auth_hash(request, u)
                messages.success(request, "Password changed successfully.")
            else:
                messages.error(request, "Please enter correct old password.")
            return redirect('/restroapp/dash')
         
        # load page   
        return render(request, 'changepwd.html')
    else:
        messages.error(request, "You must login to access this page.")

        # redirect to login page
        return redirect('/restroapp/signin')
    
#===========================================
#           SWITCH STAFF STATUS
#===========================================   
def switch_staff(request):
    if request.method == "POST":
        uid  = int(request.POST['user_id'])

        userObj = User.objects.get(id = uid)
        userObj.is_staff = not userObj.is_staff # flip

        userObj.save()
        
        response = JsonResponse({'status' : 1})
        return response
    
#===========================================
#           SEND MAIL page
#===========================================
def send_demo_email(request):
    utilities.send_demo_email_to_client()
    return redirect('/restroapp/dash')

#========================================
# APPROVE Feedback with AJAX
#========================================
def approve_feedback(request):
    if request.method == "POST":
        fbkid  = int(request.POST['feedback_id'])

        fbObj = Feedback.objects.get(fbid = fbkid)
        fbObj.approved = not fbObj.approved # flip

        fbObj.save()
        
        response = JsonResponse({'status' : 1})
        return response
    # else:
    #     response = JsonResponse({'status' : 0})
    
    


#==================================================================
#       CUISINE operation from employee dashboard
#==================================================================
def addcuisinine_category(request):
    save_status = False # conventional way of setting status
    if request.method == "POST":
        # myform = forms.CuisineForm(request.POST, request.FILES)
        myform = forms.CuisineCategoryForm(data = request.POST, files = request.FILES)
        if myform.is_valid():
            myform.save()
            # messages.success(request, 'Cuisine category added successfully')
            #return redirect('addmenuitems.html')
            return HttpResponseRedirect('/restroapp/cuisinine_cat?save_status=True') # passed on as a Get param
    else:
        myform = forms.CuisineCategoryForm()
        if 'save_status' in request.GET:   # check if there is a GET param with this name
            save_status = True
        
        return render(request, 'cuisines/addcuisinecat.html', {'mform': myform, 'save_status' : save_status})
    

# ----------- show cuisine categories -----------
def show_cuisine_cats(request):
    allcsncats = CuisineCategory.objects.all().order_by('csn_cat_name')  # ORDER BY food name

    # ----- embed the records as context & send to page --------
    ctxt = {"cuisine_list" : allcsncats}
    return render(request, 'cuisines/showcuisinecats.html', ctxt)


# ----------- update a cuisine cat ------------
def update_cuisine_cats(request, ccid):
    try:
        selected_cuisine = CuisineCategory.objects.get(id=ccid)
        # myform = forms.CuisineForm(request.POST or None)  # ********Creates an EMPTY form => 2-step function call ->
        # --> >>> if submitted then get post data & initialize the object with that dat otherwise initialize a blank object

        myform = forms.CuisineCategoryForm(request.POST or None, request.FILES or None, instance=selected_cuisine)  # instance : Populate the form with the selected object details
        # if request.method == "POST":
        if myform.is_valid():
            myform.save()  # save record with updated value
            messages.success(request, 'Cuisine category updated succcessfully')
            return redirect('/restroapp/allcuisininecats')
            # dont delet the image file yet

        return render(request, 'cuisines/editcuisinecat.html', {'mform': myform})
    
    except Exception as e:
        messages.warning(request,'Cuisine category not found')
        #print(e)
        return redirect('/restroapp/allcuisininecats')

# ----------- delete cuisine cat ----------

def delete_cuisine_cats(request, ccid):
    selected_cuisine = CuisineCategory.objects.get(id=ccid)

    if selected_cuisine.csn_cat_image:      #is not None and len(selected_food.fd_image) > 0
        os.remove(selected_cuisine.csn_cat_image.path)

    selected_cuisine.delete()
    messages.success(request, "Cuisine category deleted successfully")
    return redirect('/restroapp/allcuisininecats')


#==================================================================
#      video related operation from employee dashboard
#==================================================================

def addvideo(request):
    myform = forms.ProductVideoForm(request.POST or None, request.FILES or None)  # instance : Populate the form with the selected object details
    if myform.is_valid():
            myform.save()  # save record with updated value
            messages.success(request, 'Cuisine category updated succcessfully')
                        
    return render(request, 'videogallery/addvideos.html', {'mform': myform})

#-------------- show -----------------
def showvideogl(request):
    vid_list = ProdVideo.objects.all()
    return render(request, 'videogallery/showvideos.html', {'vidlist': vid_list})

# -------------- delete ---------------
def delete_video(request, vidid):
    selected_vid = ProdVideo.objects.get(id=vidid)

    if selected_vid.vid_file:      #is not None and len(selected_food.fd_image) > 0
        os.remove(selected_vid.vid_file.path)

    selected_vid.delete()
    messages.success(request, "Product video deleted successfully")
    return redirect('/restroapp/showvideo')

#==================================================================
#               Menu item related operation 
#==================================================================
def addmenuitem(request):
    save_status = False # conventional way of setting status
    if request.method == "POST":
        myform = forms.MenuItemForm(data = request.POST)
        if myform.is_valid():
            myform.save()
            messages.success(request, 'Menu item added successfully')
            
    myform = forms.MenuItemForm()    
    return render(request, 'menuitem/addmenu.html', {'mform': myform})


# ----------show menu items------------
def showmenuitem(request):
    allmenus = MenuItem.objects.all()  # ORDER BY food name

    ctxt = {"menu_list" : allmenus}
    return render(request, 'menuitem/showmenu.html', ctxt)

#--------update ----------
def updatemenuitem(request, mid):
    try:
        selected_menu = MenuItem.objects.get(menu_id=mid)

        myform = forms.MenuItemForm(request.POST or None, instance = selected_menu)  # instance : Populate the form with the selected object details
        if myform.is_valid():
            myform.save()
            messages.info(request, 'Menu item updated successfully ')
            return redirect('/restroapp/showmenu')

        return render(request, 'menuitem/editmenu.html', {'mform': myform})
    except Exception as e:
        messages.warning(request,'Menu item not found')
        #print(e)
        return redirect('show-menu')

#--- delete a menu item -----
def deletemenuitem(request, mid):
    selected_menu = MenuItem.objects.get(menu_id=mid)

    selected_menu.delete()
    messages.success(request, "Menu item deleted successfully")
    return redirect('/restroapp/showmenu')