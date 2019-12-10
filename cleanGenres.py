

f = open("genres.txt", "r")
o = open("genres_clean.txt", "w")

for line in f:
    newLine = line.replace("-", " ").lower()
    genres = newLine.split("/")
    for g in genres:
        o.write("{}\n".format(g.strip()))
