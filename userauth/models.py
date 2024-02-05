from django.db import models

from . import utilities
from .validators import file_size

#============ Cuisine category ==============
class CuisineCategory(models.Model):
    csn_cat_name = models.CharField('Cuisine category name', max_length = 50)
    csn_cat_desc = models.TextField('Cuisine description', null = True)
    # csn_cat_image= models.ImageField(null = True, blank = True, upload_to = 'images/')  #upload to images folder inside media older
    csn_cat_image= models.ImageField(null = True, blank = True, upload_to = utilities.get_file_path) 
    #upload to images folder inside media older
    
    def __str__(self):
        return self.csn_cat_name
    
#============ Menu item ==============
class MenuItem(models.Model):
    menu_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    desc = models.TextField()
    price = models.FloatField()
    # * * * *  foreign key * * * * * 
    menu_cat = models.ForeignKey(CuisineCategory, on_delete = models.CASCADE, default = 1)
    
    def __str__(self):
        return self.name
    
#======== video gallery ============
class ProdVideo(models.Model):
    caption = models.CharField(max_length = 100)
    vid_file = models.FileField(null=True, blank = True, upload_to="videos/%y", validators=[file_size]) # %y => year
    # file size validation applied
    
    def __str__(self):
        return self.caption
    
