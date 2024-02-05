from django.contrib import admin
from home.models import Feedback, Reservation

class FeedbackAdmin(admin.ModelAdmin):
    # layout for table columns in admin login
    list_display = ('cname', 'cemail', 'cphn')
    # create a search field
    search_fields = ('cname', ) # search based on customer names
    # filter based on a column
    list_filter = ('fbdesc',)

# Register your models here.
    
# ============ displays only the object names ===========
# admin.site.register(Feedback) 
# ============ displays the columns mentioned in the class ============
admin.site.register(Feedback, FeedbackAdmin)

admin.site.register(Reservation)


