from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from main.models import Board, Profile
from django.contrib.auth.models import User
import json
import time

# Create your views here.
boardinfo = None
profileid = 0

def index(request):
    if not request.user.is_authenticated:
        return render(request, "main/login.html")
    else:
        return HttpResponseRedirect(reverse("boards"))


def login_view(request):
    username = request.POST["username"]
    password = request.POST["password"]
    global user
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "main/login.html", {"message": "Invalid Credentials"})

def logout_view(request):
    logout(request)
    return render(request, "main/login.html", {"message": "Logged out."})

def toSignUp_view(request):
    return render(request, "main/signup.html")

def signUp_view(request):
    username = request.POST["username"]
    password = request.POST["password"]
    email = request.POST["email"]
    firstname = request.POST["firstName"]
    lastname = request.POST["lastName"]
    user = authenticate(request, username=username, password=password)
    if user is None:
        if username is not None and password is not None and email is not None and firstname is not None and lastname is not None:
            newuser = User.objects.create_user(
            username=username,
            password=password,
            email=email,
            first_name=firstname,
            last_name=lastname)
            user = authenticate(request, username=username, password=password)
            profile = Profile(userid = user.id, username = user.username)
            profile.save()
            login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "main/signup.html", {"message": "Username already in use"})

def boardmaker(request):
    shortlist = [0, 1, 2, 3, 4]
    list = [[], [], [], [], []]
    for i in range(0, 5):
        for j in range(0, 5):
            list[i].append(j + 5*i)
    context = {
        "shortlist": shortlist,
        "list": list
    }
    return render(request, "main/boardmaker.html", context)

def createBoard(request):
    bigstring = ""
    items = []
    for i in range(0, 25):
        if request.POST[str(i)] == "":
            shortlist = [0, 1, 2, 3, 4]
            list = [[], [], [], [], []]
            for i in range(0, 5):
                for j in range(0, 5):
                    list[i].append(j + 5*i)
            context = {
                "shortlist": shortlist,
                "list": list,
                "message": "All boxes must have text",
            }
            return render(request, "main/boardmaker.html", context)
        if request.POST[str(i)] in items:
            shortlist = [0, 1, 2, 3, 4]
            list = [[], [], [], [], []]
            for i in range(0, 5):
                for j in range(0, 5):
                    list[i].append(j + 5*i)
            context = {
                "shortlist": shortlist,
                "list": list,
                "message": "All boxes must have unique prompts",
            }
            return render(request, "main/boardmaker.html", context)
        items.append(request.POST[str(i)])
        bigstring = bigstring + request.POST[str(i)] + ", "
    name = request.POST["boardname"]
    for board in Board.objects.all():
        if board.name == name:
            shortlist = [0, 1, 2, 3, 4]
            list = [[], [], [], [], []]
            for i in range(0, 5):
                for j in range(0, 5):
                    list[i].append(j + 5*i)
            context = {
                "shortlist": shortlist,
                "list": list,
                "message": "That name is already in use"
            }
            return render(request, "main/boardmaker.html", context)
    ts = time.time()
    board = Board(name = name, info = bigstring, time = ts, userid = request.user.id, username = request.user.username)
    board.save()
    profile = Profile.objects.get(userid = request.user.id)
    boards = json.loads(profile.boards)
    boards['boards'].append(board.id)
    profile.boards = json.dumps(boards)
    profile.save()
    global boardinfo
    boardinfo = board.getInfo()
    context = {
        "boardinfo": boardinfo,
    }
    return HttpResponseRedirect(reverse("boards"))

def boards(request):
    boardlist=[]
    boardnames=[]
    message = ""
    if Profile.objects.get(userid = request.user.id).boards == "":
        message = "You have no boards yet"
        context = {
            "user":request.user,
            "names": boardnames,
            "message": message,
        }
        return render(request, "main/boards.html", context)
    boards = json.loads(Profile.objects.get(userid = request.user.id).boards)['boards']
    for i in boards:
        boardnames.append(Board.objects.get(id = i))
    context = {
        "user":request.user,
        "names": boardnames,
        "message": message,
    }
    return render(request, "main/boards.html", context)

def bingo(request):
    bingos = (json.loads(request.body))['item']
    name = (json.loads(request.body))['name']
    nameid = (Board.objects.get(name = name)).id
    dict = (json.loads(request.body))
    board = Board.objects.get(name=name)
    boardid = board.id
    ts = time.time()
    dict['item'] = [dict['item']]
    dict['name'] = [dict['name']]
    dict['boardid'] = [boardid]
    dict['time'] = [ts]
    if board.isBingo(bingos):
        profile = Profile.objects.get(userid = request.user.id)
        if profile.bingos == "":
            profile.bingos=json.dumps(dict)
            profile.save()

        else:
            currentbingos = json.loads(profile.bingos)
            print(currentbingos['boardid'])
            print(name)
            if nameid in currentbingos['boardid']:
                data = json.dumps({"repeat": True})
                return HttpResponse(data, content_type='application/json')
            currentbingos['item'].append(bingos)
            currentbingos['name'].append(name)
            currentbingos['boardid'].append(boardid)
            currentbingos['time'].append(ts)
            profile.bingos = json.dumps(currentbingos)
            profile.save()
    data = json.dumps({"repeat": False})
    return HttpResponse(data, content_type='application/json')

