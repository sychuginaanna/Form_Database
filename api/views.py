from django.shortcuts import render
import MySQLdb
import json
from django.http import JsonResponse


db = MySQLdb.connect("localhost","root","annasychugina19945","myprojjj")
db.set_character_set('utf8')
dbc = db.cursor()
dbc.execute('SET Names utf8;')
dbc.execute('set character set utf8;')
dbc.execute('set character_set_connection=utf8;')
db.commit()



def clear(request):
    postRequest = None
    cursor = db.cursor()
    sqlanswer = "set FOREIGN_KEY_CHECKS = 0;"
    cursor.execute(sqlanswer)
    sqlanswer  = "TRUNCATE User;"
    cursor.execute(sqlanswer)
    sqlanswer  = "TRUNCATE Posts;"
    cursor.execute(sqlanswer)
    sqlanswer  = "TRUNCATE Follow;"
    cursor.execute(sqlanswer)
    sqlanswer  = "TRUNCATE Thread;"
    cursor.execute(sqlanswer)
    sqlanswer  = "TRUNCATE Forum;"
    cursor.execute(sqlanswer)
    sqlanswer  = "TRUNCATE Subscribe;"
    cursor.execute(sqlanswer)
    sqlanswer  = "set FOREIGN_KEY_CHECKS = 1;"
    cursor.execute(sqlanswer)
    db.commit()
    return JsonResponse({"code": 0, "response": "OK"})

def status(request):
    postRequest = None
    if request.method == "POST":
        postRequest = json.loads(request.body)
    cursor = db.cursor()
    sqlanswer = "select count(*) from User;"
    cursor.execute(sqlanswer)
    results = cursor.fetchall()
    for row in results:
        uamount = row[0]
    sqlanswer = "select count(*) from Thread;"
    cursor.execute(sqlanswer)
    results = cursor.fetchall()
    for row in results:
        tamount = row[0]
    sqlanswer = "select count(*) from Forum;"
    cursor.execute(sqlanswer)
    results = cursor.fetchall()
    for row in results:
        famount = row[0]
    sqlanswer = "select count(*) from Posts;"
    cursor.execute(sqlanswer)
    results = cursor.fetchall()
    for row in results:
        pamount = row[0]
    answer = {"user":uamount,
              "thread": tamount,
              "forum": famount,
              "post": pamount}
    return JsonResponse({"code": 0, "response": answer})

def gd(one, two):
    return dict(zip(one, two))

#user create
def createuser(request):
    postRequest = None
    if request.method == "POST":
        postRequest = json.loads(request.body)
    cursor = db.cursor()
    print json.dumps(postRequest['username'])
    print ""
    if postRequest['email'] is None:
        return JsonResponse({"code": 3, "response": "error message" }) 
    sqlanswer = "INSERT INTO User(username, about, isAnonymous, name, email) VALUES(" + json.dumps(postRequest['username']) + ", "
    sqlanswer += json.dumps(postRequest['about']) + ", "
    sqlanswer += str(postRequest.get('isAnonymous', 'False')) + ", "
    sqlanswer += json.dumps(postRequest['name']) + ", "
    sqlanswer += json.dumps(postRequest['email']) + ");"
    print sqlanswer
    try:
        cursor.execute(sqlanswer)
    except MySQLdb.IntegrityError:
        return JsonResponse({'code':5, 'response':'123132'})
    db.commit()      
    resp = "select * from User where id=" + str(cursor.lastrowid) + ";"
    cursor.execute(resp)
    results = cursor.fetchall()
    for row in results:
        about = row[0]
        email = row[1]
        id = row[2]
        isAnonymous = row[3]
        name = row[4]
        username = row[5]
    cursor.close()
    names = ["about", "email", "id", "isAnonymous", "name", "username"]
    fields = [eval(x) for x in names]
    return JsonResponse({"code": 0, "response": gd(names, fields)})

#forum create
def createforum(request):
    postRequest = None
    if request.method == "POST":
        postRequest = json.loads(request.body)
    cursor = db.cursor()
    sqlanswer = "insert into Forum(name, short_name, user) values ('"+ postRequest['name'] + "',\
    '"+postRequest.get('short_name', '') + "', '"+postRequest['user'] + "');"
    
    print sqlanswer
    try:
        cursor.execute(sqlanswer)
    except MySQLdb.IntegrityError:
        return JsonResponse({"code": 3, "response": "IntegrityError"})
    db.commit()
    resp = "select * from Forum where id=" + str(cursor.lastrowid) + ";"
    cursor.execute(resp)
    results = cursor.fetchall()
    for row in results:
        id = row[0]
        name = row[1]
        short_name = row[2]
        user = row[3]
    cursor.close()
    names = ["id", "name", "short_name", "user"]
    fields = [eval(x) for x in names]
    return JsonResponse({"code": 0, "response": gd(names, fields)})

#thread create
def createthread(request):
    postRequest = None
    if request.method == "POST":
        postRequest = json.loads(request.body)
    cursor = db.cursor()
    sqlanswer = "insert into Thread(forum, isClosed, isDeleted, message, slug, title, user, date) values ('" + postRequest['forum'] + "',"\
    + str(postRequest['isClosed']) +\
    "," + str(postRequest.get('isDeleted', 'False'))\
    + ", '"+postRequest['message'] +\
    "', '" + postRequest['slug'] +\
    "', '" + postRequest['title'] +\
    "', '" + postRequest['user'] + \
    "', '" + postRequest['date'] + "');"
    print sqlanswer
    try:
        cursor.execute(sqlanswer)
    except MySQLdb.IntegrityError:
        return JsonResponse({'code':3, 'response': 'integrity error'})
    db.commit()
    resp = "select * from Thread where id=" + str(cursor.lastrowid) + ";"
    cursor.execute(resp)
    results = cursor.fetchall()
    for row in results:
        date = str(row[5])
        forum = row[7]
        id = row[0]
        isClosed = row[1]
        isDeleted = row[2]
        message = row[6]
        slug = row[4]
        title = row[3]
        user = row[8]
    cursor.close()
    names = ["date", "forum", "id", "isClosed", "isDeleted", "message", "slug", "title", "user"]
    fields = [eval(x) for x in names]
    return JsonResponse({"code": 0, "response": gd(names, fields)})

