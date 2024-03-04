import os
from django.shortcuts import redirect, render
from django.http import HttpResponse, HttpRequest
# ----- for ilike with OR in query------
from django.db.models import Q
from userauth.utilities import *

#----- for messages framework -------
from django.contrib import messages

#------ import the models------------
from home.models import Feedback, Reservation
from userauth.models import CuisineCategory, MenuItem

#--------- additional for getting current date-time-----------------
from datetime import datetime

# -------import for pdf file generation ---------
import io
from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter

# -------import for csv file generation ---------
import csv

#---------- to be used with aggregate & group by ------------
from django.db.models import Count

#-----------------------------------
#   Create your views here.
#-----------------------------------
def say_hello(request):
    return HttpResponse('Hello there')

def index_page(request):
    # >> Phase - i
    # return render(request, 'index.html')

    # >> Phase - ii (after addition of product category)
    cuisines = CuisineCategory.objects.all()
    result = MenuItem.objects.values('menu_cat').annotate(group_count=Count('menu_id'))     # SQL: select count(menu_id) as group_count from MenuItem group by menu_cat
    # print('Count result: ', result)    <QuerySet [{'menu_cat': 1, 'group_count': 1}, {'menu_cat': 2, 'group_count': 1}, {'menu_cat': 3, 'group_count': 3}, {'menu_cat': 4, 'group_count': 2}]>
    
    # store result in dictionary 
    item_count = {}     # item_count = {"1": 1, "2" :1 , "3" : 3, "4": 2}
    for entry in result:
        item_count[str(entry['menu_cat'])] = entry['group_count']

    # print("Item count dictionary : " , item_count)
    
    return render(request, 'index.html', {'cuisines' : cuisines, 'itm_qnty' : item_count})

#-----------------------------------------
#           Create a feedback
#-----------------------------------------
def feedback_page(request):
    if request.method == "POST":
        name = request.POST.get('txtName')
        phone = request.POST.get('txtPhone')
        email = request.POST.get('txtEmail')
        msg = request.POST.get('txtDesc')
        star_rating = request.POST.get('rating')
        #---- create an instance of the model -----
        fbobj = Feedback(cname = name, cemail = email, cphn = phone, fbdesc = msg, rating = star_rating, fbdate = datetime.today())

        #---- save the model -----
        fbobj.save()  # saves the resord in db

        #---- adding a message for the messages framework to respond -----
        """
        DEBUG 	    debug
        INFO 	    info
        SUCCESS 	success
        WARNING 	warning
        ERROR 	    error
        """
        # messages.add_message(request, messages.INFO, "Your order is received.") ---- OR ----
        messages.success(request, "Your feedback is submitted.")

    # return HttpResponse('Contact details')
    return render(request, 'feedbacks/feedback.html') # render the page in all situation



#-----------------------------------------
#           Show all feedback 
#-----------------------------------------
def allfeedback(request):
    #------ get all the records from db using ORM -------
    #allfb = Feedback.objects.all()  # list of objects
    allfb = Feedback.objects.filter(approved = True)  # list of objects

    # ----- embed the records as context & send to page --------
    ctxt = {"fblist" : allfb}
    return render(request, 'feedbacks/showfeedbacks.html', ctxt)

#-----------------------------------------
#           edit an feedback 
#-----------------------------------------
def edit_feedback(request, fbkid):
    selected_fb = Feedback.objects.get(fbid=fbkid)  # get single object ..this object is used for both viewing purpose & editing purpo
    # * * * If we had not set a PKey manually then to invoke the default pimary key we need to write get(pk = ordid)

    if request.method == "POST":
        name = request.POST['txtName'] # .get('txtName')
        phone = request.POST['txtPhone'] #.get('txtPhone')
        email = request.POST['txtEmail'] #.get('txtEmail')
        msg = request.POST['txtDesc'] #.get('txtOrder')
        star_rating = request.POST.get('rating')

        #---- Update the selected instance -----
        selected_fb.cname = name
        selected_fb.cemail = email
        selected_fb.cphn = phone
        selected_fb.fbdesc = msg
        selected_fb.rating = star_rating
        selected_fb.fbdate = datetime.today()

        #---- save the model -----
        selected_fb.save()  # saves the resord in db
        messages.info(request, "Your feedback is updated.")
        return redirect('/restroapp/allfeedback')

    
    ctxt = {"selfb" : selected_fb}
    return render(request, 'feedbacks/editfeedback.html', ctxt)

