from django.http.response import JsonResponse
from django.shortcuts import render
from datetime import datetime
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from backend.settings import sendMail, sendResponse ,disconnectDB, connectDB, resultMessages,generateStr

def dt_create_event(request):
    jsons =json.loads(request.body)
    action = jsons["action"]
    
    try:
        ename = jsons['ename'] # event name
        edesc = jsons['edesc'] # event descripsion
        edateb = jsons['edateb'] # event start date
        edatee = jsons['edatee'] # event end date
        venid = jsons['vid'] # venue id

    except: # key ali neg ni baihgui bol aldaanii medeelel butsaana
        action = jsons['action']
        respdata = []
        resp = sendResponse(request, 3027, respdata, action) # response beldej baina. 6 keytei.
        return resp
    
    try: 
        myConn = connectDB() # database holbolt uusgej baina
        cursor = myConn.cursor() # cursor uusgej baina
        
        # Hereglegchiin ner, password-r nevtreh erhtei (is_verified=True) hereglegch login hiij baigaag toolj baina.
        query = F"""INSERT INTO events (name, description, start_time, end_time, venueid, created_at, updated_at)
                    VALUES (
                    '{ename}', 
                    '{edesc}',
                    '{edateb}',
                    '{edatee}',
                    {venid},
                    NOW(),
                    NOW()
                )
                RETURNING eventid;""" 
        #print(query)
        cursor.execute(query) # executing query
        columns = cursor.description #
        respRow = [{columns[index][0]:column for index, 
            column in enumerate(value)} for value in cursor.fetchall()] # respRow is list and elements are dictionary. dictionary structure is columnName : value
        print(respRow)
        myConn.commit()
        resp = sendResponse(request, 200, respRow[0], action)
        cursor.close() # close the cursor. ALWAYS
    except:
        # login service deer aldaa garval ajillana. 
        action = jsons["action"]
        respdata = [] # hooson data bustaana.
        resp = sendResponse(request, 5000, respdata, action) # standartiin daguu 6 key-tei response butsaana
        
    finally:
        disconnectDB(myConn) # yamarch uyd database holbolt uussen bol holboltiig salgana. Uchir ni finally dotor baigaa
        return resp # response bustaaj baina

# Events үүсгэх ба суудлын тоо

def dt_seats(request):
    jsons =json.loads(request.body)
    action = jsons["action"]
    try:
        eid = jsons['eid'] # event id
        stype = jsons['stype'] # ticket name
        price = jsons['price'] # ticket price
        seat = jsons['seat'] # total number of seat

    except: # key ali neg ni baihgui bol aldaanii medeelel butsaana
        action = jsons['action']
        respdata = []
        resp = sendResponse(request, 3006, respdata, action) # response beldej baina. 6 keytei.
        return resp
    
    try: 
        myConn = connectDB() # database holbolt uusgej baina
        cursor = myConn.cursor() # cursor uusgej baina
        query = F"""INSERT INTO tickettypes (eventid, typename, price, quantityavailable, availableseat)
                    VALUES 
                    ({eid}, '{stype}', {price}, {seat},{seat})
                    RETURNING tickettypeid;""" 
        #print(query)
        cursor.execute(query) # executing query
        columns = cursor.description
        respRow = [{columns[index][0]: column for index, column in enumerate(value)} for value in cursor.fetchall()]
        myConn.commit()
        resp = sendResponse(request, 200, respRow, action)
        cursor.close() # close the cursor. ALWAYS
    except:
        action = jsons["action"]
        respdata = [] # hooson data bustaana.
        resp = sendResponse(request, 5000, respdata, action) # standartiin daguu 6 key-tei response butsaana
        
    finally:
        disconnectDB(myConn) # yamarch uyd database holbolt uussen bol holboltiig salgana. Uchir ni finally dotor baigaa
        return resp # response bustaaj baina

def dt_booking(request):
    jsons =json.loads(request.body)
    action = jsons["action"]
    try:
        uid = "uid"
        ttype = "ttype"
        quantity = "quantity"
        tprice = "tprice"
        status = "status"
    
    except: # key ali neg ni baihgui bol aldaanii medeelel butsaana
        action = jsons['action']
        respdata = []
        resp = sendResponse(request, 3006, respdata, action) # response beldej baina. 6 keytei.
        return resp
    
    try: 
        myConn = connectDB() # database holbolt uusgej baina
        cursor = myConn.cursor() # cursor uusgej baina
        query = F"""INSERT INTO bookings (userid, tickettypeid, quantity, totalprice, status, bookingdate)
        VALUES 
        ({uid},
        {ttype},
        {quantity},
        {tprice},
        '{status}',
        NOW())
        RETURNING tickettypeid;""" 
        #print(query)
        cursor.execute(query) # executing query
        columns = cursor.description
        respRow = [{columns[index][0]: column for index, column in enumerate(value)} for value in cursor.fetchall()]
        myConn.commit()
        resp = sendResponse(request, 200, respRow, action)
        cursor.close() # close the cursor. ALWAYS
    except:
        action = jsons["action"]
        respdata = [] # hooson data bustaana.
        resp = sendResponse(request, 5000, respdata, action) # standartiin daguu 6 key-tei response butsaana
        
    finally:
        disconnectDB(myConn) # yamarch uyd database holbolt uussen bol holboltiig salgana. Uchir ni finally dotor baigaa
        return resp # response bustaaj baina