#post create
def createpost(request):
    postRequest = None
    if request.method == "POST":
        postRequest = json.loads(request.body)
    cursor = db.cursor()
    sqlanswer = "insert into Posts(isApproved, user, date, message, isSpam, isHighlighted, thread, forum, isDeleted, isEdited, parent) values (" +\
    str(postRequest.get('isApproved', 'False')) + ",'" +\
    str(postRequest['user']) + "','" +\
    str(postRequest['date']) + "','" +\
    str(postRequest['message']) + "'," +\
    str(postRequest.get('isSpam', 'False')) + ","+\
    str(postRequest.get('isHighlighted', 'False')) + ","+\
    str(postRequest['thread']) + ",'" +\
    str(postRequest['forum']) +  "'," +\
    str(postRequest.get('isDeleted', 'False')) + "," +\
    str(postRequest.get('isEdited', 'False')) +  ", "
    if postRequest["parent"]:
        if postRequest["parent"] is None:
            sqlanswer += "null"
        else:
            sqlanswer += str(postRequest["parent"])
    else:
        sqlanswer += "null"
    sqlanswer += ");"
    print sqlanswer
    try:
        cursor.execute(sqlanswer)
    except:
        return JsonResponse({'code': 3, 'response': 'error message'})
    db.commit()
    resp = "select date, forum, id, isApproved, isDeleted, isEdited, isHighlighted, isSpam, message, parent, thread, user from Posts where id=" + str(cursor.lastrowid) + ";"
    cursor.execute(resp)
    results = cursor.fetchall()
    for row in results:
        date = str(row[0])
        forum = row[1]
        id = row[2]
        isApproved = row[3]
        isDeleted = row[4]
        isEdited = row[5]
        isHighlighted = row[6]
        isSpam = row[7]
        message = row[8]
        parent = row[9]
        thread = row[10]
        user = row[11]
    names = ["date", "forum", "id", "isApproved", "isDeleted", "isEdited", "isHighlighted", "isSpam", "message", "parent", "thread", "user"]
    fields = [eval(x) for x in names]
    return JsonResponse({"code": 0, "response": gd(names, fields)})

#details forum create
def detailsforum(request):
    postRequest = None
    if request.method == "POST":
        postRequest = json.loads(request.body)
    cursor = db.cursor()
    sqlanswer = "select * from Forum where short_name='" + request.GET.get('forum','') + "';"
    print sqlanswer
    user = None
    cursor.execute(sqlanswer)
    results = cursor.fetchall()
    for row in results:
        id = row[0]
        name = row[1]
        short_name = row[2]
        user = row[3]
    if user is None:
        return JsonResponse({'code': 3, 'response': 'invalid user name'})
    if 'related' in request.GET:
        sqlanswer = "select * from User where email='" + user + "';"
        print sqlanswer
        cursor.execute(sqlanswer)
        res = cursor.fetchall()
        for row in res: 
            about = row[0]
            email = row[1]
            followers = []
            following = []
            uid = row[2]
            isAnonymous = row[3]
            uname = row[4]
            subscriptions = []
            username = row[5]
        return JsonResponse({"code":0, "response":
          { "id": id,
            "name": name,
            "short_name": short_name,
            "user": {
                "about": about,
                "email": email,
                "followers": followers,
                "following": following,
                "id": uid,
                "isAnonymous": isAnonymous,
                "name": uname,
                "subscriptions": [],
                "username": username
            }}})
    names = ["id", "name", "short_name", "user"]
    fields = [eval(x) for x in names]
    return JsonResponse({"code": 0, "response": gd(names, fields)})

def sc(d):
    return JsonResponse({"code": 0, "response": d})

#post details create
def detailspost(request):
    postRequest = None
    if request.method == "POST":
        postRequest = json.loads(request.body)
    cursor = db.cursor()
    sqlanswer = "select date, dislikes, forum, id, isApproved, isDeleted, isEdited, isHighlighted, isSpam, likes, message, parent, thread, user from Posts where id="+request.GET['post'] + ";"
    cursor.execute(sqlanswer)
    results = cursor.fetchall()
    row = []
    try:
        row = next(iter(results))
    except:
        return JsonResponse({"code": 1, "response": "error message"})
    date = str(row[0])
    dislikes = row[1]
    forum = row[2]
    id = row[3]
    isApproved = row[4]
    isDeleted = row[5]
    isEdited = row[6]
    isHighlighted = row[7]
    isSpam = row[8]
    likes = row[9]
    message = row[10]
    points = likes - dislikes
    parent = row[11]
    thread = row[12]
    user = row[13]   
    names = ["date", "dislikes", "forum", "id", "isApproved", "isDeleted", "isEdited", "isHighlighted", "isSpam", "likes", "message", "points", "parent", "thread", "user"]
    fields = [eval(x) for x in names]
    return JsonResponse({"code": 0, "response": gd(names, fields)})

