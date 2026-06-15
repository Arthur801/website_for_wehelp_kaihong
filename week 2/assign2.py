#task 1
def func1(name):
    # coordinate of characters dictionary
    chrcoord1 = {"悟空":(0, 0), "辛巴":(-3, 3), "特南克斯":(1, -2), "貝吉塔":(-4, -1), "丁滿":(-1, 4), "弗利沙":(4, -1)}
    resultDict = {}             # Use dictionary to store the result data {distance:name}
    minDist =  float('inf')     # minimum distance
    maxDist = 0                 # maximum distance

    #pair the characters with distances
    for key in chrcoord1:
        dist = abs(chrcoord1[name][0]-chrcoord1[key][0]) + abs(chrcoord1[name][1]-chrcoord1[key][1])
        # determine whether above or below the line through (3, -2), (-1, 3) 5x+4y-7=0
        if (5*chrcoord1[name][0]+4*chrcoord1[name][1]-7>0 and 5*chrcoord1[key][0]+4*chrcoord1[key][1]-7<0) or (5*chrcoord1[name][0]+4*chrcoord1[name][1]-7<0 and 5*chrcoord1[key][0]+4*chrcoord1[key][1]-7>0):
            dist+=2
        resultDict[dist] = resultDict.get(dist, [])
        resultDict[dist].append(key)
    
    # Find max distance and min distance
    for key in resultDict:
        if key < minDist and key != 0:
            minDist = key
        if key > maxDist:
            maxDist = key
    print("最遠%s;最近%s" % ("、".join(resultDict[maxDist]), "、".join(resultDict[minDist])))


print("==========Task 1==========")
func1("辛巴")
func1("悟空")
func1("弗利沙")
func1("特南克斯")


# task 2
schedule = None
def func2(ss, start, end, criteria):
    global schedule
    if schedule == None:
        schedule = [[False] * 24 for s in range(len(ss))]# record the schedule of ss
    
    closest = [None, float("inf"), -1]

    if criteria[0] == "c":
        if criteria[1:3] == ">=":
            c = int(criteria[3:])
            for i in range(len(ss)):
                closest_dist = abs(ss[i]["c"]-c)
                if ss[i]["c"] >= c and closest_dist < closest[1] and all(t == False for t in schedule[i][start:end+1]):
                    closest = [ss[i], closest_dist, i]
            if closest[0] != None:
                schedule[closest[2]][start:end] = [True]*(end-start)
                print(ss[closest[2]]["name"])
            else:
                print("Sorry")
        elif criteria[1:3] == "<=":
            c = int(criteria[3:])
            for i in range(len(ss)):
                closest_dist = abs(ss[i]["c"]-c)
                if ss[i]["c"] <= c and closest_dist < closest[1] and all(t == False for t in schedule[i][start:end+1]):
                    closest = [ss[i], closest_dist, i]
            if closest[0] != None:
                schedule[closest[2]][start:end] = [True]*(end-start)
                print(ss[closest[2]]["name"])
            else:
                print("Sorry")
        elif criteria[1] == "=":
            c = int(criteria[2:])
            for i in range(len(ss)):
                closest_dist = abs(ss[i]["c"]-c)
                if ss[i]["c"] == c and closest_dist < closest[1] and all(t == False for t in schedule[i][start:end+1]):
                    closest = [ss[i], closest_dist, i]
            if closest[0] != None:
                schedule[closest[2]][start:end] = [True]*(end-start)
                print(ss[closest[2]]["name"])
            else:
                print("Sorry")
        else:
            print("err")
    elif criteria[0] == "r":
        if criteria[1:3] == ">=":
            r = float(criteria[3:])
            for i in range(len(ss)):
                closest_dist = abs(ss[i]["r"]-r)
                if ss[i]["r"] >= r and closest_dist < closest[1] and all(t == False for t in schedule[i][start:end+1]):
                    closest = [ss[i], closest_dist, i]
            if closest[0] != None:
                schedule[closest[2]][start:end] = [True]*(end-start)
                print(ss[closest[2]]["name"])
            else:
                print("Sorry")
        elif criteria[1:3] == "<=":
            r = float(criteria[3:])
            for i in range(len(ss)):
                closest_dist = abs(ss[i]["r"]-r)
                if ss[i]["r"] <= r and closest_dist < closest[1] and all(t == False for t in schedule[i][start:end+1]):
                    closest = [ss[i], closest_dist, i]
            if closest[0] != None:
                schedule[closest[2]][start:end] = [True]*(end-start)
                print(ss[closest[2]]["name"])
            else:
                print("Sorry")
        elif criteria[1] == "=":
            r = float(criteria[2:])
            for i in range(len(ss)):
                closest_dist = abs(ss[i]["r"]-r)
                if ss[i]["r"] == r and closest_dist < closest[1] and all(t == False for t in schedule[i][start:end+1]):
                    closest = [ss[i], closest_dist, i]
            if closest[0] != None:
                schedule[closest[2]][start:end] = [True]*(end-start)
                print(ss[closest[2]]["name"])
            else:
                print("Sorry")
        else:
            print("err")
    elif criteria[0:4] == "name":
        for i in range(len(ss)):
            if ss[i]["name"] == criteria[5:] and all(t == False for t in schedule[i][start:end+1]):
                schedule[i][start:end] = [True]*(end-start)
                print(ss[i]["name"])
        else:
            print("Sorry")
    else:
        print("err")
    
        
services = [
    {"name":"S1", "r":4.5, "c":1000},
    {"name":"S2", "r":3, "c":1200},
    {"name":"S3", "r":3.8, "c":800}
]
print("==========Task 2==========")
func2(services, 15, 17, "c>=800")
func2(services, 11, 13, "r<=4")
func2(services, 10, 12, "name=S3")
func2(services, 15, 18, "r>=4.5")
func2(services, 16, 18, "r>=4")
func2(services, 13, 17, "name=S1")
func2(services, 8, 9, "c<=1500")

# task 3
def func3(index):
    # The rule of number sequence : (-2, -3, +1, +2)*n
    num = 25
    match index%4:
        case 0:
            print(num - 2*(index//4))
        case 1:
            print(num - 2*(index//4) - 2)
        case 2:
            print(num - 2*(index//4) - 5)
        case 3:
            print(num - 2*(index//4) - 4)
        case _:
            print("error")
            return -1


print("==========Task 3==========")
func3(1);
func3(5);
func3(10);
func3(30);


# task 4
def func4(sp, stat, n):

    minSp = float("inf")
    minSpIdx = -1
    for i in range(len(sp)):
        if stat[i] == '0' and sp[i] >= n and sp[i] < minSp:
            minSp = sp[i]
            minSpIdx = i
    if minSpIdx != -1:
        print(minSpIdx)
    else:
        sumSp = 0
        spSortedList = []
        maxSp = 0
        maxSpIdx = -1
        for i in range(len(sp)):
            if stat[i] == '0' and sp[i] > 0:
                sumSp += sp[i]
                spSortedList.append(sp[i])
                if sp[i] > maxSp:
                    maxSpIdx = i
        if sumSp >= n:
            spSortedList.sort()
            print(maxSpIdx)
        else:
            print("Not enough space!")


print("==========Task 4==========")
func4([3, 1, 5, 4, 3, 2], "101000", 2)
func4([1, 0, 5, 1, 3], "10100", 4)
func4([4, 6, 5, 8], "1000", 4)