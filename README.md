## Compare HDI and depression rates in countries to the genre popularity of music tracks


## ABOUT THE PROJECT
Our application has as a main target to find out if there are any correlations between the Human Development Index (HDI) or depression rates per country and music preferences all around the world.  
The HDI is a statistic composite index of life expectancy, education, and per capita income indicators, which are used to rank countries into four tiers of human development. A country scores a higher HDI (between 0 and 1) when the lifespan is higher, the education level is higher, and the gross national income GNI per capita is higher. Moreover, we tried to associate this index with the depression rates of each country across the world in order to understand if these two affect the music genre popularity.


## DATASETS
In our project we used many datasets. The first one was taken from "last.fm Web Services": we used their API, after getting signed up and once obtained the key to use them, to get the information we needed about music distribution all over the world. The API methods we used were "geo.getTopTracks" (in order to get the most popular tracks on Last.fm about last week by country) and "track.getInfo" (in order to get the metadata for a track on Last.fm using the artist/track name).
The next step was to obtain the HDI indexes. We downloaded them from [here](http://hdr.undp.org/en/data); we had to choose “Dimension”: HDI, then again HDI on the next picker and then download data underneath.
We downloaded the depression rates data from [here](https://ourworldindata.org/mental-health) other website. The newest data is from year 2017, so we based our research on the results we got for that year.
Another dataset that was used is a list with almost 900 of the most famous music genres.


## HOW DOES IT WORK?
The project is based on the map-reduce mode, using as programming language Python. We developed many phases to reach the final result. 
In order to work with the datasets we had to do a lot of data cleaning:
First of all the music data: as the api could not give us music genres of each song we had to use the tags via track.getInfo. These tags could be many different things, for example the artist or song name, the year it was published or other things that are associated with the song. To find genres in these tags we first cleaned them so that all of the data has the same structures (e.g. no capital letters or special signs like "-"). Then we used the other list with the cleaned genres to compare each tag of a song. The genres would then be added up per country. 
The HDI and depression rates datasets also had to be cleaned before usage. The depression rates dataset gives values for the last 15 years of each country so we only used the most recent value as it is most accurate.
