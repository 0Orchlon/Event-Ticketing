import os
import smtplib
from django.http.response import JsonResponse
from django.shortcuts import render
from datetime import datetime, timezone
import json
from django.views.decorators.csrf import csrf_exempt
from backend.settings import sendMail, sendResponse, disconnectDB, connectDB, resultMessages, generateStr
import qrcode
import base64
from io import BytesIO
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from django.core.files.storage import default_storage
from django.contrib.auth.hashers import make_password
from django.db import connection
from django.core.files.base import ContentFile

# Generate QR code
def generate_qr_code(data: str) -> BytesIO:
    qr = qrcode.make(data)
    buffer = BytesIO()
    qr.save(buffer, format="PNG")
    buffer.seek(0)
    return buffer  # return raw bytes

# Send Ticket Email with QR code
def send_ticket_email(to_email: str, subject: str, body_text: str, qr_img_bytes: BytesIO):
    msg = MIMEMultipart('related')
    msg['To'] = to_email
    msg['From'] = "testmail@mandakh.edu.mn"
    msg['Subject'] = subject

    # Create the HTML content with CID reference
    bodyHTML = f"""
    <html>
        <body>
            <p>{body_text}</p>
            <p>Here is your ticket QR code:</p>
            <img src="cid:ticketqr">
        </body>
    </html>
    """
    msg.attach(MIMEText(bodyHTML, 'html'))

    # Attach the image with CID
    qr_img_bytes.seek(0)
    image = MIMEImage(qr_img_bytes.read(), name="ticket.png")
    image.add_header('Content-ID', '<ticketqr>')
    msg.attach(image)

    # Send email
    sendMail(to_email, subject, msg.as_string())

# Create Event

def dt_create_event(request):
    action = request.POST.get("action")

    try:
        ename = request.POST.get("ename")
        edesc = request.POST.get("edesc")
        edateb = request.POST.get("edateb")
        edatee = request.POST.get("edatee")
        venid = request.POST.get("vid")
        image = request.FILES.get("image")
    except KeyError:
        return sendResponse(request, 3027, [], action)

    try:
        myConn = connectDB()
        cursor = myConn.cursor()

        query = """
            INSERT INTO events (name, description, start_time, end_time, venueid, created_at, updated_at)
            VALUES (%s, %s, %s, %s, %s, NOW(), NOW()) 
            RETURNING eventid;
        """
        cursor.execute(query, [ename, edesc, edateb, edatee, venid])
        event_id = cursor.fetchone()[0]

        if image:
            filename = f"{int(timezone.now().timestamp())}_{image.name}"
            image_dir = os.path.join('media', 'events')
            os.makedirs(image_dir, exist_ok=True)
            filepath = os.path.join(image_dir, filename)
            with open(filepath, 'wb+') as f:
                for chunk in image.chunks():
                    f.write(chunk)

            with connection.cursor() as img_cursor:
                img_cursor.execute("INSERT INTO imgz (eid, imgpath) VALUES (%s, %s)",
                    [event_id, filepath]
                )

        myConn.commit()
        resp = sendResponse(request, 200, {'eventid': event_id}, action)
        cursor.close()

    except Exception as e:
        print(f"Error creating event: {e}")
        resp = sendResponse(request, 5000, [], action)
    finally:
        disconnectDB(myConn)
        return resp

# Add Ticket Types
def dt_seats(request):
    jsons = json.loads(request.body)
    action = jsons.get("action")

    try:
        eid = jsons['eid']
        stype = jsons['stype']
        price = jsons['price']
        seat = jsons['seat']
    except KeyError:
        respdata = []
        resp = sendResponse(request, 3006, respdata, action)
        return resp

    try:
        myConn = connectDB()
        cursor = myConn.cursor()
        query = f"""
        INSERT INTO tickettypes (eventid, typename, price, quantityavailable, availableseat)
        VALUES ({eid}, '{stype}', {price}, {seat}, {seat}) 
        RETURNING tickettypeid;
        """
        cursor.execute(query)
        columns = cursor.description
        respRow = [{columns[index][0]: column for index, column in enumerate(value)} for value in cursor.fetchall()]
        myConn.commit()
        resp = sendResponse(request, 200, respRow, action)
        cursor.close()
    except Exception as e:
        respdata = []
        resp = sendResponse(request, 5000, respdata, action)
        print(f"Error adding ticket type: {e}")
    finally:
        disconnectDB(myConn)
        return resp

