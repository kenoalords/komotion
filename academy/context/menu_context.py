from academy.models import Category, Software, Rank

def categories(request):
    return { 'categories' : Category.objects.all() }

def softwares(request):
    return { 'softwares' : Software.objects.all() }

def ranks(request):
    return { 'ranks' : Rank.objects.all() }
