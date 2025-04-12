from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import History
from guardian.models import Child
from datetime import datetime
from django.shortcuts import redirect,render

@api_view(['POST'])
def upload_history(request):
    """
    API endpoint to upload the browsing history.
    """
    #print("Request data:", request.data)  # Log incoming request data

    data = request.data  # DRF already parses the incoming JSON

    child_id = data.get("child_id")
    history = data.get("history")

    if not child_id or not history:
        return Response({"error": "child_id and history are required."}, status=status.HTTP_400_BAD_REQUEST)

    # Check if child exists in the database
    try:
        child = Child.objects.get(child_id=child_id)  # Fetch child by child_id
    except Child.DoesNotExist:
        return Response({"error": "Child not found."}, status=status.HTTP_404_NOT_FOUND)

    # Save history data into the database
    for item in history:
        # Parse visit_time to a datetime object if it exists
        visit_time = item.get('lastVisitTime')
        if visit_time:
            try:
                # Assuming visit_time is in milliseconds, converting it to a Python datetime object
                visit_time = datetime.fromtimestamp(visit_time / 1000)  # Convert ms to seconds
            except Exception as e:
                return Response({"error": f"Invalid visit_time: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            visit_time = None  # Default to None if no visit_time provided

        # Create History object and save it
        History.objects.create(
            child=child,
            visited_url=item.get('url'),
            title=item.get('title', ''),
            visit_time=visit_time  # Store the parsed datetime object
        )

    return Response({"message": "History uploaded successfully!"}, status=status.HTTP_200_OK)

def history_view(request):
    # Fetch all the history records (or filter by some condition, if needed)
    histories = History.objects.all().order_by('-visit_time')  # Ordered by visit time (most recent first)

    context = {
        'histories': histories
    }
    return render(request, 'history.html', context)
