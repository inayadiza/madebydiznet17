import datetime
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from main.forms import ClothingEntryForm
from main.models import ClothingEntry 
from django.http import HttpResponse
from django.core import serializers
from django.shortcuts import reverse
from django.http import HttpResponseRedirect
from .models import ClothingEntry

# Create your views here.
@login_required(login_url='/login')
def show_main(request):
    clothing_entries = ClothingEntry.objects.all()  # Menampilkan semua item pakaian

    context = {
        'npm': '2306245711',
        'name': request.user.username,
        'class': 'PBP B',
        'Price': 'Rp. 180.000',
        'Description': 'A brown cardigan is a cozy, versatile layering piece, made from soft materials like wool or cotton.',
        'clothing_entries': clothing_entries,  # Pass clothing items to the template
        'last_login': request.COOKIES.get('last_login', 'Tidak ada informasi login terakhir'),  # Menghindari KeyError
    }

    return render(request, "main.html", context)

def create_clothing_entry(request):
    form = ClothingEntryForm()

    if request.method == "POST":
        form = ClothingEntryForm(request.POST)
        if form.is_valid():
            clothing_entry = form.save(commit=False)
            clothing_entry.user = request.user
            clothing_entry.save()
            return redirect('main:show_main')

    context = {'form': form}
    return render(request, "create_clothing_entry.html", context)

def show_xml(request):
    data = ClothingEntry.objects.all()
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json(request):
    data = ClothingEntry.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def show_xml_by_id(request, id):
    data = ClothingEntry.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json_by_id(request, id):
    data = ClothingEntry.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def register(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been successfully created!')
            return redirect('main:login')
    context = {'form':form}
    return render(request, 'register.html', context)

def login_user(request):
   if request.method == 'POST':
      form = AuthenticationForm(data=request.POST)

      if form.is_valid():
        user = form.get_user()
        login(request, user)
        response = HttpResponseRedirect(reverse("main:show_main"))
        response.set_cookie('last_login', str(datetime.datetime.now()))
        return response
   else:
      form = AuthenticationForm(request)
   context = {'form': form}
   return render(request, 'login.html', context)

def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('main:login'))
    response.delete_cookie('last_login')
    return response

def edit_clothing(request, id):
    clothing = ClothingEntry.objects.get(pk = id)

    form = ClothingEntryForm(request.POST or None, instance=clothing)

    if form.is_valid() and request.method == "POST":
        form.save()
        return HttpResponseRedirect(reverse('main:show_main'))

    context = {'form': form}
    return render(request, "edit_clothing.html", context)

def delete_clothing(request, id):
    clothing = ClothingEntry.objects.get(pk = id)
    clothing.delete()
    return HttpResponseRedirect(reverse('main:show_main'))

def show_clothing(request):
    clothing_entries = ClothingEntry.objects.all()  # Make sure this queryset is correct and contains valid entries
    context = {'clothing_entries': clothing_entries}
    return render(request, 'products.html', context)
