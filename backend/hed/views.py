# Create your views here.
from django.http.response import JsonResponse
from django.shortcuts import render
from datetime import datetime
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from backend.settings import sendMail, sendResponse ,disconnectDB, connectDB, resultMessages,generateStr

def dt_gettime(request):
    jsons = json.loads(request.body)
    action = jsons["action"]
    d1 = datetime.now()
    respdata = [{'time':d1.strftime("%Y/%m/%d, %H:%M:%S")}]  
    resp = sendResponse(request, 200, respdata, action)
    return resp
def dt_login(request):
    jsons = json.loads(request.body)
    action = jsons['action']
    try:
        gmail = jsons['gmail'].lower()
        password = jsons['password']
    except: 
        action = jsons['action']
        respdata = []
        resp = sendResponse(request, 3006, respdata, action) 
        return resp
    try: 
        myConn = connectDB()
        cursor = myConn.cursor()
        query = F"""SELECT COUNT(*) AS usercount, MIN(username) AS username 
                FROM users
                WHERE gmail = '{gmail}' 
                AND is_verified = True 
                AND password = '{password}' 
                AND is_banned = False """ 
        cursor.execute(query)
        columns = cursor.description
        respRow = [{columns[index][0]:column for index, 
            column in enumerate(value)} for value in cursor.fetchall()]
        print(respRow)
        cursor.close()
        if respRow[0]['usercount'] == 1:
            cursor1 = myConn.cursor() 
            query = F"""SELECT uid, gmail, last_login, username
                    FROM users 
                    WHERE gmail = '{gmail}' AND is_verified = True AND password = '{password}'"""
            cursor1.execute(query)
            columns = cursor1.description
            respRow = [{columns[index][0]:column for index, 
                column in enumerate(value)} for value in cursor1.fetchall()]
            uid = respRow[0]['uid'] 
            gmail = respRow[0]['gmail'] 
            lname = respRow[0]['username']
            last_login = respRow[0]['last_login']
            respdata = [{'uid': uid,'gmail':gmail, 'username':lname, 'last_login':last_login}] 
            resp = sendResponse(request, 1002, respdata, action)
            query = F"""UPDATE users 
                    SET last_login = NOW()
                    WHERE gmail = '{gmail}' AND is_verified = True AND password = '{password}'"""
            cursor1.execute(query) 
            myConn.commit()
            cursor1.close()
        else: 
            data = [{'gmail':gmail}] 
            resp = sendResponse(request, 1004, data, action)
    except:
        action = jsons["action"]
        respdata = []
        resp = sendResponse(request, 5001, respdata, action) 
    finally:
        disconnectDB(myConn) 
        return resp
def dt_register(request):
    jsons = json.loads(request.body)
    action = jsons["action"]
    try :
        gmail = jsons["gmail"].lower()
        username = jsons["username"].capitalize()
        password = jsons["password"]
    except:
        action = jsons['action']
        respdata = []
        resp = sendResponse(request, 3007, respdata, action)
        return resp
    
    try:
        conn = connectDB()
        cursor = conn.cursor()
        query = F"SELECT COUNT(*) AS usercount FROM users WHERE gmail = '{gmail}' AND is_verified = True"
        cursor.execute(query) 
        columns = cursor.description #
        respRow = [{columns[index][0]:column for index, 
            column in enumerate(value)} for value in cursor.fetchall()] 
        print(respRow)
        cursor.close()
        if respRow[0]["usercount"] == 0:
            cursor1 = conn.cursor()
            query = F"""INSERT INTO users(gmail, username, password, is_verified, is_banned, create_date, last_login) 
                        VALUES('{gmail}','{username}', '{password}',
                        False, False, NOW(), '1970-01-01') 
            RETURNING uid"""
            print(query)
            cursor1.execute(query)
            uid = cursor1.fetchone()[0]
            print(uid, "uid")
            conn.commit() 
            token = generateStr(20) 
            query = F"""INSERT INTO t_token(uid, token, token_type, end_date, create_date) VALUES({uid}, '{token}', 'register', NOW() + interval \'1 day\', NOW() )""" # Inserting t_token
            print(query)
            cursor1.execute(query)
            conn.commit()
            cursor1.close()
            
            subject = "User burtgel batalgaajuulah mail"
            bodyHTML = F"""<a target='_blank' href='http://localhost:8000/user/?token={token}'>CLICK ME to acivate your account</a>"""
            sendMail(gmail,subject,bodyHTML)
            action = jsons['action']
            respdata = [{"gmail":gmail,"username":username}]
            resp = sendResponse(request, 200, respdata, action)
        else:
            action = jsons['action']
            respdata = [{"gmail":gmail, "username":username}]
            resp = sendResponse(request, 3008, respdata, action)
    except (Exception) as e:
        action = jsons["action"]
        respdata = [{"aldaa":str(e)}] 
        resp = sendResponse(request, 5002, respdata, action)
    finally:
        disconnectDB(conn)
        return resp
