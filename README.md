## Compare HDI and depression rates in countries to the genre popularity of music tracks


## ABOUT THE PROJECT
Our application studies how Human Development Index (HDI) and depression rates affect music preferences all around the world.  
The HDI is a statistic composite index of life expectancy, education, and per capita income indicators, which are used to rank countries into four tiers of human development. A country scores a higher HDI (between 0 and 1) when the lifespan is higher, the education level is higher, and the gross national income GNI per capita is higher. Moreover, we tried to associate this index with the depression rates of each country in order to understand if these two affect the music genre popularity.


## DATASETS
In our project we used many datasets. The first one was taken from "last.fm Web Services": we used their API, after getting signed up and once obtained the key to use them, to get the information we needed about music distribution all over the world. The API methods we used were "geo.getTopTracks" (in order to get the most popular tracks on Last.fm about last week by country) and "track.getInfo" (in order to get the metadata for a track on Last.fm using the artist/track name).
The next step was to obtain the HDI indexes. We downloaded them from [here](http://hdr.undp.org/en/data); we had to choose “Dimension”: HDI, then again HDI on the next picker and then download data underneath.
We downloaded the depression rates data from [here](https://ourworldindata.org/mental-health) other website. The newest data is from year 2017, so we based our research on the results we got for that year.
Another dataset that was used is a list with almost 900 of the most famous music genres.


## TARGETS
With our project we wanted to show informations that could be useful for people interested in the argument, since it is for research purposes only.
Our main aim was to see if music genre popularities are affected by the "human growth level" and the depression rate in each country. In simple terms, if we have a country with a low level of HDI and a high depression rate, we wanted to check if the most popular genres there are the one considered more "sad" or "emotional". At the same time, a country which has got a high score of HDI and a low depression rate might listen to "happy" genres like pop, commercial and so on.
To conclude, since music is listened all over the world, we tried to understand if the spreadest genres in each country are related to "how people feel" internally, to how they live and to how they are used to see the world in their environment.



## WHY THE NEED FOR BIG DATA?
Our project has to work with a huge amount of data and a simple application wouldn't have been suitable for many reasons.
First of all, the music data: we had so many tracks, genres (around 900), artists for each country (around 194) and, moreover, we needed to process it in order to get usable results to be compared with other data taken from a totally different field, the HDI index and the depression rate (each one of these for each nation in the world). It sounds pretty clear that we couldn't have developed an application like this using simple coding or loops, since the response time would have been whopping.
To solve this problem, we used two services: the Amazon Web Servers, which provided us a cluster on which we runned the code, and Apache Spark, a unified analytics engine for large-scale data processing.


## HOW DOES IT WORK?
The project is based on the map-reduce model, using as programming language Python. We developed many phases to reach the final result. 
In order to work with the datasets we had to do a lot of data cleaning:
First of all the music data: as the API could not give us music genres of each song we had to use the tags through track.getInfo. These tags could be many different things, for example the artist or song name, the year it was published or other things that are associated with the song. To find genres in these tags we first cleaned them so that all of the data has the same structures (e.g. no capital letters or special signs like "-"). Then we used the other list with the cleaned genres to compare each tag of a song. The genres would then be added up per country. 
The HDI and depression rates datasets also had to be cleaned before usage. The depression rates dataset gives values for the last 15 years of each country so we only used the most recent value as it is most accurate.

## WORKFLOW
Now we're going to explain how we moved through the code and the guideline followed:
- Extract tags from last.fm API per country:
```              
def getSongInfo(mbid):
    return requests.get("http://ws.audioscrobbler.com/[...]_
                
                
def tagsExtractor(track):
    mbid = track['mbid'].replace('"', '')
    ...
    if 'track' in response.keys():
       topTagsAndLinks = response['track']['toptags']['tag']
       tags = []
       for tagsAndLinks in topTagsAndLinks:
           tags.append(tagsAndLinks['name'])
           ...
       return tags
                  
              
def createGroups(country_attribute):
    country_attribute = country_attribute.sortBy(lambda x: x[1]).collect()
    number_of_groups = 15
    number_of_countries = int(len(country_attribute)/number_of_groups)
    country_attribute_groups = []
    ... 

    return country_attribute_groups
                   
 ```               
 - Cleanup data and filter tags:
 ```
  def cleanup(tag_number):
     tag, number = tag_number
     newTag = tag.replace("-", " ").lower()
     return newTag, number
                             
     genres_clean = sc.textFile('genres_clean.txt')

     for line in genres_clean.collect():
     genres_dict[line] = 0
     ...

     for gt in depressionGroupsTags.collect():

     tag, number = gt
     if tag in genres_dict.keys():
        genres_dict[tag] = number
                   
```                   
- Count the genres per group of countries:
```
   for key in genres_dict.keys():
       if genres_dict[key] != 0:
          groupOut.write("{}:{}\n".format(key, genres_dict[key]))
```

## USAGE OF THE APPLICATION
In order to use the application properly, here we show you many guidelines:

**Installing python-pip:**
    _sudo apt install python-pip_

**Installing requests:**
    _pip install requests_

**Installing numpy:**
    _pip install numpy_

**Installing matplotlib:**
    _pip install matplotlib_

**Starting the depression rate calculations**:
    _spark-submit ./calcDepression.py_

**Starting the hdi calculations**:
    _spark-submit ./calcHDI.py_

**Displaying the depression graph**:
    _python ./depression/analyzeDepression.py 15_

**Displaying the hdi graph**:
    _python ./hdi/analyzeHDI.py 15_

The lastFM API key is already hardcoded in the _trackGrouping.py_ file, the one  which is found inside can be used.
The groups will appear in the corresponding folders, but they are also already pushed in the repository.
 
 
                 
## CONCLUSIONS                  
Seeing our results, we can say that music genres aren't strictly correlated with HDI and depression rates, cause the world's tastes are more or less the same worldwide, fact which also justifies the global popularity of many artists, leaders of the genre they represent.
An higher correlation can be seen on many minor genres: in average, countries with an high HDI are more likely to hear new genres as we can see in the graph (for example with "funk") and countries with the lowest HDI are more likely to listen to "street" and "urban" genres, like rap.
The depression rate doesn't affect that much our studies because, as already said, the most famous genres are the same everywhere. The only thing we can conclude from it is that countries more incline to be depressed listen to many subgeneres that countries less depressed don't. 
Basing ourselves on these facts, to conclude, we can say that life expectancy, education, per capita income indicators and depression rates don't indicate accurately what people listen to, but they can point out how every country explores musical genres beyond the most famous ones.



## AUTHORS
This application has been developed as final project for the subject "Cloud y Big Data" by five Erasmus students at the Universidad Complutense de Madrid:
- Tomislav Kravaršćan
- Simon Markmann
- Valerio Moroni
- Ena Rajković
- Yurii Shcheholiev

