from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, AddRecordForm
from .models import Record, Carbrand, Cartypes, Vehicle
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User  # Import the User model
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.db import models
import os

# Create your views here.
@login_required
def dashboard(request):
    if request.user.is_authenticated:
        # Query the database to get the total count of customers (records)
        total_customers = Record.objects.count()  # Assuming 'Record' is the model name

        # Retrieve user details from the request.user object
        user_first_name = request.user.first_name
        user_last_name = request.user.last_name
        user_email = request.user.email
        user_username = request.user.username

        # Determine the staff symbol based on is_staff
        staff_symbol = "✔️" if request.user.is_staff else "❌"

        # Query the database to get the total count of registered users
        total_users = User.objects.count()

        # Query the database to get the total count of registered users
        total_vehicles = Vehicle.objects.count()

        # Pass all the details to the template as context variables
        context = {
            'total_customers': total_customers,
            'user_first_name': user_first_name,
            'user_last_name': user_last_name,
            'user_email': user_email,
            'user_username': user_username,
            'staff_symbol': staff_symbol,  # Add the staff symbol to the context
            'total_users': total_users,    # Add the total users count to the context
            'total_vehicles': total_vehicles,
        }
    else:
        messages.success(request, "Please log in to access the dashboard.")
        return redirect('login')  # Redirect to the login page with the message

    return render(request, 'dashboard.html', context)

@login_required
def customers(request):
     records = Record.objects.all().order_by('-created_at')
     return render(request, 'customers.html', {'records':records})


def home(request):
    records = Record.objects.all()

    # Check to see if logging in
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        # Authenticate User
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request,user)
            messages.success(request, "You Have Been Logged In")
            return redirect('dashboard')
        else:
            messages.success(request, "")
            return redirect('home')
    else:
        return render(request, 'home.html', {})


def login_user(request):
    failed_login = False  # Initialize the failed_login variable
    # Check to see if logging in
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        # Authenticate User
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request,user)
            messages.success(request, "You Have Been Logged In")
            return redirect('dashboard')
        else:
            failed_login = True  # Set failed_login to True for a failed attempt
            messages.error(request, "There Was An Error Logging In, Please Try Again")

    return render(request, 'login.html', {'failed_login': failed_login})

@login_required
def logout_user(request):
    logout(request)
    messages.success(request, "You Have Been Logged Out")
    return redirect('home')


def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            # Authenticate and Login
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "You Have Successfully Registered!")
            return redirect('login')  # Redirect to the login page
    else:
        form = SignUpForm()
    return render(request, 'register.html', {'form': form})

@login_required
def customer_record(request, pk):
    if request.user.is_authenticated:
        # Look Up Records
        customer_record = Record.objects.get(id=pk)
        return render(request, 'record.html', {'customer_record':customer_record})
    else:
        messages.success(request, "You Must Be Logged In To View Records")
        return redirect('home')

@login_required
def delete_record(request,pk):
    if request.user.is_authenticated:
        delete_record = Record.objects.get(id=pk)
        delete_record.delete()
        messages.success(request, "Record Deleted Successfully")
        return redirect('customers')
    else:
        messages.success(request, "Please Login")
        return redirect('home')
    
