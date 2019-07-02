from .models import appearance, Category

def backprocessor(request):
    backimage = appearance.objects.all()  
    for a in backimage:
        return {'backimage': a}

def categoryprocessor(request):
    categories = Category.objects.all()  
    return {'categories':categories}