#-----------------------------------------
#           Delete an feedback 
#-----------------------------------------
def delete_feedback(request, fbkid):
    selected_fb = Feedback.objects.get(fbid = fbkid)  # get single object 
    selected_fb.delete()
    messages.warning(request, "Your feedback is deleted.")
    return redirect('/allfeedback/allfeedback')

def search_food(request):
    if request.method == "POST":
        #------ filter records from db using ORM -------
        searched_food = request.POST['txtSearch']
        
        # food_list = MenuItem.objects.filter(name__icontains=searched_food)  # list of objects
        food_list = MenuItem.objects.filter(Q(name__icontains=searched_food) | Q(desc__icontains = searched_food))      # * * Query with OR operator * *

        # ----- embed the records as context & send to page --------
        return render(request, 'menuitem/searchedfood.html', {'searched': searched_food, 'foods' : food_list})
    # else:
    #     messages.warning(request, 'Please search with a valid keyword !!')
    #     return render(request, 'index.html')

#-----------------------------------------------------------------------------
#        Display list of menu items based an Cuisine category selected
#-----------------------------------------------------------------------------
def menu_by_cat(request, ccid):
    try:
        # get the cuisine category details for header image & name to be displayed
        csn_catg = CuisineCategory.objects.get(id = ccid)
        
        # menu_list = MenuItem.objects.filter(menu_cat = ccid)  --> It works
        # or
        menu_list = csn_catg.menuitem_set.all()  # works bcz of FKey relation
        
        return render(request, 'menubycat.html', {'menulist': menu_list, 'cuisine' : csn_catg}) # , 'sel_category' : catname
    except:
        messages.warning(request, 'That category does not exist.')
        return redirect('home')

#-----------------------------------------------------------------------------
#           Make a reservation
#-----------------------------------------------------------------------------
def reservation_page(request):
    if request.method == "POST":
        name = request.POST['txtName']
        phone = request.POST['txtPhone']
        email = request.POST['txtEmail']
        msg = request.POST['txtMessage']
        rvdate = request.POST['txtDate']
        rvTime = request.POST['txtTime']
        pplcnt = request.POST['txtPplCount']

        #---- create an instance of the model -----
        rvObj = Reservation(cname = name, cemail = email, cphn = phone, rv_date = rvdate, rv_time = rvTime, ppl_count = pplcnt, msg = msg)

        # store user id for logged in users
        if request.user.is_authenticated:
            rvObj.uid = request.user.id 

        #---- save the model -----
        rvObj.save()  # saves the resord in db

        # messages.add_message(request, messages.INFO, "Your order is received.") ---- OR ----
        messages.success(request, "Your booking request has been accepted. We have sent a confirmation email.")
        # ++++++ Confirmation email +++++++++
        # ======================================
        subject = "Booking at Newton's Apple"
        message = '''Hello %s , Your booking at our place is confirmed. We will be expecting you on %s at %s .
        \n Thank you for your interest,
        \n Regards,
        \n - Team RestroApp''' % (name, rvdate, rvTime)
        send_custom_email(subject, message, email)

    # return HttpResponse('Contact details')
    return render(request, 'bookings/reservation.html') # render the page in all situation

# ------------ all bookings ------------
def allreservations(request):
    if request.user.is_authenticated:
        booking_list = None
        if request.user.is_staff:  # show all for super user
            booking_list = Reservation.objects.all()
        else:
            booking_list = Reservation.objects.filter(uid = request.user.id) # only for the specific user

        return render(request, 'bookings/allbookings.html', {'booking_list' : booking_list})
    else:
        return redirect('dashboard')

# ----edit a booking ----------------    
def edit_booking(request, rvid):
    selected_rv = Reservation.objects.get(rv_id=rvid)  # get single object ..this object is used for both viewing purpose & editing purpo
    # * * * If we had not set a PKey manually then to invoke the default pimary key we need to write get(pk = ordid)

    if selected_rv.uid != request.user.id and request.user.is_staff != True:
        messages.warning(request, messages.warning(request, "You are not allowed to edit this booking. You can edit bookings that you have made"))
        return redirect('allbookings')

    # -------- if user validation passes ----
    if request.method == "POST":
        name = request.POST['txtName']
        phone = request.POST['txtPhone']
        email = request.POST['txtEmail']
        msg = request.POST['txtMessage']
        rvdate = request.POST['txtDate']
        rvTime = request.POST['txtTime']
        pplcnt = request.POST['txtPplCount']

        #---- Update the selected instance -----
        selected_rv.cname = name
        selected_rv.cemail = email
        selected_rv.cphn = phone
        selected_rv.rv_date = rvdate
        selected_rv.rv_time = rvTime
        selected_rv.ppl_count = pplcnt
        selected_rv.msg = msg
        # Don't change the UID ***

        #---- save the model -----
        selected_rv.save()  # saves the resord in db
        messages.info(request, "The booking is updated.")
        return redirect('/restroapp/allbookings')

    ctxt = {"selrv" : selected_rv}
    return render(request, 'bookings/editbooking.html', ctxt)

