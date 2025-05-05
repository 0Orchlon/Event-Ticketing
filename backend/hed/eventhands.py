# eventhandle.py

import os
import json
import base64
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.db import connection
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from backend.settings import connectDB, disconnectDB
from django.utils import timezone

def sendResponse(request, code, data, action):
    """
    Ensure that sendResponse always returns a JsonResponse
    """
    response = {
        "code": code,
        "data": data,
        "action": action
    }
    return JsonResponse(response)

@csrf_exempt
def eventapi(request):
    action = None

    if request.content_type.startswith('application/json'):
        try:
            data = json.loads(request.body)
            action = data.get('action')
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    elif request.method == 'POST':
        action = request.POST.get('action')

    if not action:
        return JsonResponse({'error': 'Invalid action for form-data'}, status=400)

    print(f"Received action: {action}")

    if action == "create_event":
        return dt_create_event(data)

    elif action == "list_events":
        return list_events()

    elif action == "event_detail":
        return event_detail(data)

    elif action == "available_seats":
        return available_seats(data)

    elif action == "book_ticket":
        return book_ticket(data)

    elif action == "get_user_tickets":
        return get_user_tickets(data)

    elif action == "mock_payment":
        return mock_payment(data)

    elif action == "get_seats":
        return get_seats(data)

    elif action == "edit_event":
        print("Received action:", request.POST.get("action"))
        return edit_event(request)
    elif action == "get_seats":
        return get_seats(request)


    else:
        return JsonResponse({"error": "Invalid action"}, status=4001)

def dt_create_event(request):
    action = request.POST.get("action")

    try:
        ename = request.POST.get("ename")
        edesc = request.POST.get("edesc")
        edateb = request.POST.get("edateb")
        edatee = request.POST.get("edatee")
        venid = request.POST.get("vid")
        images = request.FILES.getlist("images") 
    except KeyError:
        return sendResponse(request, 3027, [], action)

    try:
        myConn = connectDB()
        cursor = myConn.cursor()

        # Insert event details
        query = """
            INSERT INTO event (name, description, start_time, end_time, venue)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING eventid;
        """
        cursor.execute(query, [ename, edesc, edateb, edatee, venid])
        event_id = cursor.fetchone()[0]

        # Save and insert each image

        # Save and insert each image
        for image in images:
            filename = f"{int(timezone.now().timestamp())}_{image.name}"
            image_dir = os.path.join('media', 'events')
            os.makedirs(image_dir, exist_ok=True)
            filepath = os.path.join(image_dir, filename)

            with open(filepath, 'wb+') as f:
                for chunk in image.chunks():
                    f.write(chunk)

            # Insert image path to event_images table
                cursor.execute("""
        INSERT INTO event_images (eventid, image_path)
        VALUES (%s, %s)
    """, [event_id, filepath])

# Commit AFTER both inserts
        myConn.commit()

        cursor.close()
        resp = sendResponse(request, 200, {'eventid': event_id}, action)

    except Exception as e:
        print(f"Error creating event: {e}")
        resp = sendResponse(request, 5000, [], action)
    finally:
        disconnectDB(myConn)
        return resp

def list_events():
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT e.eventid, e.name, e.description, e.start_time, e.end_time, e.venue,
                ARRAY_AGG(ei.image_path) AS image_paths
            FROM event e
            LEFT JOIN event_images ei ON e.eventid = ei.eventid
            GROUP BY e.eventid
        """)
        rows = cursor.fetchall()

    events = [
        {
            "eventid": row[0],
            "name": row[1],
            "description": row[2],
            "start_time": row[3],
            "end_time": row[4],
            "venue": row[5],
            "images": [f"/media/{path}" for path in row[6] if path] if row[6] else [],
        }
        for row in rows
    ]
    return JsonResponse(events, safe=False)

def event_detail(data):
    eventid = data.get("eventid")
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM event WHERE eventid = %s", [eventid])
        row = cursor.fetchone()
        if not row:
            return JsonResponse({"error": "Event not found"}, status=404)

        # Get all images for the event
        cursor.execute("SELECT image_path FROM event_images WHERE eventid = %s", [eventid])
        img_rows = cursor.fetchall()
        images = [f"/{img[0]}" for img in img_rows if img[0]]

    event = {
        "eventid": row[0],
        "name": row[1],
        "description": row[2],
        "venue": row[3],
        "start_time": row[4],
        "end_time": row[5],
        "images": images
    }
    return JsonResponse(event)


def available_seats(data):
    eventid = data.get("eventid")
    with connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM ticket WHERE eventid = %s AND booked = 0", [eventid])
        row = cursor.fetchone()

    return JsonResponse({"available_seats": row[0]})


def get_seats(data):
    eventid = data.get("eventid")
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT ticketid, seat, price, booked 
            FROM ticket WHERE eventid = %s
        """, [eventid])
        rows = cursor.fetchall()

    seats = [
        {
            "ticketid": row[0],
            "seat": row[1],
            "price": float(row[2]),
            "booked": bool(row[3])
        } for row in rows
    ]
    return JsonResponse(seats, safe=False)