#user details create
def detailsuser(request):
    postRequest = None
    if request.method == "POST":
        postRequest = json.loads(request.body)
    cursor = db.cursor()
    sqlanswer = "select * from User where email='"+request.GET['user'] + "';"
    print sqlanswer
    cursor.execute(sqlanswer)
    results = cursor.fetchall()
    names = []
    fields = []
    for row in results:
        about = row[0]
        email = row[1]
        id = row[2]
        isAnonymous = row[3]
        name = row[4]
        username = row[5]
        followers = []
        following = []
        subscriptions = [] 
        sqlanswer2 = "select following from Follow where follower='" + email + "';"
        print sqlanswer2
        cursor.execute(sqlanswer2)
        result = cursor.fetchall()
        for row in result:
            following.append(row[0])
        sqlanswer3 = "select follower from Follow where following='" + email + "';"
        print sqlanswer3
        cursor.execute(sqlanswer3)
        result1 = cursor.fetchall()
        for row in result1:
            followers.append(row[0])
        sqlanswer4 = "select * from Subscribe where subscriber='" + email + "';"
        print sqlanswer4
        cursor.execute(sqlanswer4)
        result2 = cursor.fetchall()
        for row in result2:
            subscriptions.append(row[1])
        names = ["about", "email", "followers", "following", "id", "isAnonymous", "name", "subscriptions", "username"]
        fields = [eval(x) for x in names]
    return JsonResponse({"code": 0, "response": gd(names, fields)})

#details thread
def detailsthread(request):
    postRequest = None
    if request.method == "POST":
        postRequest = json.loads(request.body)
    cursor = db.cursor()
    sqlanswer = "select * from Thread where id='"+request.GET['thread'] + "';"
    print sqlanswer
    try:
        cursor.execute(sqlanswer)
    except:
        return JsonResponse({"code": 3, "response": "error"})
    results = cursor.fetchall()
    if not results:
        return JsonResponse({"code": 1, "response": "error"})
    names = ["id", "isClosed", "isDeleted", "title", "slug", "date", "message", "forum", "user", "likes", "dislikes"]
    answer = {}
    data = {}
    for row in results:
        data = dict(zip(names, row))
        data["points"] = data["likes"] - data["dislikes"]
        data["date"] = str(data["date"])
        sqlanswer2 = "select count(*) from Posts where isDeleted=0 and thread=" + str(data["id"]) + ";"
        cursor.execute(sqlanswer2)
        resp = cursor.fetchall()
        for row2 in resp:
            data["posts"] = row2[0]
        if "user" in request.GET.getlist('related'):
            sqlanswer1 = "select * from User where email='" + data["user"]  + "';"
            print sqlanswer1
            cursor.execute(sqlanswer1)
            results1 = cursor.fetchall()
            ansUser = []
            userNames = ["about", "email", "id", "isAnonymous", "name", "username", "user"]
            for userRow in results1:
                data["user"] = dict(zip(userNames, userRow))
                data["user"]["followers"] = data["user"]["following"] = data["user"]["subsctiptions"] = []
        if "forum" in request.GET.getlist('related'):
            sqlanswer1 = "select * from Forum where name='" + data["forum"] + "';"
            print sqlanswer1
            cursor.execute(sqlanswer1)
            results1 = cursor.fetchall()
            ansForum = []
            forumNames = ["id", "name", "short_name", "user"]
            for forumRow in results1:
                data["forum"] = dict(zip(forumNames, forumRow))      
        if "thread" in request.GET.getlist('related'):
            return JsonResponse({"code": 3, "response": "error"})
    if not data:
        return JsonResponse({"code": 1, "response": "error"})
    return JsonResponse({"code": 0, "response": data})


#list posts forum
def listpostsforum(request):
    print ">>>>> entering listposts from forum"
    postRequest = None
    if request.method == "POST":
        postRequest = json.loads(request.body)
    cursor = db.cursor()
    if ('since' in request.GET):
        datesince = request.GET['since']
        sqlanswer = "select date, dislikes, forum, id, isApproved, isDeleted, isEdited, isHighlighted, isSpam, likes, message, parent, thread, user from Posts where forum='"+ request.GET.get('forum', '') + "' and date>='"+ str(datesince) + "' "
    else:
        sqlanswer = "select date, dislikes, forum, id, isApproved, isDeleted, isEdited, isHighlighted, isSpam, likes, message, parent, thread, user from Posts where forum='"+request.GET.get('forum', '') + "' " 
    order = request.GET.get('order', 'desc')
    sqlanswer = sqlanswer + "order by date " + order 
    if ('limit' in request.GET):
        sqlanswer += " limit " + request.GET["limit"] 
    sqlanswer += ";"
    print ">>>>> sqlanswer= ", sqlanswer
    cursor.execute(sqlanswer)
    results = cursor.fetchall()
    total = []
    for row in results:
        date = str(row[0])
        dislikes = row[1]
        forum = row[2]
        id = row[3]
        print ">>>>>", id
        isApproved = row[4]
        isDeleted = row[5]
        isEdited = row[6]
        isHighlighted = row[7]
        isSpam = row[8]
        likes = row[9]
        message = row[10]
        points = likes - dislikes
        parent = row[11]
        thread = row[12]
        user = row[13]
        if 'related' in request.GET:
            for i in request.GET.getlist('related'):
                if (i == 'thread'):
                    sqlanswer2 = "select * from Thread where id="+str(thread) + ";"
                    print sqlanswer2
                    trdid = str(thread)
                    cursor.execute(sqlanswer2)
                    results2 = cursor.fetchall()
                    names = ["id", "isClosed", "isDeleted", "title", "slug", "date", "message", "forum", "user", "likes", "dislikes"]
                    for row in results2:
                        thread = dict(zip(names, row)) 
                        thread["points"] = thread["likes"] - thread["dislikes"]
                        thread["date"] = str(thread["date"])
                        sqlanswer2 = "select count(*) from Posts where thread=" + trdid + ";"
                        cursor.execute(sqlanswer2)
                        resp = cursor.fetchall()
                        thread["posts"] = None
                        for row2 in resp:
                            thread["posts"] = row2[0]   
                if (i == 'forum'):
                    sqlanswer2 = "select * from Forum where short_name='"+str(forum) + "';"
                    print sqlanswer2
                    cursor.execute(sqlanswer2)
                    results2 = cursor.fetchall()
                    name = None
                    for row in results2:
                        fid = row[0]
                        name = row[1]
                        short_name = row[2]
                        fuser = row[3]
                    forum = {"id": fid,
                             "name": name,
                             "short_name": short_name,
                             "user": fuser}
                if (i == 'user'):
                    sqlanswer2 = "select * from User where email='" + str(user) + "';"
                    print sqlanswer2
                    cursor.execute(sqlanswer2)
                    results2 = cursor.fetchall()
                    for row in results2:      
                        about = row[0]
                        email = row[1]
                        followers = '[]'
                        following = '[]'
                        uid = row[2]
                        isAnonymous = row[3]
                        uname = row[4]
                        subscriptions = '[]'
                        username = row[5]
                    user = {"about": about,
                            "email": email,
                            "followers": followers,
                            "following": following,
                            "id": uid,
                            "isAnonymous": isAnonymous,
                            "name": uname,
                            "subscriptions": subscriptions,
                            "username": username}
        total.append({ 
            "date": date,
            "dislikes": dislikes,
            "forum": forum,
            "id": id,
            "isApproved": isApproved,
            "isDeleted": isDeleted,
            "isEdited": isEdited,
            "isHighlighted":isHighlighted,
            "isSpam":isSpam,
            "likes": likes,
            "message":message,
            "points":points,
            "parent": parent,
            "thread":thread,
            "user": user})
    return JsonResponse({"code": 0, "response": total})

