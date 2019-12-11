import sys
import matplotlib.pyplot as plt
import matplotlib
import numpy as np


n = len(sys.argv)
for i in range(1, n):
    fileName = sys.argv[i]
    print("File: {}".format(fileName))
    groupFile = open(fileName, 'r')
    firstLine = True
    ranges = None
    tags = []
    for line in groupFile:
        if firstLine:
            ranges = line.split('-')
            firstLine = False
            continue

        lineSplit = line.split(':')
        if int(lineSplit[1]) > 10:
            tags.append((lineSplit[0], int(lineSplit[1])))
        
    tags = sorted(tags, key=lambda tag: -tag[1])
    for tag, count in tags: 
        print("\t{}:{}".format(tag, count))
    
    print("\n\n")

    labels = [tag[0] for tag in tags]
    counts = [tag[1] for tag in tags]

    x = np.arange(len(labels))  # the label locations
    width = 0.35  # the width of the bars

    fig, ax = plt.subplots()
    rects1 = ax.bar(x - width/2, counts, width)

    ax.set_ylabel('Counts')
    ax.set_title('Tag counts')
    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=90)
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

