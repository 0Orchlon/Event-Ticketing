from django.shortcuts import render, redirect
from .models import Event, Booking
from .forms import EventForm  # We'll create a form for the event creation

# List all events
def event_list(request):
    events = Event.objects.all()
    return render(request, 'admin/event_list.html', {'events': events})

# Create a new event
def create_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin:event_list')
    else:
        form = EventForm()
    return render(request, 'admin/create_event.html', {'form': form})

# View event details and bookings
def event_detail(request, event_id):
    event = Event.objects.get(id=event_id)
    bookings = Booking.objects.filter(event=event)
    return render(request, 'admin/event_detail.html', {'event': event, 'bookings': bookings})