def showbingos(request):
    if Profile.objects.get(userid = request.user.id).bingos == "":
        context = {
            "message": "You have no bingos yet"
        }
        return render(request, "main/message.html", context)
    bingos = json.loads(Profile.objects.get(userid = request.user.id).bingos)
    boards = bingos['boardid']
    boardlist = []
    for board in boards:
        boardlist.append(Board.objects.get(id=board))
    context = {
        'boardlist': boardlist,
    }
    return render(request, "main/bingos.html", context)

def getbingos(request):
    boardid = (json.loads(request.body))['id']
    dict = json.loads(Profile.objects.get(userid = request.user.id).bingos)
    dataarray = dict['item'][dict['boardid'].index(int(boardid))]
    data = json.dumps({ "item": dataarray})
    return HttpResponse(data, content_type='application/json')

def feed(request):
    posts = []
    boards = []
    following = json.loads(Profile.objects.get(userid = request.user.id).following)["following"]
    for id in following:
        for board in (Board.objects.filter(userid = id)):
            boards.append(board)
    length = len(boards)
    for i in range(0, length):
        for board in boards:
            max = 0
            maxindex = 0
            if board.time > max:
                max = board.time
                maxindex = boards.index(board)
        posts.append(boards[maxindex])
        boards.remove(boards[maxindex])
    context = {
        "boardlist": posts
    }
    return render(request, "main/feed.html", context)

def search(request):
    return render(request, "main/search.html")

def runsearch(request):
    result = []
    querey = request.POST["search"]
    result1 = (Profile.objects.filter(username__icontains=querey))
    for profile in result1:
        if profile != Profile.objects.get(userid = request.user.id):
            result.append(profile)
    context = {
        "result": result
    }
    return render(request, "main/results.html", context)

def userprofile(request, username):
    message = ""
    boardnames=[]
    boards = json.loads(Profile.objects.get(username = username).boards)["boards"]
    id = Profile.objects.get(username = username).userid
    global profileid
    profileid = id
    user = User.objects.get(id = id)
    for i in boards:
        boardnames.append(Board.objects.get(id = i))
    if boardnames == []:
        message = "This profile has no boards"
    context = {
        "user": user,
        "names": boardnames,
        "message": message,
    }
    return render(request, "main/userboards.html", context)

def showuserbingos(request, username):
    user = User.objects.get(username = username)
    global profileid
    profileid = user.id
    if Profile.objects.get(userid = user.id).bingos == "":
        context = {
            "user": User.objects.get(username = username),
            "message": "This profile has no bingos yet",
        }
        return render(request, "main/usermessage.html", context)
    bingos = json.loads(Profile.objects.get(userid = user.id).bingos)
    boards = bingos['boardid']
    boardlist = []
    for board in boards:
        boardlist.append(Board.objects.get(id=board))
    context = {
        'boardlist': boardlist,
        'user': user
    }
    return render(request, "main/userbingos.html", context)

def getuserbingos(request):
    boardid = (json.loads(request.body))['id']
    dict = json.loads(Profile.objects.get(userid = profileid).bingos)
    dataarray = dict['item'][dict['boardid'].index(int(boardid))]
    data = json.dumps({ "item": dataarray})
    return HttpResponse(data, content_type='application/json')

def follow(request):
    profile = Profile.objects.get(userid = request.user.id)
    userprofile = Profile.objects.get(userid = (json.loads(request.body))['id'])
    following = json.loads(profile.following)
    userfollowers = json.loads(userprofile.followers)
    requestid = json.loads(request.body)["id"]
    if  requestid in following["following"]:
        following["following"].remove(str(requestid))
        userfollowers["followers"].remove(str(request.user.id))
        profile.following = json.dumps(following)
        profile.save()
        userprofile.followers = json.dumps(userfollowers)
        userprofile.save()
        data = json.dumps({"following": False})
        return HttpResponse(data, content_type='application/json')
    if  requestid not in following["following"]:
        following["following"].append(requestid)
        userfollowers["followers"].append(str(request.user.id))
        profile.following = json.dumps(following)
        profile.save()
        userprofile.followers = json.dumps(userfollowers)
        userprofile.save()
        data = json.dumps({"following": True})
        return HttpResponse(data, content_type='application/json')

def isfollowing(request):
    name = json.loads(request.body)['name']
    id = Profile.objects.get(username = name).userid
    profile = json.loads((Profile.objects.get(userid = request.user.id).following))["following"]
    if str(id) in profile:
        data = json.dumps({"following": True})
    else:
        data = json.dumps({"following": False})
    return HttpResponse(data, content_type='application/json')

def delete(request, id):
    for profile in Profile.objects.all():
        if profile.bingos != "":
            bingos = json.loads(profile.bingos)
            for board in bingos["boardid"]:
                if board == int(id):
                    index = bingos["boardid"].index(board)
                    bingos["item"].remove(bingos["item"][0])
                    bingos["name"].remove(bingos["name"][0])
                    bingos["boardid"].remove(bingos["boardid"][0])
                    bingos["time"].remove(bingos["time"][0])
                    profile.save()
    pfile = Profile.objects.get(userid = request.user.id)
    pboards = json.loads(pfile.boards)["boards"]
    pboards.remove(int(id))
    if pboards == None:
        pboards = {"boards": []}
    pfile.boards = json.dumps({"boards": pboards})
    pfile.save()
    Board.objects.get(id = id).delete()
    return HttpResponseRedirect(reverse("boards"))
