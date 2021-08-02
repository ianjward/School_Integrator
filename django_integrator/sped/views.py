from django.shortcuts import render


# Create your views here.
def add_file(request):
    return render(request, 'sped_add_file.html')
