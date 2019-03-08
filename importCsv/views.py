from django.contrib.auth import logout
from django.shortcuts import render
from django.contrib import messages

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
import json
from io import TextIOWrapper,StringIO
from importCsv.forms import uploadForm,upload_url,searchForm

from django.views.decorators.csrf import ensure_csrf_cookie


@login_required
@ensure_csrf_cookie
def csv_import(request):
    if request.method == 'POST':
        form = uploadForm(request.POST, request.FILES)
        if form.is_valid():
            errors  = handle_uploaded_file(TextIOWrapper(request.FILES['csv_file'], encoding="utf-8"),request.POST["title"])
            if len(errors) == 0:
                messages.success(request, "Successfully Uploaded!")
            else:
                for err in errors:
                    messages.add_message(request,messages.WARNING,"can not import "+ ' '.join(err))
            return render(request, 'post_form.html')
    else:
        form = uploadForm()
    return render(request, 'post_form.html', {'form': form})


def handle_uploaded_file(file,title):
    import csv
    from .models import City,Hotel
    errors = []
    csv_data = csv.reader(file, delimiter=';')
    if title == "city":
        for row in csv_data:
            try:
                if row[0] != "":
                    rec = City.objects.get(abbrev=row[0])
                    errors.append(row)
                continue
            except:
                if len(row) ==2 :
                    rec = City(abbrev=row[0],name=row[1])
                    rec.save()
    elif title == "hotel":
        for row in csv_data:
            try:
                if row[1] != "":
                    rec = Hotel.objects.get(data=row[1])
                continue
            except:
                if len(row) ==3 :
                    try:
                        hasCity = City.objects.get(abbrev=row[0])
                        rec = Hotel(city= hasCity, data=row[1], name=row[2])
                        rec.save()
                    except:
                        errors.append(row)
                        continue
    return errors


def logoutUser(request):
   logout(request)
   messages.add_message(request,messages.SUCCESS,"Successfully logged out")
   return HttpResponseRedirect('/')


def index(request):
    return render(request,'main.html')

@login_required
def csv_setting(request):
    from .models import Url
    if request.method == 'POST':
        form = upload_url(request.POST)
        if form.is_valid():
            file = get_file(request)
            if len(file) != 0 and request.POST["save"]=="on":
                Url.objects.get_or_create(url=request.POST["url"],defaults={'title':request.POST["title"],'username':request.POST["username"],'password':request.POST["password"]})
            errors = handle_uploaded_file(StringIO(file),request.POST["title"])
            if len(errors) == 0:
                messages.success(request, "Successfully Uploaded!")
            else:
                for err in errors:
                    messages.add_message(request, messages.WARNING, "can not import " + ' '.join(err))
            return render(request, 'settings.html')
    else:
        form = uploadForm()
    return render(request, 'settings.html', {'form': form})


def get_file(request):
    import requests
    data = requests.get(request.POST["url"],auth=(request.POST["username"],request.POST["password"]))
    if data.status_code != 200:
        messages.error(request,"Received an error "+str(data.status_code))
        return render(request,"settings.html")
    return data.text


def search(request):
    from .models import City,Hotel
    cities = City.objects.all()
    form = searchForm(request.POST or None,cities=cities)
    if request.method == 'POST':
        if form.is_valid():
            hotels =[]
            checkedCity =[]
            for c in request.POST:
                if c =='csrfmiddlewaretoken':
                    continue
                city = City.objects.get(abbrev=c)
                checkedCity.append(city.abbrev)
                hotels.extend(Hotel.objects.filter(city=city))
            return render(request, 'search.html',{'cities':cities,'hotels':hotels,'checkedCity':checkedCity})
    else:
        return render(request, 'search.html', {'form': form,'cities':cities})
