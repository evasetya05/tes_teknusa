from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def dashboard_view(request):
    """
    Dashboard view that requires user to be logged in
    """
    return render(request, 'dashboard/dashboard.html')