@login_required 
def add_record(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = AddRecordForm(request.POST)
            if form.is_valid():
                # Save the record
                add_record = form.save()

                # Show a success message
                messages.success(request, "Customer Added Successfully")

                # Redirect to the 'customers' view
                return redirect('customers')
        else:
            form = AddRecordForm()
        
        return render(request, 'add_record.html', {'form': form})
    else:
        messages.success(request, "You Must Be Logged In...")
        return redirect('login')
    
@login_required  
def update_record(request, pk):
    if request.user.is_authenticated:
        current_record = Record.objects.get(id=pk)
        if request.method == 'POST':
            form = AddRecordForm(request.POST, instance=current_record)
            if form.is_valid():
                updated_record = form.save()
                messages.success(request, "Record has been updated")
                # Redirect to the updated record's detail page
                return HttpResponseRedirect(reverse('record', args=[updated_record.id]))
        else:
            form = AddRecordForm(instance=current_record)

        return render(request, 'update_record.html', {'form': form})
    else:
        messages.error(request, "You must be logged in.")
        return redirect('home')
    
@login_required
def car_brands(request):
    # Annotate the brands queryset with the count of associated cars
    brands_with_counts = Carbrand.objects.annotate(num_cars=Count('brand'))

    context = {'brands_with_counts': brands_with_counts}
    return render(request, 'car_brands.html', context)

@login_required
def add_carbrand(request):
    if request.method == "POST":
        brand = Carbrand()
        brand.brand = request.POST.get('brand')
        brand.description = request.POST.get('description')
        brand.status = request.POST.get('status')
        
        if len(request.FILES) != 0:
            brand.image = request.FILES['image']

        brand.save()
        messages.success(request, 'Car Brand Added Successfully')
        return redirect('car_brands')
    
    return render(request, 'add_carbrand.html', {})

@login_required
def edit_carbrand(request, pk):
    brands = Carbrand.objects.get(id=pk)
    if request.method == "POST":
        if len(request.FILES) != 0:
            if len(brands.image) > 0:
                os.remove(brands.image.path)
            brands.image = request.FILES['image']
        brands.brand = request.POST.get('brand')
        brands.description = request.POST.get('description')
        brands.status = request.POST.get('status')
        brands.save()
        messages.success(request, "Brand Updated Successfully")
        return redirect('car_brands')
    
    context = {'brands': brands}
    return render(request, 'edit_carbrand.html', context)

@login_required
def delete_carbrand(request, pk):
    brands = Carbrand.objects.get(id=pk)
    if len(brands.image) > 0:
        os.remove(brands.image.path)
    brands.delete()
    messages.success(request, "Brand Deleted Successfully")
    return redirect('car_brands')

@login_required
def car_types(request):
    types = Cartypes.objects.all()
    context = {'types': types}
    return render(request, 'car_types.html', context)  # Remove the extra curly braces

@login_required
def add_cartype(request):
    if request.method == "POST":
        types = Cartypes()
        types.type = request.POST.get('type')
        types.description = request.POST.get('description')
        types.status = request.POST.get('status')
        
        types.save()
        messages.success(request, 'Car Type Added Successfully')
        return redirect('car_types')
    
    return render(request, 'add_cartype.html', {})

@login_required
def edit_cartype(request, pk):
    types = Cartypes.objects.get(id=pk)
    
    if request.method == 'POST':
        types.type = request.POST.get('type')
        types.description = request.POST.get('description')
        types.status = request.POST.get('status')
        types.save()
        messages.success(request, "Car Type Updated Successfully")
        return redirect('car_types')
    
    context = {'types': types}
    return render(request, 'edit_cartype.html', context)

@login_required
def delete_cartype(request, pk):
    types = Cartypes.objects.get(id=pk)
    types.delete()
    messages.success(request, "Car Type Deleted Successfully")
    return redirect('car_types')

@login_required
def all_vehicles(request):
    # Retrieve all vehicles
    all_vehicles = Vehicle.objects.all()
    vehicles = all_vehicles

    return render(request, 'all_vehicles.html', {'vehicles': vehicles})

@login_required
def add_vehicle(request):
    # Fetch the available "Type" choices from the Cartypes model
    cartypes = Cartypes.objects.all()
    brands = Carbrand.objects.all()

    if request.method == "POST":
        all_vehicles = Vehicle()
        all_vehicles.brand = request.POST.get('brand')
        all_vehicles.type = request.POST.get('type')
        all_vehicles.model = request.POST.get('model')
        all_vehicles.enginetype = request.POST.get('enginetype')
        all_vehicles.transmission = request.POST.get('transmission')
        all_vehicles.technology = request.POST.get('technology')
        all_vehicles.mvfileno = request.POST.get('mvfileno')
        all_vehicles.plate = request.POST.get('plate')
        all_vehicles.variant = request.POST.get('variant')
        all_vehicles.color = request.POST.get('color')
        all_vehicles.mileage = request.POST.get('mileage')
        all_vehicles.engineno = request.POST.get('engineno')
        all_vehicles.chasisno = request.POST.get('chasisno')
        all_vehicles.description = request.POST.get('description')
        all_vehicles.price = request.POST.get('price')
        all_vehicles.status = request.POST.get('status')

        if 'image' in request.FILES:
            all_vehicles.image = request.FILES['image']

        all_vehicles.save()
        messages.success(request, 'Vehicle Added Successfully')
        return redirect('all_vehicles')

    return render(request, 'add_vehicle.html', {'cartypes': cartypes, 'brands': brands})

@login_required
def vehicle_details(request, pk):
    if request.user.is_authenticated:
        # Look Up Records
        vehicle_record = Vehicle.objects.get(id=pk)
        return render(request, 'vehicle_details.html', {'vehicle_record':vehicle_record})
    else:
        messages.success(request, "You Must Be Logged In To View Records")
        return redirect('home')

@login_required
def update_vehicle(request, pk):
    all_vehicles = Vehicle.objects.get(id=pk)
    # Fetch the available "Type" choices from the Cartypes model
    cartypes = Cartypes.objects.all()
    brands = Carbrand.objects.all()

    if request.method == "POST":
        if len(request.FILES) != 0:
            if len(all_vehicles.image) > 0:
                os.remove(all_vehicles.image.path)
            all_vehicles.image = request.FILES['image']
        all_vehicles.brand = request.POST.get('brand')
        all_vehicles.type = request.POST.get('type')
        all_vehicles.model = request.POST.get('model')
        all_vehicles.enginetype = request.POST.get('enginetype')
        all_vehicles.transmission = request.POST.get('transmission')
        all_vehicles.technology = request.POST.get('technology')
        all_vehicles.mvfileno = request.POST.get('mvfileno')
        all_vehicles.plate = request.POST.get('plate')
        all_vehicles.variant = request.POST.get('variant')
        all_vehicles.color = request.POST.get('color')
        all_vehicles.mileage = request.POST.get('mileage')
        all_vehicles.engineno = request.POST.get('engineno')
        all_vehicles.chasisno = request.POST.get('chasisno')
        all_vehicles.description = request.POST.get('description')
        all_vehicles.price = request.POST.get('price')
        all_vehicles.status = request.POST.get('status')
        all_vehicles.save()
        messages.success(request, "Vehicle Updated Successfully")
        return redirect('all_vehicles')
    
    context = {'all_vehicles': all_vehicles}
    return render(request, 'update_vehicle.html', {'all_vehicles':all_vehicles, 'cartypes': cartypes, 'brands': brands})

@login_required
def delete_vehicle(request, pk):
    all_vehicles = Vehicle.objects.get(id=pk)
    if len(all_vehicles.image) > 0:
        os.remove(all_vehicles.image.path)
    all_vehicles.delete()
    messages.success(request, "Vehicle Deleted Successfully")
    return redirect('all_vehicles')


# CSS
# def style(request):
#     return render(request, '')