from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import CreateUserForm
from manageStore.forms import UserForm
from django.contrib.auth.models import User
# =========================================
from .models import *
# from .filters import SheetFilter
from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm
from django.http import HttpResponseRedirect
from django.http import HttpResponse
import openpyxl
import time
from django_cryptography.fields import encrypt
from django.db.models import Count
from django.contrib import messages
from tablib import Dataset
from .resources import *







@login_required(login_url='http://127.0.0.1:8000/login')
def add_data_source(request):
    return render(request, 'app/add_data_source.html')

@login_required(login_url='http://127.0.0.1:8000/login')
def registerPage(request):
    return render(request, 'app/test.html')

@login_required(login_url='http://127.0.0.1:8000/login')
def manage_store(request):
    return render(request, 'app/manage_store.html')

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('manage_store')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('manage_store')
            else: 
                messages.info(request, 'Username OR password is incorrect')
    return render(request, 'app/login.html')


#--------------------------------------------------------
# ==============>Section add user<=======================
#--------------------------------------------------------
def registerPage(request):
        if not request.user.is_authenticated:
            return redirect('login')
        users = User.objects.all()
        form = CreateUserForm()
        if request.method == 'POST': 
                form = CreateUserForm(request.POST)
                if form.is_valid():
                    form.save()
                    user = form.cleaned_data.get('username')
                    messages.success(request, 'Account was updated ' + user)
                    return redirect('add_user')
        context ={'form':form,'users':users,'manageStore': Manage_store.objects.all(), 'manageStoreId': Manage_store.objects.all()}
        return render(request, 'app/add_user.html', context)

def destroy_user(request, id):
    if not request.user.is_authenticated:
            return redirect('login')  
    users = User.objects.get(id=id)  
    users.delete()  
    return HttpResponseRedirect("/add_user") 

#Edit&Update-User
def edit_user(request, id):
    if not request.user.is_authenticated:
            return redirect('login')  
    users = User.objects.get(id=id)  
    return render(request,'app/edit_user.html', {'users':users}) 


def update_user(request, id):
    if not request.user.is_authenticated:
            return redirect('login')   
    users =  User.objects.get(id=id)  
    user = UserForm(request.POST, instance = users)
    if user.is_valid():  
        user.save()  
        return redirect("/add_user")  

def logoutUser(request):
    logout(request)
    return redirect('login')

#--------------------------------------------------------
# ==============>end Section add user<===================
#--------------------------------------------------------

#--------------------------------------------------------
# =============start section data resource<==============
#--------------------------------------------------------
def add_data_source(request):
    if not request.user.is_authenticated:
            return redirect('login') 
    data_source = Data_source.objects.all()
    context={'data_source': data_source,'manageStore': Manage_store.objects.all(), 'manageStoreId': Manage_store.objects.all()}
    return render(request, 'app/add_data_source.html',context )

# AddData
def addDataSource(request):
    if not request.user.is_authenticated:
            return redirect('login') 
    if request.method == 'POST':
      if request.POST['name']:
        dataSource = Data_source(name=request.POST['name'])
        dataSource.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

# editDataSource 
def editDataSource(request, id):
    if not request.user.is_authenticated:
        return redirect('login') 
    if id:
        dataSource = Data_source.objects.get(id=id)
        return render(request, "app/edit_data_source.html", context={'dataSource': dataSource})