def dt_activate(request):
    try:
        jsons = json.loads(request.body)
        uid = jsons.get("uid")
        token = jsons.get("token")
        if not all([uid, token]):
            return sendResponse(request, 4000, [], "activate")
        conn = connectDB()
        cursor = conn.cursor()
        query = f"""
        SELECT token, end_date FROM t_token 
        WHERE uid = {uid} AND token = '{token}' AND token_type = 'register'
        """
        cursor.execute(query)
        token_data = cursor.fetchone()
        cursor.close()
        if not token_data or token_data[1] < datetime.now().date():
            return sendResponse(request, 4001, [], "activate")
        cursor1 = conn.cursor()
        query = f"UPDATE users SET is_verified = True WHERE uid = {uid}"
        cursor1.execute(query)
        conn.commit()
        query = f"DELETE FROM t_token WHERE uid = {uid} AND token = '{token}'"
        cursor1.execute(query)
        conn.commit()
        cursor1.close()
        return sendResponse(request, 200, [], "activate")
    except Exception as e:
        return sendResponse(request, 5002, [{"error": str(e)}], "activate")
    finally:
        disconnectDB(conn)


def dt_forgot(request):
    jsons = json.loads(request.body)
    action = jsons['action']
    resp = {}
    try:
        gmail = jsons['gmail'].lower() 
    except: 
        action = jsons['action']
        respdata = []
        resp = sendResponse(request, 3016, respdata, action)
        return resp
    
    try: 
        myConn = connectDB()
        cursor = myConn.cursor()
        query = f"""SELECT COUNT(*) AS usercount, MIN(gmail) AS gmail , MIN(uid) AS uid
                    FROM users
                    WHERE gmail = '{gmail}' AND is_verified = True"""
        cursor.execute(query)
        cursor.description
        columns = cursor.description 
        respRow = [{columns[index][0]:column for index, 
            column in enumerate(value)} for value in cursor.fetchall()] 
        if respRow[0]['usercount'] == 1:
            uid = respRow[0]['uid']
            gmail = respRow[0]['gmail']
            token = generateStr(25) 
            query = F"""INSERT INTO t_token(uid, token, token_type, end_date, create_date) 
            VALUES({uid}, '{token}', 'forgot', NOW() + interval \'1 day\', NOW() )"""
            cursor.execute(query)
            myConn.commit()
            subject = "Nuuts ug shinechleh"
            body = f"<a href='http://localhost:3000/verified/?token={token}'>Martsan nuuts ugee shinechleh link</a>"
            sendMail(gmail, subject, body)
            action = jsons['action']
            respdata = [{"gmail":gmail}]
            resp = sendResponse(request,3012,respdata,action )
        else:
            action = jsons['action']
            respdata = [{"gmail":gmail}]
            resp = sendResponse(request,3013,respdata,action )
    except Exception as e:
        action = jsons["action"]
        respdata = [{"error":str(e)}]
        resp = sendResponse(request, 5003, respdata, action) 
    finally:
        cursor.close()
        disconnectDB(myConn)
        return resp