#list post
def listpost(request):
    postRequest = None
    if request.method == "POST":
        postRequest = json.loads(request.body)
    cursor = db.cursor()
    sqlanswer = "select * from Posts "
    if 'forum' in request.GET:
        forum = request.GET['forum']
        sqlanswer += "where forum='"+ forum + "' "
    else:
        if 'thread' in request.GET:
            thread = request.GET['thread']
            sqlanswer += "where thread=" + thread + " "
    if 'since' in request.GET:
        datesince = request.GET['since']
        sqlanswer += "and date>='"+ datesince + "' "
    order = request.GET.get('order','desc')
    sqlanswer += "order by date " + order
    if 'limit' in request.GET:
        limit = request.GET['limit']
        sqlanswer += " limit " + limit
    sqlanswer += ";"
    print sqlanswer
    cursor.execute(sqlanswer)
    results = cursor.fetchall()
    total = []
    for row in results:
        date = str(row[0])
        dislikes = row[1]
        forum = row[2]
        id = row[3]
        isApproved = row[4]
        isDeleted = row[5]
        isEdited = row[6]
        isHighlighted = row[7]
        isSpam = row[8]
        likes = row[9]
        message = row[10]
        user = row[11]
        points = likes - dislikes
        thread = row[12]
        parent = row[13]
        total.append({
            "date": date,
            "dislikes": dislikes,
            "forum": forum,
            "id": id,
            "isApproved": isApproved,
            "isDeleted": isDeleted,
            "isEdited": isEdited,
            "isHighlighted":isHighlighted,
            "isSpam":isSpam,
            "likes": likes,
            "message":message,
            "points":points,
            "parent": parent,
            "thread":thread,
            "user": user})
    return JsonResponse({"code": 0, "response": total})


#folower user
def followuser(request):
    postRequest = None
    if request.method == "POST":
        postRequest = json.loads(request.body)
    cursor = db.cursor()
    follower = postRequest.get('follower', '')
    followee = postRequest.get('followee', '')
    print follower + "\n"
    print followee + "\n"
    try:
        sqlanswer = "insert into Follow (follower, following) values ('" + follower + "', '" + followee + "');"
    except:
        return JsonResponse({"code": 3, "response": "error msg"})
    print sqlanswer
    try:
        cursor.execute(sqlanswer)
    except MySQLdb.IntegrityError:
        JsonResponse({"code": 3, "response": "error msg"})
    db.commit()
    sqlanswer2 = "select * from User where email='" + follower + "';"
    print sqlanswer2
    cursor.execute(sqlanswer2)
    results = cursor.fetchall()
    for row in results:
       about = row[0]
       email = row[1]
       id = row[2]
       isAnonymous = row[3]
       name = row[4]
       username = row[5]
    subscriptions = []
    sqlanswer4 = "select count(*) from Subscribe where subscriber='"+email+"';"
    print sqlanswer4
    cursor.execute(sqlanswer4)
    result2 = cursor.fetchall()
    for row in result2:
        subscriptions.append(row[0])
    sqlanswer2 = "select following from Follow where follower='" + email + "';"
    print sqlanswer2
    followers = []
    following = []
    cursor.execute(sqlanswer2)
    result = cursor.fetchall()
    for row in result:
        following.append(row[0])
    sqlanswer3 = "select follower from Follow where following='" + email + "';"
    print sqlanswer3
    cursor.execute(sqlanswer3)
    result1 = cursor.fetchall()
    for row in result1:
        followers.append(row[0])
    names = ["about", "email", "id", "isAnonymous", "followers", "following", "subscriptions", "username", "name"]
    fields = [eval(x) for x in names]
    return JsonResponse({"code": 0, "response": gd(names, fields)})


