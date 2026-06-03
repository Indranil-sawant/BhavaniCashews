from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import User, Address
from .forms import AddressForm


def login_view(request):
    if request.user.is_authenticated:
        return redirect('profile')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect('profile')
        else:
            messages.error(request, 'Invalid credentials. Please try again.')

    return render(request, 'accounts/login.html')


def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('home')


def register_view(request):
    if request.user.is_authenticated:
        return redirect('profile')

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if not username or not password or not email:
            messages.error(request, 'Please fill in all required fields.')
        elif password != confirm_password:
            messages.error(request, 'Passwords do not match.')
        elif User.objects.filter(username=username).exists():
            messages.error(request, 'Username is already taken.')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Email is already registered.')
        else:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                phone=phone
            )
            login(request, user)
            messages.success(request, f"Welcome, {user.username}! Your account has been created.")
            return redirect('profile')

    return render(request, 'accounts/register.html')


@login_required
def profile_view(request):
    from orders.models import Order, OrderStatus
    real_orders = Order.objects.filter(user=request.user).order_by('-created_at')
    
    orders_data = []
    for order in real_orders:
        # Determine color for badge
        if order.status == OrderStatus.DELIVERED:
            status_color = 'bg-green-100 text-green-800'
        elif order.status == OrderStatus.CANCELLED:
            status_color = 'bg-red-100 text-red-800'
        elif order.status == OrderStatus.SHIPPED:
            status_color = 'bg-blue-100 text-blue-800'
        else:
            status_color = 'bg-amber-100 text-amber-800'
            
        # Determine total representation and action links for B2B wholesale inquiries
        is_b2b = order.payment_method == 'B2B'
        orders_data.append({
            'id': str(order.id),
            'date': order.created_at.strftime('%b %d, %Y'),
            'status': order.get_status_display(),
            'status_color': status_color,
            'total': "Custom Quote" if is_b2b else f"₹{order.total:,.2f}",
            'action': 'View Quote' if is_b2b else 'Track',
            'detail_url': f"/orders/detail/{order.id}/"
        })
        
    addresses = Address.objects.filter(user=request.user)
    address_form = AddressForm()

    context = {
        'orders': orders_data,
        'addresses': addresses,
        'address_form': address_form,
    }
    return render(request, 'accounts/profile.html', context)


@login_required
def address_create(request):
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()
            
            # Check if AJAX request
            if request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.content_type == 'application/json':
                return JsonResponse({'success': True, 'message': 'Address added successfully!'})
            
            messages.success(request, "Address added successfully!")
            return redirect('profile')
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.content_type == 'application/json':
                # Convert errors to flat list or dictionary
                errors = {field: [err['message'] for err in errs] for field, errs in form.errors.get_json_data().items()}
                return JsonResponse({'success': False, 'errors': errors})
            
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.replace('_', ' ').title()}: {error}")
    return redirect('profile')


@login_required
def address_edit(request, pk):
    address = get_object_or_404(Address, pk=pk, user=request.user)
    if request.method == 'POST':
        form = AddressForm(request.POST, instance=address)
        if form.is_valid():
            form.save()
            
            if request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.content_type == 'application/json':
                return JsonResponse({'success': True, 'message': 'Address updated successfully!'})
                
            messages.success(request, "Address updated successfully!")
            return redirect('profile')
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.content_type == 'application/json':
                errors = {field: [err['message'] for err in errs] for field, errs in form.errors.get_json_data().items()}
                return JsonResponse({'success': False, 'errors': errors})
                
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.replace('_', ' ').title()}: {error}")
    else:
        # GET request for edit: Return Address data as JSON for the modal edit form
        data = {
            'id': address.id,
            'full_name': address.full_name,
            'phone': address.phone,
            'address_line1': address.address_line1,
            'address_line2': address.address_line2 or '',
            'landmark': address.landmark or '',
            'city': address.city,
            'state': address.state,
            'pincode': address.pincode,
            'country': address.country,
            'is_default': address.is_default
        }
        return JsonResponse({'success': True, 'address': data})
    return redirect('profile')


@login_required
def address_delete(request, pk):
    address = get_object_or_404(Address, pk=pk, user=request.user)
    address.delete()
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'success': True, 'message': 'Address deleted successfully!'})
        
    messages.success(request, "Address deleted successfully!")
    return redirect('profile')


@login_required
def address_set_default(request, pk):
    address = get_object_or_404(Address, pk=pk, user=request.user)
    address.is_default = True
    address.save()
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'success': True, 'message': 'Default address updated!'})
        
    messages.success(request, "Default address updated!")
    return redirect('profile')