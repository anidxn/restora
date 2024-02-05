from django.urls import path
from . import views

urlpatterns = [
    path('hello/', views.say_hello),                                    # just a text response
    path('', views.index_page, name='home'),                            # index page without url
    path('home/', views.index_page, name='home'),                       # index page with home url

    path('booking/', views.reservation_page, name='reserve'),
    path('allbookings/', views.allreservations, name='allbookings'),
    path('editbooking/<int:rvid>/', views.edit_booking, name = "edit-booking"),
    path('delbooking/<int:rvid>/', views.delete_booking, name = "delete-booking"),

    path('feedback/', views.feedback_page),
    path('allfeedback/', views.allfeedback, name = "all-feedbacks"),
    #------- Internal path ----------
    path('editfb/<int:fbkid>/', views.edit_feedback, name = "edit-feedback"),
    path('deletefb/<int:fbkid>/', views.delete_feedback, name = "delete-feedback"),

    path('searchfood/', views.search_food, name = 'search-food'),       # search from the nav bar
    path('bookingpdf/', views.booking_pdffile, name='booking-pdf'),               # generate pdf
    path('bookingcsv/', views.booking_csvfile, name='booking-csv'),               # generate csv
    path('bookingtxt/', views.booking_txtfile, name='booking-txt'),               # generate csv
    
    path('menubycat/<int:ccid>/', views.menu_by_cat, name='menubycat')

]