def book_ticket(data):
    userid = data.get("userid")
    ticketid = data.get("ticketid")

    if not userid or not ticketid:
        return JsonResponse({"error": "Missing userid or ticketid"}, status=400)

    with connection.cursor() as cursor:
        cursor.execute("SELECT booked FROM ticket WHERE ticketid = %s", [ticketid])
        row = cursor.fetchone()

        if not row:
            return JsonResponse({"error": "Ticket not found"}, status=404)
        if row[0]:  # Already booked
            return JsonResponse({"error": "Ticket already booked"}, status=400)

        # Book the ticket
        cursor.execute("UPDATE ticket SET booked = 1 WHERE ticketid = %s", [ticketid])
        cursor.execute("""
            INSERT INTO booking (userid, ticketid, payment_status, booked_at)
            VALUES (%s, %s, %s, NOW())
        """, [userid, ticketid, "pending"])

    return JsonResponse({"success": True, "message": "Ticket booked successfully"})

def mock_payment(data):
    bookingid = data.get("bookingid")

    with connection.cursor() as cursor:
        # Just update the status
        cursor.execute("UPDATE booking SET payment_status = 'paid' WHERE bookingid = %s", [bookingid])

    return JsonResponse({"success": True})


def get_user_tickets(data):
    userid = data.get("userid")
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT b.bookingid, b.payment_status, t.seat, e.name, e.start_time, e.end_time
            FROM booking b
            JOIN ticket t ON b.ticketid = t.ticketid
            JOIN event e ON t.eventid = e.eventid
            WHERE b.userid = %s
        """, [userid])
        rows = cursor.fetchall()

    tickets = [
        {
            "bookingid": row[0],
            "payment_status": row[1],
            "seat": row[2],
            "event_name": row[3],
            "start_time": row[4],
            "end_time": row[5]
        } for row in rows
    ]
    return JsonResponse(tickets, safe=False)


def edit_event(request):
    action = request.POST.get("action")

    try:
        eventid = request.POST.get("eventid")
        ename = request.POST.get("ename")
        edesc = request.POST.get("edesc")
        edateb = request.POST.get("edateb")
        edatee = request.POST.get("edatee")
        venid = request.POST.get("vid")
        images = request.FILES.getlist("images")  # This will be empty if no images are uploaded
    except KeyError:
        return sendResponse(request, 4001, [], action)

    try:
        myConn = connectDB()
        cursor = myConn.cursor()

        # Update event table with the new event details
        cursor.execute("""
            UPDATE event 
            SET name = %s, description = %s, start_time = %s, end_time = %s, venue = %s
            WHERE eventid = %s
        """, [ename, edesc, edateb, edatee, venid, eventid])

        # Only update images if new ones were provided
        if images:
            # Delete old image records and optionally files (if needed)
            cursor.execute("SELECT image_path FROM event_images WHERE eventid = %s", [eventid])
            old_images = cursor.fetchall()

            for img_path_tuple in old_images:
                img_path = img_path_tuple[0]
                if os.path.exists(img_path):
                    os.remove(img_path)  # Delete file from the filesystem
            cursor.execute("DELETE FROM event_images WHERE eventid = %s", [eventid])

            # Insert new images
            for image in images:
                filename = f"{int(timezone.now().timestamp())}_{image.name}"
                image_dir = os.path.join('media', 'events')
                os.makedirs(image_dir, exist_ok=True)
                filepath = os.path.join(image_dir, filename)

                with open(filepath, 'wb+') as f:
                    for chunk in image.chunks():
                        f.write(chunk)

                cursor.execute("""
                    INSERT INTO event_images (eventid, image_path)
                    VALUES (%s, %s)
                """, [eventid, filepath])

        # Handle removed images (if any)
        removed_images = request.FILES.get("removed_images") or request.POST.get("removed_images")

        if removed_images:
            removed_list = json.loads(removed_images)
            for img_path in removed_list:
                full_path = os.path.join(settings.MEDIA_ROOT, img_path.replace("/media/", ""))
                if os.path.exists(full_path):
                    os.remove(full_path)

        myConn.commit()
        cursor.close()
        resp = sendResponse(request, 200, {"eventid": eventid}, action)

    except Exception as e:
        print(f"Error editing event: {e}")
        resp = sendResponse(request, 5001, [], action)
    finally:
        disconnectDB(myConn)
        return resp
def get_seats(data):
    eventid = data.get("eventid")
    if not eventid:
        return JsonResponse({"error": "Missing eventid"}, status=400)

    with connection.cursor() as cursor:
        cursor.execute("SELECT ticketid, seat, price, booked FROM ticket WHERE eventid = %s", [eventid])
        rows = cursor.fetchall()

    seats = [
        {"ticketid": r[0], "seat": r[1], "price": float(r[2]), "booked": r[3]}
        for r in rows
    ]
    return JsonResponse({"seats": seats})
