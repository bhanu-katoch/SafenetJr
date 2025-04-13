# guardian/views.py

from django.http import JsonResponse
from .models import Parent
from django.shortcuts import get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login,logout

from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect

from django.shortcuts import render, redirect
from .models import Parent, Child
from django.contrib.auth.decorators import login_required
import uuid

@login_required
def parent_dashboard(request):
    parent = Parent.objects.get(user=request.user)

    if request.method == 'POST':
        child_name = request.POST.get('child_name')
        child_number = request.POST.get('child_number')

        # Create a new Child
        Child.objects.create(
            parent=parent,
            child_number=child_number,
            name=child_name,
            child_id=str(uuid.uuid4())  # Auto-generate unique child_id
        )
        return redirect('parent_dashboard')

    children = parent.children.all()  # Fetch all children of this parent
    return render(request, 'dashboard.html', {'children': children,'pid':parent.parent_id})

def custom_logout(request):
    logout(request)
    return render(request, 'logout.html')

def home(request):
    return render(request,'home.html')
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create a Parent object linked to the user
            Parent.objects.create(user=user)
            login(request, user)  # Automatically login after registration
            return redirect('parent_dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def get_child_id(request):
    # Fetch parent_id and child_number from GET parameters
    parent_id = request.GET.get('parent_id')
    child_number = request.GET.get('child_number')

    if not parent_id or not child_number:
        return JsonResponse({"error": "parent_id and child_number are required"}, status=400)

    try:
        parent = Parent.objects.get(parent_id=parent_id)
        child = Child.objects.get(id=parent.id)
        return JsonResponse({"child_id": child.child_id})

    except Parent.DoesNotExist:
        return JsonResponse({"error": "Child not found"}, status=404)

@login_required
def add_child(request):
    if request.method == 'POST':
        parent = Parent.objects.get(user=request.user)
        child_name = request.POST.get('child_name')
        child_number = request.POST.get('child_number')

        # Create and save the new child
        Child.objects.create(
            parent=parent,
            child_number=child_number,
            name=child_name,
            child_id=str(uuid.uuid4())  # Generate unique child ID
        )
        return redirect('parent_dashboard')  # Redirect to dashboard after adding child

    return render(request, 'dashboard.html')
