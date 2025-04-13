from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import History
from guardian.models import Child
from datetime import datetime
from django.shortcuts import redirect,render

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Child, History
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.http import Http404


@api_view(['POST'])
def upload_history(request):
    """
    API endpoint to upload a single browsing history.
    """
    data = request.data  # DRF already parses the incoming JSON

    child_id = data.get("child_id")
    visited_url = data.get("visited_url")
    title = data.get("title", "")
    visit_time = data.get("visit_time")

    # Check if required data is provided
    if not child_id or not visited_url or not visit_time:
        return Response({"error": "child_id, visited_url, and visit_time are required."}, status=status.HTTP_400_BAD_REQUEST)

    # Check if child exists in the database
    try:
        child = Child.objects.get(child_id=child_id)  # Fetch child by child_id
    except Child.DoesNotExist:
        return Response({"error": "Child not found."}, status=status.HTTP_404_NOT_FOUND)

    # Parse visit_time to a datetime object (if it exists)
    try:
        visit_time = datetime.fromtimestamp(visit_time / 1000)  # Assuming visit_time is in milliseconds, converting to datetime
    except Exception as e:
        return Response({"error": f"Invalid visit_time: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

    # Save history data into the database
    History.objects.create(
        child=child,
        visited_url=visited_url,
        title=title,
        visit_time=visit_time  # Store the parsed datetime object
    )

    return Response({"message": "History uploaded successfully!"}, status=status.HTTP_200_OK)

@login_required
def history_view(request, child_id):
    try:
        # Fetch the Child instance corresponding to the provided child_id
        child = Child.objects.get(child_id=child_id)

        # Fetch the history records for this child
        histories = History.objects.filter(child=child).order_by('-visit_time')  # Ordered by visit time (most recent first)
    
    except Child.DoesNotExist:
        raise Http404("Child not found.")
    
    context = {
        'child': child,
        'histories': histories
    }
    return render(request, 'history.html', context)