def dt_resetpassword(request):
    jsons = json.loads(request.body) 
    action = jsons['action'] 
    resp = {}
    try:
        newpass = jsons['newpass'] 
        token = jsons['token'] 
    except: 
        action = jsons['action']
        respdata = []
        resp = sendResponse(request, 3018, respdata, action)
        return resp
    
    try: 
        myConn = connectDB() 
        cursor = myConn.cursor() 
        query = f"""SELECT COUNT (users.uid) AS usercount
                , MIN(gmail) AS gmail
                , MAX(users.uid) AS uid
                , MAX(t_token.tid) AS tid
                FROM users INNER JOIN t_token
                ON users.uid = t_token.uid
                WHERE t_token.token = '{token}'
                AND users.is_verified = True
                AND t_token.end_date > NOW()"""
        cursor.execute(query)
        columns = cursor.description 
        respRow = [{columns[index][0]:column for index, 
            column in enumerate(value)} for value in cursor.fetchall()] 
        if respRow[0]['usercount'] == 1:
            uid = respRow[0]['uid']
            gmail = respRow[0]['gmail']
            tid = respRow[0] ['tid'] 
            token = generateStr(40)
            query = F"""UPDATE users SET password = '{newpass}'
                        WHERE users.uid = {uid}"""
            cursor.execute(query)
            myConn.commit()
            
            query = F"""UPDATE t_token 
                SET token = '{token}'
                , end_date = '1970-01-01' 
                WHERE tid = {tid}""" 
            cursor.execute(query)
            myConn.commit()             
            action = jsons['action']
            respdata = [{"gmail":gmail}]
            resp = sendResponse(request,3019,respdata,action )
        else:
            action = jsons['action']
            respdata = []
            resp = sendResponse(request,3020,respdata,action )
    except Exception as e:
        action = jsons["action"]
        respdata = [{"error":str(e)}] 
        resp = sendResponse(request, 5005, respdata, action) 
    finally:
        cursor.close()
        disconnectDB(myConn)
        return resp
def dt_changepassword(request):
    jsons = json.loads(request.body) 
    action = jsons['action'] 
    resp = {}
    
    try:
        gmail = jsons['gmail'].lower() # get gmail key from jsons
        newpass = jsons['newpass'] # get newpass key from jsons
        oldpass = jsons['oldpass'] # get oldpass key from jsons
    except: # gmail, newpass, oldpass key ali neg ni baihgui bol aldaanii medeelel butsaana
        action = jsons['action']
        respdata = []
        resp = sendResponse(request, 3021, respdata, action) # response beldej baina. 6 keytei.
        return resp
    
    try: 
        myConn = connectDB()
        cursor = myConn.cursor() 
        query = f"""SELECT COUNT(uid) AS usercount ,MAX(uid) AS uid
                    ,MIN(gmail) AS gmail
                    ,MAX (username) AS fname
                    FROM users
                    WHERE gmail='{gmail}'  
                    AND is_verified=true
                    AND password='{oldpass}'"""
        cursor.execute(query) # executing query
        columns = cursor.description #
        respRow = [{columns[index][0]:column for index, 
            column in enumerate(value)} for value in cursor.fetchall()] 
        if respRow[0]['usercount'] == 1: 
            uid = respRow[0]['uid']
            gmail = respRow[0]['gmail']
            fname = respRow[0]['fname']
            
            query = F"""UPDATE users SET password='{newpass}'
                        WHERE uid={uid}""" # Updating user's new password using uid in users
            cursor.execute(query) # executing query
            myConn.commit() # saving DB
            
            # sending Response
            action = jsons['action']
            respdata = [{"gmail":gmail, "username":fname}]
            resp = sendResponse(request, 3022, respdata, action )
            
        else: # old password not match
            action = jsons['action']
            respdata = [{"gmail":gmail}]
            resp = sendResponse(request, 3023, respdata, action )
            
    except Exception as e: # change password service deer dotood aldaa garsan bol ajillana.
        # change service deer aldaa garval ajillana. 
        action = jsons["action"]
        respdata = [{"error":str(e)}] # hooson data bustaana.
        resp = sendResponse(request, 5006, respdata, action) # standartiin daguu 6 key-tei response butsaana
    finally:
        cursor.close() # close the cursor. ALWAYS
        disconnectDB(myConn) # yamarch uyd database holbolt uussen bol holboltiig salgana. Uchir ni finally dotor baigaa
        return resp # response bustaaj baina
