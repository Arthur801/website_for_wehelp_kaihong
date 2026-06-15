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



print("==========Task 2==========")