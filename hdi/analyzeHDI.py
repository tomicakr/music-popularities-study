import sys
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import operator

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
                print("Sad sam na file-u {}".format(i+j))
                ranges = line.split('-')
                rangesTotal.append(ranges)
                firstLine = False
                if j==0:
                    print("0000000000000000000")
                    bigGroupRanges[0] = ranges[0]
                elif j==2:
                    print("2222222222222222222")
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

    labels = [tag[0] for tag in sortedBigGroupPercetage[:10]]
    counts = [tag[1] for tag in sortedBigGroupPercetage[:10]]

    for j in range(0,10):
        label, count = labels[j], counts[j]
        if label in genresDict.keys():
            groupsDict = genresDict[label]
            groupsDict[(i-groupFactor)] = count
        else:
            genresDict[label] = {(i-groupFactor):count}

    groupFactor += 2

    # x = np.arange(len(labels))  # the label locations
    # width = 0.35  # the width of the bars

    # fig, ax = plt.subplots()
    # rects1 = ax.bar(x - width/2, counts, width)

    # ax.set_ylabel('Counts')
    # ax.set_title('Tag counts')
    # ax.set_xticks(x)
    # ax.set_xticklabels(labels, rotation=90)
    # ax.legend()

    # def autolabel(rects):
    #     """Attach a text label above each bar in *rects*, displaying its height."""
    #     for rect in rects:
    #         height = rect.get_height()
    #         ax.annotate('{}'.format(height),
    #                     xy=(rect.get_x() + rect.get_width() / 2, height),
    #                     xytext=(0, 3), 
    #                     textcoords="offset points",
    #                     ha='center', va='bottom')

    # #autolabel(rects1)
    # fig.tight_layout()
    # plt.show()
print(genresDict)
genres = genresDict.keys()

labels = genres

x = np.arange(len(labels))  # the label locations
width = 0.7  # the width of the bars

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

# for key in genresDict.keys():
#     a = 0
#     for i in range(1,6):
#         if i in genresDict[key]:
#             groupDictPerGenre[i-1][a] = genresDict[key][i]
#     a += 1

# print(groupDictPerGenre)
# a=0
# print(x)
# for i in range(5):
#     rects1 = ax.bar((x-width/len(labels))*(a), groupDictPerGenre[i], width, label=key)
#     a+=1

ax.set_ylabel('Percent')
ax.set_title('Percentage of tags in attribute groups')
ax.set_xticks(x)
ax.set_xticklabels(labels, rotation=45)
ax.legend()

def autolabel(rects):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect in rects:
        height = rect.get_height()
        ax.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3), 
                    textcoords="offset points",
                    ha='center', va='bottom')

#autolabel(rects1)
fig.tight_layout()
plt.show()