#listthread
def listthread(request):
    postRequest = None
    if request.method == "POST":
        postRequest = json.loads(request.body)
    cursor = db.cursor()
    sqlanswer = ""
    if "user" in request.GET:
        sqlanswer = "select * from Thread where user = '" + request.GET['user'] + "' "
    elif "forum" in request.GET:
        sqlanswer = "select * from Thread where forum='" + request.GET['forum'] + "' "
    if "since" in request.GET:
        sqlanswer += "and date>='" + request.GET['since'] + "' "
    sqlanswer += "order by date " + request.GET.get('order', 'desc') + " "
    if "limit" in request.GET:
        sqlanswer += "limit " + request.GET['limit']
    sqlanswer += ";"
    print sqlanswer
    cursor.execute(sqlanswer)
    results = cursor.fetchall()
    names = ["id", "isClosed", "isDeleted", "title", "slug", "date", "message", "forum", "user", "likes", "dislikes"]
    answer = []
    for row in results:
        data = dict(zip(names, row))
        data["points"] = data["likes"] - data["dislikes"]
        data["date"] = str(data["date"])
        sqlanswer2 = "select count(*) from Posts where isDeleted=0 and thread=" + str(data["id"]) + ";"
        cursor.execute(sqlanswer2)
        resp = cursor.fetchall()
        for row2 in resp:
            data["posts"] = row2[0]
        answer.append(data)
    return sc(answer)

def dfs(id, limit, cursor, posts, request):
    sqlanswer = "select date, dislikes, forum, id, isApproved, isDeleted, isHighlighted, isEdited, isSpam, likes, message, user, thread, parent from Posts where thread = " + str(request.GET['thread']) + " and id = " + str(id) + ";"
    if len(posts) == limit:
        return
    cursor.execute(sqlanswer)
    results = cursor.fetchall()
    names = ["date", "dislikes", "forum", "id", "isApproved", "isDeleted", "isHighlighted", "isEdited", "isSpam", "likes", "message", "user", "thread", "parent"]
    answer = []
    for row in results:
        data = dict(zip(names, row))
        data["date"] = str(data["date"])
        data["points"] = data["likes"] - data["dislikes"]
        answer.append(data)
    posts += answer
    sqlanswer2 = "select id from Posts where thread = " + str(request.GET['thread']) + " and parent = " + str(id) + ";"
    cursor.execute(sqlanswer2)
    results = cursor.fetchall()
    for row in results:
        dfs(row[0], limit, cursor, posts, request)

#listpoststhread
def listpoststhread(request):
    postRequest = None
    if request.method == "POST":
        postRequest = json.loads(request.body)
    cursor = db.cursor()  
    sort = request.GET.get('sort', 'flat')
    sqlanswer = None
    if sort == 'flat': 
        sqlanswer = "select date, dislikes, forum, id, isApproved, isDeleted, isHighlighted, isEdited, isSpam, likes, message, user, thread, parent from Posts "
        if "thread" in request.GET:
            sqlanswer += "where thread = " + str(request.GET['thread']) + " "
        if "since" in request.GET:
            sqlanswer += "and date >= '" + request.GET['since'] + "' "
        sqlanswer += "order by date " + request.GET.get('order', 'desc') + " "
        if "limit" in request.GET:
            sqlanswer += "limit " + request.GET['limit'] 
        sqlanswer += ";"
        print sqlanswer
        cursor.execute(sqlanswer)
        results = cursor.fetchall()
        names = ["date", "dislikes", "forum", "id", "isApproved", "isDeleted", "isHighlighted", "isEdited", "isSpam", "likes", "message", "user", "thread", "parent"]
        answer = []
        for row in results:
            data = dict(zip(names, row))
            data["date"] = str(data["date"])
            data["points"] = data["likes"] - data["dislikes"]
            answer.append(data)
        return sc(answer)
    if sort == 'tree':
        sqlanswer = "select id from Posts where thread = "+ str(request.GET['thread']) + " and parent is null "
        if "since" in request.GET:
            sqlanswer += "and date >= '" + request.GET['since'] + "' "
        sqlanswer += "order by date " + request.GET.get('order', 'desc') + ";"
        cursor.execute(sqlanswer)
        results = cursor.fetchall()
        answer = []
        lim = int(request.GET.get('limit', '-1'))
        print lim
        for row in results:
            dfs(row[0], lim, cursor, answer, request)
        return sc(answer)
    if sort == 'parent_tree':
        sqlanswer = "select id from Posts where thread = " + str(request.GET['thread']) + " and parent is null order by date "+ request.GET.get('order', 'desc')
        if 'limit' in request.GET:
            sqlanswer += " limit " + request.GET["limit"]
        sqlanswer += ";"
        cursor.execute(sqlanswer)
        results = cursor.fetchall()
        answer = []
        for row in results:
            dfs(row[0], -1, cursor, answer, request)
        return sc(answer)

def listthreadsforum(request):
    postRequest = None
    if request.method == "POST":
        postRequest = json.loads(request.body)
    cursor = db.cursor()
    sqlanswer = "select * from Thread where forum='" + request.GET['forum'] + "'" 
    if "since"  in request.GET:
        sqlanswer += " and date>= '" + request.GET['since']+ "'"
    if "order" in request.GET:
        sqlanswer += " order by date " + request.GET['order']
    if "limit" in request.GET:
        sqlanswer += " limit " + request.GET['limit']
    sqlanswer += ";"
    print sqlanswer
    cursor.execute(sqlanswer)
    results = cursor.fetchall()
    names = ["id", "isClosed", "isDeleted", "title", "slug", "date", "message", "forum", "user", "likes", "dislikes"]
    answer = []
    for row in results:
        data = dict(zip(names, row))
        data["points"] = data["likes"] - data["dislikes"]
        data["date"] = str(data["date"])
        if "user" in request.GET.getlist('related'):
            sqlanswer1 = "select * from User where email='" + data["user"]  + "';"
            print sqlanswer1
            cursor.execute(sqlanswer1)
            results1 = cursor.fetchall()
            ansUser = []
            userNames = ["about", "email", "id", "isAnonymous", "name", "username", "user"]
            for userRow in results1:
                data["user"] = dict(zip(userNames, userRow))
                data["user"]["followers"] = data["user"]["following"] = []
                data["user"]["subscriptions"] = []
                sqlanswersub = "select subscription from Subscribe where subscriber='"+data["user"]["email"]+"';"
                cursor.execute(sqlanswersub)
                resultss = cursor.fetchall()
                for row in resultss:
                    data["user"]["subscriptions"].append(row[0])
        if "forum" in request.GET.getlist('related'):
            sqlanswer1 = "select * from Forum where short_name='" + request.GET['forum'] + "';"
            print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>", sqlanswer1
            cursor.execute(sqlanswer1)
            results1 = cursor.fetchall()
            ansForum = []
            data["forum"] = {}
            forumNames = ["id", "name", "short_name", "user"]
            print "12312312312", results1
            for forumRow in results1:
                data["forum"] = dict(zip(forumNames, forumRow))
                print forumRow
                print "11111111111111111111111111111111111111111", data["forum"]
        sqlanswer2 = "select count(*) from Posts where isDeleted=0 and thread=" + str(data["id"]) + ";"
        cursor.execute(sqlanswer2)
        resp = cursor.fetchall()
        for row2 in resp:
            data["posts"] = row2[0]
        answer.append(data)
    return sc(answer)

