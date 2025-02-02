import sys
import matplotlib.pyplot as plt
import matplotlib
import numpy as np

n = int(sys.argv[1])
genresDict = {}
groupFactor = 0
rangesTotal = []

allBigGroupRanges = []
for i in range(1, n+1, 3):
    bigGroupDict = {}
    bigGroupRanges = [0,0]
    totalTagsCount = 0
    for j in range(0, 3):
        fileName = "group_{}".format(i+j)
        print("File: {}".format(fileName))
        groupFile = open(fileName, 'r')
        firstLine = True
        ranges = None
        tags = []
        for line in groupFile:
            if firstLine:
                ranges = line.split('-')
                rangesTotal.append(ranges)
                firstLine = False
                if j==0:
                    bigGroupRanges[0] = ranges[0]
                elif j==2:
                    bigGroupRanges[1] = ranges[1]
                continue

            tag, count = line.split(':')
            count = int(count)
            totalTagsCount += count
            if tag in bigGroupDict.keys():
                bigGroupDict[tag] = bigGroupDict[tag] + count
            else:
                bigGroupDict[tag] = count
    allBigGroupRanges.append(bigGroupRanges)

    bigGroupDictPercetage = {}
    for key in bigGroupDict.keys():
        bigGroupDictPercetage[key] = float(bigGroupDict[key])*100/totalTagsCount

    sortedBigGroupPercetage = sorted(bigGroupDictPercetage.items(), key=lambda kv: -kv[1])
    for tag, count in sortedBigGroupPercetage: 
        print("\t{}:{}".format(tag, count))
    
    print("\n\n")

    labels = [tag[0] for tag in sortedBigGroupPercetage[:15]]
    counts = [tag[1] for tag in sortedBigGroupPercetage[:15]]

    for j in range(0,10):
        label, count = labels[j], counts[j]
        if label in genresDict.keys():
            groupsDict = genresDict[label]
            groupsDict[(i-groupFactor)] = count
        else:
            genresDict[label] = {(i-groupFactor):count}

    groupFactor += 2

    x = np.arange(len(labels))
    width = 0.5

    fig, ax = plt.subplots()
    rects1 = ax.bar(x, counts, width)

    ax.set_ylabel('Percentages')
    ax.set_title('The percentages of tags per genre')
    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=45)

    fig.tight_layout()
    plt.show()


print(genresDict)
genres = genresDict.keys()
labels = genres
x = np.arange(len(labels))
width = 0.7
fig, ax = plt.subplots()

groupDictPerGenre = [[0 for _ in range(len(labels))] for i in range(5)]
print(x)
for i in range(1,6):
    a=0
    for key in genresDict.keys():
        if i in genresDict[key]:
            groupDictPerGenre[i-1][a] = genresDict[key][i]
        a+=1

    print(groupDictPerGenre[i-1])
    rects1 = ax.bar(x + (i-3)*(width/5), groupDictPerGenre[i-1], width/5, label="Group {}: range {}-{}".format(i, round(float(allBigGroupRanges[i-1][0]),3), round(float(allBigGroupRanges[i-1][1]),3)))

ax.set_ylabel('Percent')
ax.set_title('Percentage of tags in attribute groups')
ax.set_xticks(x)
ax.set_xticklabels(labels, rotation=45)
ax.legend()

fig.tight_layout()
plt.show()