# ----- delete a booking -------------
def delete_booking(request, rvid):
    logged_user = request.user
    selected_rv = Reservation.objects.get(rv_id = rvid)  # get single object 

    # * * * only a logged user can delete his bookings or staff can delete any booking
    # prevents deletetion of booking by url hit /restroapp/delbooking/3/  >> changing the booking id to random id in browser URL
    if selected_rv.uid == logged_user.id or logged_user.is_staff:
        selected_rv.delete()
        messages.warning(request, "Your booking is cancelled.")
    else:
        messages.warning(request, "You are not allowed to delete this booking. You can delete bookings that you have made")
    return redirect('allbookings')




#----------------------------------------------------------
#    Generate pdf with list of orders using ReportLab
#   https://www.reportlab.com/docs/reportlab-userguide.pdf
#----------------------------------------------------------
def booking_pdffile(request):
    # create a ByteStream buffer
    buff = io.BytesIO()
    # Create a canvas
    can = canvas.Canvas(buff, pagesize=letter, bottomup = 0) # Letter size page
    # create a text object
    txtObj = can.beginText()
    txtObj.setTextOrigin(inch, inch)
    txtObj.setFont("Helvetica", 14)

    # add some lines of text
    """
    txtlines = [
        "This is line 1", 
        "This is line 2", 
        "This is line 3", 
        "This is line 4", 
    ] """
    txtlines = []

    # orderlist = Orders.objects.all()
    if request.user.is_staff:  # show all for staff user
        booking_list = Reservation.objects.all()
    else:
        booking_list = Reservation.objects.filter(uid = request.user.id) # only for the specific user

    for rv in booking_list:
        # txtlines.append(rv.cname)
        # txtlines.append(rv.cemail)
        # txtlines.append(rv.cphn)
        # txtlines.append(str(rv.rv_date))
        # txtlines.append(str(rv.rv_time))
        # txtlines.append(str(rv.ppl_count))
        # txtlines.append(rv.msg)

        txtlines.append(rv.cname  + ' | ' + rv.cemail  + ' | ' + rv.cphn  + ' | ' + str(rv.rv_date)  + ' at ' + str(rv.rv_time)  + ' | ' + str(rv.ppl_count) + ' | ' + rv.msg)
        txtlines.append("=======================================================================================================================================================")

    # Loop
    for line in txtlines:
        txtObj.textLine(line)

    # finish up
    can.drawText(txtObj)
    can.showPage()
    can.save()
    buff.seek(0)

    # return response
    return FileResponse(buff, as_attachment=True, filename='orders.pdf') 
                    # utilities.get_file_path(filename='orders.pdf')

#----------------------------------------------------------
#    Generate csv with list of orders
#----------------------------------------------------------
def booking_csvfile(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=orders.csv'

    # create a CSV writer
    writer = csv.writer(response)

    if request.user.is_staff:  # show all for staff user
        booking_list = Reservation.objects.all()
    else:
        booking_list = Reservation.objects.filter(uid = request.user.id) # only for the specific user

    # Add column headings to the csv
    writer.writerow(['Customer name', 'e-mail ', 'Phone #', 'Booking Date', 'Booking time', '# of people', 'Message'])  # pass a list of column values

    # write all records
    for rv in booking_list:
        writer.writerow([rv.cname, rv.cemail, rv.cphn, rv.rv_date, rv.rv_time, rv.ppl_count, rv.msg])

    return response

#----------------------------------------------------------
#    Generate text file with list of orders
#----------------------------------------------------------
def booking_txtfile(request):
    response = HttpResponse(content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename=orders.txt'

    txtlines = []

    if request.user.is_staff:  # show all for staff user
        booking_list = Reservation.objects.all()
    else:
        booking_list = Reservation.objects.filter(uid = request.user.id) # only for the specific user

    for rv in booking_list:
        txtlines.append(f'{rv.cname} | {rv.cemail} | {rv.cphn} | {rv.rv_date} | {rv.rv_time} | {rv.ppl_count} | {rv.msg}\n')

    response.writelines(txtlines)
    return response