#listusersforum
def listusersforum(request):
    postRequest = None
    if request.method == "POST":
        postRequest = json.loads(request.body)
    cursor = db.cursor()
    sqlanswer = "select * from User as u inner join Posts as p on p.user=u.email where p.forum='" + request.GET["forum"] + "'"
    if "since_id" in request.GET:
        sqlanswer += " and u.id>=" + request.GET["since_id"]
    sqlanswer += " group by u.email"
    sqlanswer += " order by u.name "+ request.GET.get("order", "desc")
    if "limit" in request.GET:
        sqlanswer += " limit " + request.GET["limit"]
    sqlanswer += ";"
    cursor.execute(sqlanswer)
    results = cursor.fetchall()
    names = ["about", "email", "id", "isAnonymous", "name", "username", "user"]
    answer = []
    for row in results:
        data = dict(zip(names, row))
        data["followers"] = data["following"] = [] 
        data["subscriptions"] = []
        sqlanswer2 = "select subscription from Subscribe where subscriber='" + str(data["email"]) + "';"
        cursor.execute(sqlanswer2)
        res = cursor.fetchall()
        for row2 in res:
            data["subscriptions"].append(row2[0])
        answer.append(data)
    return sc(answer)

#remove post
def removepost(request):
    postRequest = None
    if request.method == "POST":
        postRequest = json.loads(request.body)
    cursor = db.cursor()
    sqlanswer = "update Posts set isDeleted=1 where id=" + str(postRequest["post"]) + ";"
    print sqlanswer
    cursor.execute(sqlanswer)
    db.commit()
    answer = {"post": postRequest["post"]}
    return sc(answer)


#restor post
def restorepost(request):
    postRequest = None
    if request.method == "POST":
        postRequest = json.loads(request.body)
    cursor = db.cursor()
    sqlanswer = "update Posts set isDeleted=0 where id=" + str(postRequest["post"]) + ";"
    print sqlanswer
    cursor.execute(sqlanswer)
    db.commit()
    answer = {"post": postRequest["post"]}
    return sc(answer)

#update post
def updatepost(request):
    postRequest = None
    if request.method == "POST":
        postRequest = json.loads(request.body)
    cursor = db.cursor()
    sqlanswer = "update Posts set message='" + postRequest["message"] + "' where id=" + str(postRequest["post"]) + ";"
    print sqlanswer
    cursor.execute(sqlanswer)
    db.commit()
    sqlanswer2 = "select * from Posts where id=" + str(postRequest["post"]) + ";"
    cursor.execute(sqlanswer2)
    results = cursor.fetchall()
    names = ["date", "dislikes", "forum", "id", "isApproved", "isDeleted", "isEdited", "isHighlighted", "isSpam", "likes", "message", "user", "thread", "parent"]
    answer = []
    for row in results:
        answer.append(dict(zip(names, row)))
    return sc(answer)

#voted post
def votepost(request):
    postRequest = None
    if request.method == "POST":
        postRequest = json.loads(request.body)
    cursor = db.cursor()
    sqlanswer = ''
    if postRequest['vote'] == -1:
        sqlanswer = "update Posts set dislikes = dislikes + 1 where id=" + str(postRequest["post"]) + ";"
    if postRequest['vote'] == 1:
        sqlanswer = "update Posts set likes = likes + 1 where id=" + str(postRequest["post"]) + ";"
    cursor.execute(sqlanswer)
    db.commit()
    sqlanswer2 = "select * from Posts where id=" + str(postRequest["post"]) + ";"
    cursor.execute(sqlanswer2)
    results = cursor.fetchall()
    names = ["date", "dislikes", "forum", "id", "isApproved", "isDeleted", "isEdited", "isHighlighted", "isSpam", "likes", "message", "user", "thread", "parent"]
    answer = []
    for row in results:
        answer.append(dict(zip(names, row)))
    return sc(answer)

#list followers user
def listfollowersuser(request):
    postRequest = None
    if request.method == "POST":
        postRequest = json.loads(request.body)
    cursor = db.cursor()
    sqlanswer = "select * from User as u inner join Follow as f on f.following = u.email where f.follower='" + request.GET["user"] + "' and u.id>" + request.GET.get("since_id", "0") + " order by u.id " + request.GET.get("order", "desc")
    if "limit" in request.GET:
        sqlanswer += " limit " + request.GET["limit"]
    sqlanswer += ";" 
    print sqlanswer
    cursor.execute(sqlanswer)
    results = cursor.fetchall()
    names = ["about", "email", "id", "isAnonymous", "name", "username"]
    answer = []
    for row in results:
        data = dict(zip(names, row))
        user2 = row[1]
        sqlanswer2 = "select follower from Follow where following='" + user2 + "';"
        print sqlanswer2
        cursor.execute(sqlanswer2)
        results = cursor.fetchall()
        uans = []
        for row in results:
            uans.append(row[0])
        data["followers"] = uans
        sqlanswer2 = "select following from Follow where follower='" + user2 + "';"
        print sqlanswer2
        cursor.execute(sqlanswer2)
        results = cursor.fetchall()
        uans = []
        for row in results:
            uans.append(row[0])
        data["following"] = uans
        sqlanswer3 = "select subscription from Subscribe where subscriber='" + user2 + "';"
        cursor.execute(sqlanswer3)
        results = cursor.fetchall()
        sans = []
        for row in results:
            sans.append(row[0])
        data["subscriptions"] = sans
        answer.append(data)
    return sc(answer)  

