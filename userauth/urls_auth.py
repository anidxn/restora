from django.urls import path
from . import views

urlpatterns = [
    path('signin/', views.signin_user, name='login'),
    path('signup/', views.signup_page),
    path('signout/', views.signout_page),
    path('dash/', views.dashboard_page, name='dashboard'),
    path('changepass/', views.changepwd_page, name='change-pass'),
    path('sendmail/', views.send_demo_email, name='send-mail'),

    path('switchstaff/', views.switch_staff, name='switch-staff'),

    path('approvefbk/', views.approve_feedback, name='approve-feedback'),
    
    # ---------- cuisine category -----------
    path('cuisinine_cat/', views.addcuisinine_category),
    path('allcuisininecats/', views.show_cuisine_cats),
    path('editcsncat/<int:ccid>/', views.update_cuisine_cats, name = "edit-cuisine"),
    path('deletecsncat/<int:ccid>/', views.delete_cuisine_cats, name = "delete-cuisine"),
    # ---------- menu items -----------
    path('addmenu/', views.addmenuitem),
    path('showmenu/', views.showmenuitem, name='show-menu'),
    path('editmenuitems/<int:mid>/', views.updatemenuitem, name = "edit-menuitem"),
    path('deletemenuitems/<int:mid>/', views.deletemenuitem, name = "delete-menuitem"),
    #---------- video ---------
    path('addpvideo/', views.addvideo),                                 # upload a video file
    path('showvideo/', views.showvideogl),                              # show video gallery
    path('deletevideo/<int:vidid>/', views.delete_video, name='delete-video')
]