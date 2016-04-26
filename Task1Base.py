
import sys
import os

def common_friends(userId_1, userId_2, graph):
    neighborhood_1 = set(graph[userId_1])
    neighborhood_2 = set(graph[userId_2])

    c_friends = list(neighborhood_1 & neighborhood_2)
    return len(c_friends)

def jaccard(userId_1, userId_2, graph):
    neighborhood_1 = set(graph[userId_1])
    neighborhood_2 = set(graph[userId_2])
    c_friends = neighborhood_1 & neighborhood_2
    all_friends = neighborhood_1 | neighborhood_2

    return len(c_friends) / len(all_friends)


def mask_open(mask):
    opened = bin(mask)[2:]
    opened = '0' + opened[-1::-1] + '0'*20
    return opened


def prediction_function(demog, graph, write_file):
    for userId, neighbohood in graph.items():
        try:
            if demog[userId] != None:
                continue
        except:
            print('Age for user {} have to be predicted'.format(userId))
        for friendId in neighbohood:
            common_score = common_friends(userId, friendId, graph)
            jaccard_score = jaccard(userId, friendId, graph)
            pass



def bl(graph, demog, fd=False):
    res = list()
    count = int(0)

    for pId, conns in graph.items():
        count += 1
        if count % 1000 == 0:
            print(count)
        dateSum = 0
        totalLen = 0
        maxBDp = 0
        minBDp = sys.maxint
        print(pId)
        try:
            if demog[pId] is not None:
                continue
        except:
            print("good")
        if type(conns) == int:
            conns = [conns]
        for links in conns:
            totalLen += 1
            try:
                bd = int(demog[links])
            except:
                bd = sys.maxint

            if bd == sys.maxint:
                continue
            if bd > maxBDp:
                maxBDp = bd
            if bd < minBDp:
                minBDp = bd
            dateSum += int(bd)

        if (totalLen == 0):
            continue
        if (totalLen >= 4):
            avg = (dateSum - maxBDp - minBDp) / (totalLen - 2)
        else:
            avg = (dateSum) / (totalLen)
        res.append([pId, avg])
        if (fd):
            fd.write(str(pId) + '\t' + str(avg) + '\n')
    return res


from GraphParser import graphParser

cols = list()
cols.append("userId")
cols.append("birth_date")
(demog, fd) = graphParser.parseFolderBySchema(os.path.join("Task1", "Task1",
                                                           "trainDemography"), 0, "",
                                              "userId", cols, True)

cols = list()
cols.append("from")
cols.append("to")
cols.append("links")
cols.append("mask")
(graph, fd) = graphParser.parseFolderBySchema(os.path.join("Task1", "Task1", "graph"),
                                              0, "", "from", cols,
                                              True)
print("data loaded")
fdres = open("results.txt", 'w')
bl(graph, demog, fdres)