#following user
def listfollowinguser(request):
    postRequest = None
    if request.method == "POST":
        postRequest = json.loads(request.body)
    cursor = db.cursor()
    sqlanswer = "select * from User as u inner join Follow as f on f.following = u.email where f.follower='" + request.GET["user"] + "' and u.id>=" + request.GET.get("since_id", "-1") + " order by u.id " + request.GET.get("order", "desc")
    if "limit" in request.GET:
        sqlanswer += " limit " + request.GET["limit"]
    sqlanswer += ";" 
    cursor.execute(sqlanswer)
    results = cursor.fetchall()
    names = ["about", "email", "id", "isAnonymous", "name", "username"]
    answer = []
    for row in results:
        data = dict(zip(names, row))
        user2 = row[1]
        sqlanswer2 = "select follower from Follow where following='" + user2 + "';"
        print sqlanswer2
        cursor.execute(sqlanswer2)
        results = cursor.fetchall()
        uans = []
        for row in results:
            uans.append(row[0])
        data["followers"] = uans
        sqlanswer2 = "select following from Follow where follower='" + user2 + "';"
        print sqlanswer2
        cursor.execute(sqlanswer2)
        results = cursor.fetchall()
        uans = []
        for row in results:
            uans.append(row[0])
        data["following"] = uans
        sqlanswer3 = "select subscription from Subscribe where subscriber='" + user2 + "';"
        cursor.execute(sqlanswer3)
        results = cursor.fetchall()
        sans = []
        for row in results:
            sans.append(row[0])
        data["subscriptions"] = sans
        answer.append(data)
    sqlanswer = "select following from Follow where follower='"+ request.GET["user"] + "';"
    print ":::::::::::::::::::", sqlanswer
    cursor.execute(sqlanswer)
    results = cursor.fetchall()
    for row in results:
        print ":::::::::::::   ", row[0]
    return sc(answer) 

#list post user
def listpostsuser(request):
    postRequest = None
    if request.method == "POST":
        postRequest = json.loads(request.body)
    cursor = db.cursor()
    sqlanswer = "select * from Posts where user='" + request.GET["user"] + "'"
    if "since" in request.GET:
        sqlanswer += " and date>='" + request.GET["since"] + "'"
    sqlanswer += " order by date " + request.GET.get("order","desc")
    if "limit" in request.GET:
        sqlanswer += " limit " + request.GET["limit"]
    sqlanswer += ";"
    print sqlanswer
    cursor.execute(sqlanswer)
    results = cursor.fetchall()
    names = ["date", "dislikes", "forum", "id", "isApproved", "isDeleted", "isEdited", "isHighlighted", "isSpam", "likes", "message", "user", "thread", "parent"]
    answer = []
    for row in results:
        data = dict(zip(names, row))
        data["date"] = str(data["date"])
        data["points"] = data["likes"] - data["dislikes"]
        answer.append(data)
    return sc(answer)

#unfolowing user
def unfollowuser(request):
    postRequest = None
    if request.method == "POST":
        postRequest = json.loads(request.body)
    cursor = db.cursor()
    print postRequest
    sqlanswer = "delete from Follow where follower='" + postRequest["follower"] + "' and following='" + postRequest["followee"] + "';"
    print sqlanswer
    cursor.execute(sqlanswer)
    db.commit()
    sqlanswer2 = "select * from User where email='" + postRequest["follower"] + "';"
    print sqlanswer2
    cursor.execute(sqlanswer2)
    results = cursor.fetchall()
    names = ["about", "email", "id", "isAnonymous", "name", "username", "user"]
    answer = []
    for row in results:
        data = dict(zip(names, row))
        user2 = row[1]
        sqlanswer2 = "select follower from Follow where following='" + user2 + "';"
        print sqlanswer2
        cursor.execute(sqlanswer2)
        results = cursor.fetchall()
        uans = []
        for row in results:
            uans.append(row[0])
        data["followers"] = uans
        sqlanswer2 = "select following from Follow where follower='" + user2 + "';"
        print sqlanswer2
        cursor.execute(sqlanswer2)
        results = cursor.fetchall()
        uans = []
        for row in results:
            uans.append(row[0])
        data["following"] = uans
        sqlanswer3 = "select id from Thread where user='" + user2 + "';"
        cursor.execute(sqlanswer3)
        results = cursor.fetchall()
        sans = []
        for row in results:
            sans.append(row[0])
        data["subscriptions"] = sans
        answer.append(data)
    return sc(answer)

