from django import forms
from django.forms import ModelForm  # forms created by Models
from . models import CuisineCategory, ProdVideo,MenuItem

# Create a Add new Cuisine form
class CuisineCategoryForm(ModelForm):
    class Meta:  # Meta class will connect the form to the model************
        model = CuisineCategory  # set the model to the cuisine category model
        # fields = "__all__"  # we want all the fields of the models
        fields = ('csn_cat_name', 'csn_cat_desc', 'csn_cat_image')

        # OPTIONAL => custom labels for form fields
        labels = {
            'csn_cat_name' : 'Cuisine category Name',
            'csn_cat_desc' : 'Few details about it',
            'csn_cat_image' : 'Upload an image'
        }

        # OPTIONAL => 
        # widgets are required to decorate using bootstrap
        # https://docs.djangoproject.com/en/5.0/ref/forms/widgets/
        
        widgets = {
            'csn_cat_name' : forms.TextInput(attrs={'class': 'form-control', 'placeholder' : 'Category name'}),  # form-control is  bootstrap class 
            'csn_cat_desc' : forms.Textarea(attrs={'class': 'form-control', 'placeholder' : 'Details of ingredients'}),
        }

        """
        forms.EmailInput --> for email
        forms.Select() 'class': form-select'--> dropdown
        """



#========= create a add new video form ===========
class ProductVideoForm(ModelForm):
    class Meta:  
        model = ProdVideo
        fields = "__all__" 

#========= Menu item form ===========
class MenuItemForm(ModelForm):
    class Meta:  
        model = MenuItem
        fields = "__all__"

        labels = {
            'name' : 'Menu item name',
            'desc' : 'Little bit about it',
            'price' : 'Pricing',
            'menu_cat' : 'Choose category'
        }
        
        widgets = {
            'name' : forms.TextInput(attrs={'class': 'form-control'}),
            'desc' : forms.Textarea(attrs={'class': 'form-control'}),
            'price' : forms.NumberInput(attrs={'class': 'form-control'}),
            'menu_cat' : forms.Select()
        }