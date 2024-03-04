#========================================================================================
#   Custom filter to apply specific functions on context values inside django tags      #
#   src: https://docs.djangoproject.com/en/dev/howto/custom-template-tags/#writing-custom-template-filters
#       https://www.geeksforgeeks.org/custom-template-filters-in-django/                #
#       https://reintech.io/blog/writing-custom-template-filters-in-django              #
#========================================================================================

from django import template 
  
register = template.Library() 

# The "@register.filter" decorator tells Django that this function should be registered as a template filter.
@register.filter()
def low(value): 
    return value.lower()



@register.filter(name="cut") # giving custom name to the filter
def cut(value, arg):
    return value.replace(arg, "")

# If you leave off the name argument, Django will use the function’s name as the filter name
@register.filter
def getval_by_key(dictionary, key):
    key = str(key)
    return dictionary.get(key)