# dt_changepassword

@csrf_exempt # method POST uyd ajilluulah csrf
def checkService(request): # hamgiin ehend duudagdah request shalgah service
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
        
        # request-n action ni gettime
        if action == "gettime":
            result = dt_gettime(request)
            return JsonResponse(result)
        # request-n action ni login bol ajillana
        elif action == "login":
            result = dt_login(request)
            return JsonResponse(result)
        # request-n action ni register bol ajillana
        elif action == "register":
            result = dt_register(request)
            return JsonResponse(result)
        # request-n action ni forgot bol ajillana
        elif action == "forgot":
            result = dt_forgot(request)
            return JsonResponse(result)
        #requestiin action resetpassword-r ajillna
        elif action == "resetpassword":
            result = dt_resetpassword(request)
            return JsonResponse(result)
        #requestiin action changepassword-r ajillna
        elif action == "changepassword":
            result = dt_changepassword(request)
            return JsonResponse(result)
        elif action == "verify":
            result = dt_activate(request)
            return JsonResponse(result)
        else:
            action = "no action"
            respdata = []
            resp = sendResponse(request, 3001, respdata, action)
            return JsonResponse(resp)
    elif request.method == "GET":
        token = request.GET.get('token') # token parameteriin utgiig avch baina.
        
        if (token is None):
            action = "no action" 
            respdata = []  # response-n data-g beldej baina. list turultei baih
            resp = sendResponse(request, 3015, respdata, action)
            return JsonResponse(resp)
            # response beldej baina. 6 keytei.
            
            
        try: 
            conn = connectDB() # database holbolt uusgej baina
            cursor = conn.cursor() # cursor uusgej baina
            
            # gadnaas orj irsen token-r mur songoj toolj baina. Tuhain token ni idevhtei baigaag mun shalgaj baina.
            query = F"""
                    SELECT COUNT(*) AS tokencount
                        , MIN(tid) AS tid
                        , MAX(uid) AS uid
                        , MIN(token) token
                        , MAX(token_type) token_type
                    FROM t_token 
                    WHERE token = '{token}' 
                            AND end_date > NOW()"""
            # print (query)
            cursor.execute(query) # executing query
            # print(cursor.description)
            columns = cursor.description #
            respRow = [{columns[index][0]:column for index, 
                column in enumerate(value)} for value in cursor.fetchall()] # respRow is list and elements are dictionary. dictionary structure is columnName : value
            # print(respRow)
            uid = respRow[0]["uid"]
            token_type = respRow[0]["token_type"]
            tid = respRow[0]["tid"]
            
            if respRow[0]["tokencount"] == 1: # Hervee hargalzah token oldson baival ajillana.
                #token_type ni 3 turultei. (register, forgot, login) 
                # End register, forgot hoyriig shagaj uzehed hangalttai. Uchir ni login type ni GET method-r hezee ch orj irehgui.
                if token_type == "register": # Hervee token_type ni register bol ajillana.
                    query = f"""SELECT gmail, username, create_date 
                            FROM users
                            WHERE uid = {uid}""" # Tuhain neg hunii medeelliig avch baina.
                    cursor.execute(query) # executing query
                    
                    columns = cursor.description #
                    respRow = [{columns[index][0]:column for index, 
                        column in enumerate(value)} for value in cursor.fetchall()]
                    gmail = respRow[0]['gmail']
                    username = respRow[0]['username']
                    create_date = respRow[0]['create_date']
                    
                    # Umnu gmail-r verified bolson hereglegch baival tuhain gmail-r dahin verified bolgoj bolohgui. Iimees umnu verified hereglegch oldoh yosgui. 
                    query  = f"""SELECT COUNT(*) AS verifiedusercount 
                                , MIN(gmail) AS gmail
                            FROM users 
                            WHERE gmail = '{gmail}' AND is_verified = True"""
                    cursor.execute(query) # executing query
                    columns = cursor.description #
                    respRow = [{columns[index][0]:column for index, 
                        column in enumerate(value)} for value in cursor.fetchall()]
                    
                    if respRow[0]['verifiedusercount'] == 0:
                        
                        # verified user oldoogui tul hereglegchiin verified bolgono.
                        query = f"UPDATE users SET is_verified = true WHERE uid = {uid}"
                        cursor.execute(query) # executing query
                        conn.commit() # saving database
                        
                        token = generateStr(30) # huuchin token-oo uurchluh token uusgej baina
                        # huuchin token-g idevhgui bolgoj baina.
                        query = f"""UPDATE t_token SET token = '{token}', 
                                    end_date = '1970-01-01' WHERE tid = {tid}"""
                        cursor.execute(query) # executing query
                        conn.commit() # saving database
                        
                        # token verified service-n response
                        action = "userverified"
                        respdata = [{"uid":uid,"gmail":gmail, "username":username,
                                    "token_type":token_type
                                    , "create_date":create_date}]
                        resp = sendResponse(request, 3010, respdata, action) # response beldej baina. 6 keytei.
                    else: # user verified already. User verify his or her mail verifying again. send Response. No change in Database.
                        action = "user verified already"
                        respdata = [{"gmail":gmail,"token_type":token_type}]
                        resp = sendResponse(request, 3014, respdata, action) # response beldej baina. 6 keytei.
                elif token_type == "forgot": # Hervee token_type ni forgot password bol ajillana.
                    
                    query = f"""SELECT gmail, username, create_date FROM users
                            WHERE uid = {uid} AND is_verified = True""" # Tuhain neg hunii medeelliig avch baina.
                    cursor.execute(query) # executing query
                    columns = cursor.description #
                    respRow = [{columns[index][0]:column for index, 
                        column in enumerate(value)} for value in cursor.fetchall()]
                    
                    gmail = respRow[0]['gmail']
                    username = respRow[0]['username']
                    create_date = respRow[0]['create_date']
                    
                    # forgot password check token response
                    action = "forgot user verify"
                    respdata = [{"uid":uid,"gmail":gmail,  "token_type":token_type
                                , "create_date":create_date}]
                    resp = sendResponse(request, 3011, respdata, action) # response beldej baina. 6 keytei.
                else:
                    # token-ii turul ni forgot, register ali ali ni bish bol buruu duudagdsan gej uzne.
                    # login-ii token GET-r duudagdahgui. 
                    action = "no action"
                    respdata = []
                    resp = sendResponse(request, 3017, respdata, action) # response beldej baina. 6 keytei.
                
            else: # Hervee hargalzah token oldoogui bol ajillana.
                # token buruu esvel hugatsaa duussan . Send Response
                action = "notoken" 
                respdata = []
                resp = sendResponse(request, 3009, respdata, action) # response beldej baina. 6 keytei.
                
        except:
            # GET method dotood aldaa
            action = "no action" 
            respdata = []  # response-n data-g beldej baina. list turultei baih
            resp = sendResponse(request, 5004, respdata, action)
            # response beldej baina. 6 keytei.
        finally:
            cursor.close()
            disconnectDB(conn)
            return JsonResponse(resp)
    
    # Method ni POST, GET ali ali ni bish bol ajillana
    else:
        #GET, POST-s busad uyd ajillana
        action = "no action"
        respdata = []
        resp = sendResponse(request, 3002, respdata, action)
        return JsonResponse(resp) 