# Handle Event Booking
def dt_booking(request):
    jsons = json.loads(request.body)
    action = jsons.get("action")

    try:
        uid = jsons["uid"]
        ttype = jsons["ttype"]
        quantity = jsons["quantity"]
        tprice = jsons["tprice"]
        status = jsons["status"]
    except KeyError:
        respdata = []
        resp = sendResponse(request, 3006, respdata, action)
        return resp

    try:
        # Connect to the database
        myConn = connectDB()
        cursor = myConn.cursor()

        # Insert booking details into the bookings table
        query = f"""
        INSERT INTO bookings (userid, tickettypeid, quantity, totalprice, status, bookingdate)
        VALUES ({uid}, {ttype}, {quantity}, {tprice}, '{status}', NOW()) 
        RETURNING bookingid;
        """
        cursor.execute(query)
        booking_id = cursor.fetchone()[0]

        myConn.commit()

        # Fetch the user email to send the ticket email
        cursor.execute("""
            SELECT email FROM users WHERE userid = %s
        """, [uid])
        user_email = cursor.fetchone()[0]

        if user_email:
            # Generate the ticket QR code (for simplicity, we use the booking ID as the data)
            qr_data = f"Booking ID: {booking_id}, Ticket Type: {ttype}, Quantity: {quantity}"
            qr_img_bytes = generate_qr_code(qr_data)

            # Prepare the email body and send the ticket email
            email_subject = f"Your Event Ticket - Booking ID: {booking_id}"
            email_body = f"Thank you for your booking! Here is your ticket for the event. Your booking ID is {booking_id}."
            send_ticket_email(user_email, email_subject, email_body, qr_img_bytes)

        # Prepare the response data
        columns = cursor.description
        respRow = [{columns[index][0]: column for index, column in enumerate(value)} for value in cursor.fetchall()]
        resp = sendResponse(request, 200, respRow, action)

        cursor.close()

    except Exception as e:
        respdata = []
        resp = sendResponse(request, 5000, respdata, action)
        print(f"Error processing booking: {e}")
    finally:
        disconnectDB(myConn)
        return resp

# Add Payment Method
def dt_paymethod(request):
    jsons = json.loads(request.body)
    action = jsons.get("action")

    try:
        uid = jsons["uid"]
        provider = jsons["provider"]
        token = jsons["token"]
    except KeyError:
        respdata = []
        resp = sendResponse(request, 3006, respdata, action)
        return resp

    try:
        myConn = connectDB()
        cursor = myConn.cursor()
        query = f"""
        INSERT INTO paymentmethods (userid, provider, token, createdate)
        VALUES ({uid}, {provider}, {token}, NOW()) 
        RETURNING tickettypeid;
        """
        cursor.execute(query)
        columns = cursor.description
        respRow = [{columns[index][0]: column for index, column in enumerate(value)} for value in cursor.fetchall()]
        myConn.commit()
        resp = sendResponse(request, 200, respRow, action)
        cursor.close()
    except Exception as e:
        respdata = []
        resp = sendResponse(request, 5000, respdata, action)
        print(f"Error processing payment method: {e}")
    finally:
        disconnectDB(myConn)
        return resp

# Handle Seat Availability
def dt_avialable_seats(request):
    jsons = json.loads(request.body)
    action = jsons.get("action")

    try:
        tid = jsons["tid"]
    except KeyError:
        respdata = []
        resp = sendResponse(request, 3006, respdata, action)
        return resp

    try:
        myConn = connectDB()
        cursor = myConn.cursor()
        query = f"""
        SELECT tickettypeid, availableseat 
        FROM tickettypes
        WHERE tickettypeid = {tid}
        """
        cursor.execute(query)
        columns = cursor.description
        respRow = [{columns[index][0]: column for index, column in enumerate(value)} for value in cursor.fetchall()]
        myConn.commit()
        if cursor.rowcount == 0:
            resp = sendResponse(request, 201, [], action)
        else:
            resp = sendResponse(request, 200, respRow, action)
        cursor.close()
    except Exception as e:
        respdata = []
        resp = sendResponse(request, 5000, respdata, action)
        print(f"Error fetching available seats: {e}")
    finally:
        disconnectDB(myConn)
        return resp

# Create Admin
@csrf_exempt
def create_admin(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = data["username"]
        email = data["email"]
        password = data["password"]

        hashed = make_password(password)

        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO users (username, email, password, is_admin)
                VALUES (%s, %s, %s, %s)
            """, [username, email, hashed, 1])

        return JsonResponse({"message": "Admin user created successfully."})

# Event Service
@csrf_exempt
def EventService(request):
    if request.method == "POST":
        try:
            jsons = json.loads(request.body)
        except:
            respdata = []
            resp = sendResponse(request, 3003, respdata)
            return JsonResponse(resp)

        action = jsons.get("action", "no action")
        
        if action == "addevent":
            result = dt_create_event(request)
            return JsonResponse(result)
        elif action == "addeventseats":
            result = dt_seats(request)
            return JsonResponse(result)
        elif action == "bookingticket":
            result = dt_booking(request)
            return JsonResponse(result)
        elif action == "addpaymethod":
            result = dt_paymethod(request)
            return JsonResponse(result)
        elif action == "availableseat":
            result = dt_avialable_seats(request)
            return JsonResponse(result)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})