# updateDataSource
def updateDataSource(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method == 'POST':
        if request.POST['name']:
            Data_source.objects.filter(id=request.POST['id']).update(name=request.POST['name'])
            return redirect("/")

# deleteData
def deleteData(request, id):
    if not request.user.is_authenticated:
        return redirect('login')
    Data_source.objects.filter(id=id).delete()
    return redirect("/")


#--------------------------------------------------------
# ==============>end section data resource<=======================
#--------------------------------------------------------

#--------------------------------------------------------
# ==============>start section mange source <=======================
#--------------------------------------------------------




def index():
    return redirect('/manage_store/')
         # -------- Start Upload Excel Sheet ----- #

def manage_store(request):
    if not request.user.is_authenticated:
        return redirect('login')
    data = Data.objects.all()
    read_data_source = Data_source.objects.all()
    if  'gender' or 'state' or 'city' or 'profit' in request.POST:
        # fetch all data form database
        all_data = Data.objects.all()
        #------>custom search<---------
        # ----->define variables<------
        gender = request.POST.get('gender', False)
        state  = request.POST.get('state', False)
        city   = request.POST.get('city', False)
        profit = request.POST.get('profit', False)
        
        if city and state and gender and profit:
            f_city = all_data.filter(city = city)
            f_state = f_city.filter(state = state)
            f_gender = f_state.filter(gender = gender)
            if profit == "up":
                f_profit = f_gender.filter(profit__gte = 0)
                return render(request, 'app/manage_store.html',{'hello2': f_profit})
            else:
                f_profit = f_gender.filter(profit__lte = 0)
                return render(request, 'app/manage_store.html',{'hello2': f_profit})
        else: 
            if gender:
                f_gender = all_data.filter(gender = gender)
                return render(request, 'app/manage_store.html',{'hello2': f_gender})
            elif state:
                f_state = all_data.filter(state = state)
                return render(request, 'app/manage_store.html',{'hello2': f_state})
            elif city:
                f_city = all_data.filter(city = city)
                return render(request, 'app/manage_store.html',{'hello2': f_city})
            elif profit:
                if profit == "up":
                    f_profit = all_data.filter(profit__gte = 0)
                    return render(request, 'app/manage_store.html',{'hello2': f_profit})
                else:
                    f_profit = all_data.filter(profit__lte = 0)
                    return render(request, 'app/manage_store.html',{'hello2': f_profit})

    return render(request, 'app/manage_store.html', {'Data': data, 'read_data_source': read_data_source,'manageStore': Manage_store.objects.all(), 'manageStoreId': Manage_store.objects.all()})
# ------------------ End View Pages ------------------ #
# ------------- Start Upload Excel Sheet ------------------ #
def upload(request , id=None):
    data_source_name = ''
    if request.method == 'POST':
        start_time = time.time()
        # Take data_source Id From select
        id_source_selected = request.POST['data_source']
        # data_resource = DataResources()
        dataset = Dataset()
        if not request.FILES:
            return redirect('/manage_store')
        new_data = request.FILES['myfile']
        # To Get File Name
        file_name = request.FILES['myfile'].name
        if not new_data.name.endswith('xls') and not new_data.name.endswith('xlsx'):
            messages.info(request, 'wrong format')
            return redirect('/manage_store')
        if new_data.name.endswith('xls'):
            import_data = dataset.load(new_data.read(), format='xls')
        elif new_data.name.endswith('xlsx'):
            import_data = dataset.load(new_data.read(), format='xlsx')
        for p in Data_source.objects.raw('SELECT * FROM managestore_data_source where id= %s' % id_source_selected):
            data_source_name = p.name
        if not Manage_store.objects.all().filter(file_name=file_name).exists():
            ManageStoreId = upload_manage_source(data_source_name, file_name, 0, 0, id_source_selected)
        else:
            return redirect('/manage_store')
        for data in import_data:
            value = Data(data[0], data[1], data[2], data[3], data[4], data[5],
                         data[6], data[7], data[8], data[9], data[10], data[11],
                         data[12], data[13], ManageStoreId)
            value.save()
        excution_time_to_upload_sheet = time.time() - start_time
        Manage_store.objects.all().filter(id=ManageStoreId).update(execution_time=excution_time_to_upload_sheet,
                                                                   number_of_records=len(Data.objects.all().filter(
                                                                       manage_store_id=ManageStoreId)))
        data = Data.objects.all()
        read_data_source = Data_source.objects.all()
        return render(request, 'app/manage_store.html',
                      {'Data': data, 'read_data_source': read_data_source, 'data_source_name': data_source_name,'manageStore': Manage_store.objects.all(), 'manageStoreId': Manage_store.objects.all().filter(id=id)})
# ---------------- End Upload Excel Sheet ------------------ #
def upload_manage_source(data_source_name, file_name, execution_time, number_of_records, id_source_selected):
    ManageStoreValue = Manage_store()
    ManageStoreValue.data_source_name = data_source_name
    ManageStoreValue.file_name = file_name
    ManageStoreValue.execution_time = execution_time
    ManageStoreValue.number_of_records = number_of_records
    ManageStoreValue.data_source_id = id_source_selected
    ManageStoreValue.save()
    return ManageStoreValue.id
    
# ---------------- End Upload Excel Sheet ------------------ #

def information(request, id=None):
    return render(request, 'app/information.html',{'manageStore': Manage_store.objects.all(), 'manageStoreId': Manage_store.objects.all().filter(id=id)})

#--------------------------------------------------------
# ==============>end section manage source<=======================
#--------------------------------------------------------