#update profile
def updateprofileuser(request):
    postRequest = None
    if request.method == "POST":
        postRequest = json.loads(request.body)
    cursor = db.cursor()
    sqlanswer = "update User set about='" + postRequest["about"] + "', name='" + postRequest["name"] + "' where email='" + postRequest["user"] + "';"
    print sqlanswer
    cursor.execute(sqlanswer)
    db.commit()
    sqlanswer2 = "select * from User where email='" + postRequest["user"] + "';"
    cursor.execute(sqlanswer2)
    results = cursor.fetchall()
    names = ["about", "email", "id", "isAnonymous", "name", "username", "user"]
    answer = []
    for row in results:
        data = dict(zip(names, row))
        user2 = row[1]
        sqlanswer2 = "select follower from Follow where following='" + user2 + "';"
        print sqlanswer2
        cursor.execute(sqlanswer2)
        results = cursor.fetchall()
        uans = []
        for row in results:
            uans.append(row[0])
        data["followers"] = uans
        sqlanswer2 = "select following from Follow where follower='" + user2 + "';"
        print sqlanswer2
        cursor.execute(sqlanswer2)
        results = cursor.fetchall()
        uans = []
        for row in results:
            uans.append(row[0])
        data["following"] = uans
        sqlanswer3 = "select id from Thread where user='" + user2 + "';"
        cursor.execute(sqlanswer3)
        results = cursor.fetchall()
        sans = []
        for row in results:
            sans.append(row[0])
        data["subscriptions"] = sans
        answer.append(data)
    return sc(answer)

#close thread
def closethread(request):
    postRequest = None
    if request.method == "POST":
        postRequest = json.loads(request.body)
    cursor = db.cursor()
    sql = "update Thread set isClosed=1 where id=" + str(postRequest["thread"]) + ";"
    cursor.execute(sql)
    db.commit()
    answer ={"thread": postRequest["thread"]} 
    return sc(answer)

def openthread(request):
    postRequest = None
    if request.method == "POST":
        postRequest = json.loads(request.body)
    cursor = db.cursor()
    sql = "update Thread set isClosed=0 where id=" + str(postRequest["thread"]) + ";" 
    cursor.execute(sql)
    db.commit()
    answer ={"thread": postRequest["thread"]} 
    return sc(answer)

def removethread(request):
    postRequest = None
    if request.method == "POST":
        postRequest = json.loads(request.body)
    cursor = db.cursor()
    sql = "update Thread set isDeleted=1 where id=" + str(postRequest["thread"]) + ";" 
    cursor.execute(sql)
    db.commit()
    sql = "update Posts set isDeleted=1 where thread=" + str(postRequest["thread"]) + ";"
    cursor.execute(sql)
    db.commit()
    answer ={"thread": postRequest["thread"]} 
    return sc(answer)

def restorethread(request):
    postRequest = None
    if request.method == "POST":
        postRequest = json.loads(request.body)
    cursor = db.cursor()
    sql = "update Thread set isDeleted=0 where id=" + str(postRequest["thread"]) + ";" 
    cursor.execute(sql)
    db.commit() 
    sql = "update Posts set isDeleted=0 where thread=" + str(postRequest["thread"]) + ";"
    cursor.execute(sql)
    db.commit()
    answer ={"thread": postRequest["thread"]} 
    return sc(answer)

def votethread(request):
    postRequest = None
    if request.method == "POST":
        postRequest = json.loads(request.body)
    cursor = db.cursor()
    sql = ''
    if postRequest['vote'] == -1:
        sql = "update Thread set dislikes = dislikes + 1 where id=" + str(postRequest["thread"]) + ";"
    if postRequest['vote'] == 1:
        sql = "update Thread set likes = likes + 1 where id=" + str(postRequest["thread"]) + ";"
    cursor.execute(sql)
    db.commit()
    sql2 = "select id, isClosed, isDeleted, title, slug, date, message, forum, user, likes, dislikes from Thread where id=" + str(postRequest["thread"]) + ";"
    cursor.execute(sql2)
    results = cursor.fetchall()
    names = ["id", "isClosed", "isDeleted", "title", "slug", "date", "message", "forum", "user", "likes", "dislikes"]
    answer = []
    for row in results:
        data = dict(zip(names, row))
        data["points"] = data["likes"] - data["dislikes"]
        sql2 = "select count(*) from Posts where isDeleted=0 and thread=" + str(data["id"]) + ";"
        cursor.execute(sql2)
        resp = cursor.fetchall()
        for row2 in resp:
            data["posts"] = row2[0]
        answer.append(data)
    return sc(answer)

def subscribethread(request):
    postRequest = None
    if request.method == "POST":
        postRequest = json.loads(request.body)
    cursor = db.cursor()
    sql = "insert into Subscribe values('" + postRequest["user"] + "', " + str(postRequest["thread"]) + ");"
    try:
        cursor.execute(sql)
    except MySQLdb.IntegrityError:
        return JsonResponse({"code": 3, "response": "IntegrityError"})
    db.commit()
    answer = {"thread": postRequest["thread"],
              "user": postRequest["user"]}
    return sc(answer)

def unsubscribethread(request):
    postRequest = None
    if request.method == "POST":
        postRequest = json.loads(request.body)
    cursor = db.cursor()
    sql = "delete from Subscribe where subscriber='" + postRequest["user"] + "' and subscription=" + str(postRequest["thread"]) + ";"
    cursor.execute(sql)
    db.commit()
    answer = {"thread": postRequest["thread"],
              "user": postRequest["user"]}
    return sc(answer)

#update thread
def updatethread(request):
    postRequest = None
    if request.method == "POST":
        postRequest = json.loads(request.body)
    cursor = db.cursor()
    sqlanswer = "update Thread set message='" + postRequest["message"] + "', slug='" + postRequest["slug"] + "' where id=" + str(postRequest["thread"]) + ";"
    cursor.execute(sqlanswer)
    db.commit()
    answer = []
    results = cursor.fetchall()
    names = ["id", "isClosed", "isDeleted", "title", "slug", "date", "message", "forum", "user", "likes", "dislikes"]
    for row in results:
        data = dict(zip(names, row))
        data["points"] = data["likes"] - data["dislikes"]
        sqlanswer2 = "select count(*) from Posts where isDeleted=0 and thread=" + str(data["id"]) + ";"
        cursor.execute(sqlanswer2)
        resp = cursor.fetchall()
        for row2 in resp:
            data["posts"] = row2[0]
        answer.append(data)
    return sc(answer)

