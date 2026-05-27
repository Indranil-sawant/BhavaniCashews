from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import User


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
        
    mock_wishlist = [
        {
            'name': 'Premium Jumbo W180',
            'price': '850.00',
            'package': '500G VACUUM PACK',
            'image': 'https://lh3.googleusercontent.com/aida-public/AB6AXuCkJtgbxeP2aNO2xWb_T5SQ_c0A0TJ822298ye2f_5cKsQUredr3GGQGQ02C3ZuYheuk8qna9ilAZesa7ghqTr67BYJ2Ib7fBNKbJYD-oRs0Y2uaXUk1OGTSXXa-vt3CKBliLIP9DMaFGaZNFeKfoAi5GXdGjd5nSzokLHfeMOM26ZA1LujTLssTJR0uoC8NlJhDE2YjF8ogoODFXRVgoH0YElkVFMxIUmYscu04qx-dGKwksd0y0N6YmGDfGeYpEH0lxrlUhmM6NQ'
        },
        {
            'name': 'Himalayan Salted Roast',
            'price': '620.00',
            'package': '250G LUXURY TIN',
            'image': 'https://lh3.googleusercontent.com/aida-public/AB6AXuAdhQxcyHKhVLuFNlwaOMv4LnqcFWPf53U_TQbHy9Y0ddE3IW6uk7k9yr44HlW0FcgUNM1SE1e_8RrQK0zKfje6dhDWKlxaekeubGxLtLK8Hf28zM6Ia5_MC0l_OggX32bv0FO5Wwc_Rh5jziWt3KxrSNdSEPx-IrBUkfQhko8HhZoUWWopnc86USzwjKmWzJvJ5Ke_8A3jcLaGPjZZ41wuHE5j29UWLkTNvZOnjyxUav4olbS7OMkf-6SJFptllxcbzM2YR-Nl-b8'
        },
        {
            'name': 'Organic Broken Splits',
            'price': '450.00',
            'package': '1KG ECO-POUCH',
            'image': 'https://lh3.googleusercontent.com/aida-public/AB6AXuBAuvzgTH3n-SWHIxHpekdUHxXbmhYy1aPTSNzSv_e2LnvHM2rknfqI__XaTaMyauj62x2bpwGm6lygybaNQsBPR4MZ9-AQFbiMNJAmXDaS-Nbur-wQqZPYFdqdS_J2XOhMC07Nh2Kb2Cftng0Qkzdf09MfMMe5eOwX2eHw0v93o-mzSyWx1BVpPZIDEWsHuA09YkYKfiXp6NaKc8sGslYpsyVLI9AIjGzs_AI0rTI_WSDYlESzXqsTJAZp5y-OkRW9YYrq1GbvIqg'
        }
    ]

    context = {
        'orders': orders_data,
        'wishlist': mock_wishlist,
    }
    return render(request, 'accounts/profile.html', context)