def dt_paymethod(request):
    jsons =json.loads(request.body)
    action = jsons["action"]
    try:
        uid = jsons["uid"]
        provider = jsons["provider"]
        token = jsons["token"]
    
    except: # key ali neg ni baihgui bol aldaanii medeelel butsaana
        action = jsons['action']
        respdata = []
        resp = sendResponse(request, 3006, respdata, action) # response beldej baina. 6 keytei.
        return resp
    
    try: 
        myConn = connectDB() # database holbolt uusgej baina
        cursor = myConn.cursor() # cursor uusgej baina
        query = F"""INSERT INTO paymentmethods (userid, provider, token, createdate)
        VALUES 
        ({uid},
        {provider},
        {token},
        NOW())
        RETURNING tickettypeid;""" 
        #print(query)
        cursor.execute(query) # executing query
        columns = cursor.description
        respRow = [{columns[index][0]: column for index, column in enumerate(value)} for value in cursor.fetchall()]
        myConn.commit()
        resp = sendResponse(request, 200, respRow, action)
        cursor.close() # close the cursor. ALWAYS
    except:
        action = jsons["action"]
        respdata = [] # hooson data bustaana.
        resp = sendResponse(request, 5000, respdata, action) # standartiin daguu 6 key-tei response butsaana
        
    finally:
        disconnectDB(myConn) # yamarch uyd database holbolt uussen bol holboltiig salgana. Uchir ni finally dotor baigaa
        return resp # response bustaaj baina

def dt_add(request):
    jsons =json.loads(request.body)
    action = jsons["action"]
    try:
        tid = jsons["tid"]
    
    except: # key ali neg ni baihgui bol aldaanii medeelel butsaana
        action = jsons['action']
        respdata = []
        resp = sendResponse(request, 3006, respdata, action) # response beldej baina. 6 keytei.
        return resp
    
    try: 
        myConn = connectDB() # database holbolt uusgej baina
        cursor = myConn.cursor() # cursor uusgej baina
        query = F"""
UPDATE tickettypes 
SET availableseat = availableseat - 1 
WHERE tickettypeid = {tid} AND availableseat >= 1;
""" 
        #print(query)
        cursor.execute(query) # executing query
        myConn.commit()
        # respdata = []
        if cursor.rowcount == 0:
            resp = sendResponse(request, 201, [], action)
        else:
            resp = sendResponse(request, 200, [], action)
        # resp = sendResponse(request, 200, respdata, action)
        cursor.close() # close the cursor. ALWAYS
    except:
        action = jsons["action"]
        respdata = [] # hooson data bustaana.
        resp = sendResponse(request, 5000, respdata, action) # standartiin daguu 6 key-tei response butsaana
        
    finally:
        disconnectDB(myConn) # yamarch uyd database holbolt uussen bol holboltiig salgana. Uchir ni finally dotor baigaa
        return resp # response bustaaj baina


@csrf_exempt
def EventService(request):
    if request.method == "POST": # Method ni POST esehiig shalgaj baina
        try:
            # request body-g dictionary bolgon avch baina
            jsons = json.loads(request.body)
        except:
            # request body json bish bol aldaanii medeelel butsaana. 
            action = "no action"
            respdata = [] # hooson data bustaana.
            resp = sendResponse(request, 3003, respdata) # standartiin daguu 6 key-tei response butsaana
            return JsonResponse(resp) # response bustaaj baina
            
        try: 
            #jsons-s action-g salgaj avch baina
            action = jsons["action"]
        except:
            # request body-d action key baihgui bol aldaanii medeelel butsaana. 
            action = "no action"
            respdata = [] # hooson data bustaana.
            resp = sendResponse(request, 3005, respdata,action) # standartiin daguu 6 key-tei response butsaana
            return JsonResponse(resp)# response bustaaj baina
        
        if action == "addevent":
            result = dt_create_event(request)
            return JsonResponse(result)
        elif action == "seats":
            result = dt_seats(request)
            return JsonResponse(result)
        elif action == "booking":
            result = dt_booking(request)
            return JsonResponse(result)
        elif action == "paymethod":
            result = dt_paymethod(request)
            return JsonResponse(result)
        elif action == "buy":
            result = dt_add(request)
            return JsonResponse(result)
        else:
            action = "no action"
            respdata = []
            resp = sendResponse(request, 3001, respdata, action)
            return JsonResponse(resp)
    
    # Method ni POST bish bol ajillana
    else:
        #GET, POST-s busad uyd ajillana
        action = "no action"
        respdata = []
        resp = sendResponse(request, 3002, respdata, action)
        return JsonResponse(resp)