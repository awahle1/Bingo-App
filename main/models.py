from django.db import models
from django.contrib.auth.models import User
import json

# Create your models here.
class Board(models.Model):
    info = models.CharField(
        default = "",
        max_length = 10000
    )
    userid = models.IntegerField(
        default = 0,
        null=True,
        blank=True
    )
    username = models.CharField(
        default = "",
        max_length = 10000
    )
    time = models.IntegerField(
        default = 0,
        null=True,
        blank=True
    )
    name = models.CharField(
        default = "",
        max_length = 30
    )
    def getInfo(self):
        board = [[], [], [], [], []]
        info = self.info
        for i in range(0,5):
            for j in range(0,5):
                board[i].append(info[0:(info.find(','))])
                info = info[(info.find(',')+1):]
        return(board)
    def isBingo(self, bingos):
        board = self.getInfo()
        columns = [[], [], [], [], []]
        for column in columns:
            for row in board:
                column.append(row[columns.index(column)])
        for row in board:
            for item in row:
                if item not in bingos:
                    break
                else:
                    if row.index(item)==4:
                        return(True)
        for column in columns:
            for item in column:
                if item not in bingos:
                    break
                else:
                    if column.index(item)==4:
                        return(True)
        return (False)

class Profile(models.Model):
    boards = models.CharField(
        default = json.dumps({'boards':[]}),
        max_length = 100000,
    )
    bingos = models.CharField(
        default = "",
        max_length = 100000,
    )
    userid = models.IntegerField(
        default = 0,
        null=True,
        blank=True
    )
    username = models.CharField(
        default = "",
        max_length = 100000,
    )
    followers = models.CharField(
        default = json.dumps({"followers":[]}),
        max_length = 100000,
    )
    following = models.CharField(
        default = json.dumps({"following":[]}),
        max_length = 100000,
    )
    def getBoards(self):
        boardlist = self.boards
        boards = []
        while "," in boardlist:
            boards.append(boardlist[1:boardlist.find(',')])
            boardlist = boardlist[boardlist.find(',')+1:]
        return (boards)
    def getFollowers(self):
        followerlist = self.followers
        followers = []
        while "," in followerlist:
            followers.append(followerlist[1:followerlist.find(',')])
            followerlist = followerlist[followerlist.find(',')+1:]
        return (followers)

    def getFollowing(self):
        followinglist = self.following
        following = []
        while "," in followinglist:
            following.append(followinglist[1:followinglist.find(','):])
            followinglist = followinglist[followinglist.find(',')+1:]
        return (following)
