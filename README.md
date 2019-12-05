## Compare HDI and depression rates in countries to the genre popularity of music tracks


## ABOUT THE PROJECT
Our application has as main target letting people understand how the Human Development Index (HDI) and the depression rates influence music preferences all around the world.  
The HDI is a statistic composite index of life expectancy, education, and per capita income indicators, which are used to rank countries into four tiers of human development. A country scores a higher HDI when the lifespan is higher, the education level is higher, and the gross national income GNI per capita is higher. Moreover, we tried to associate this index with the depression rates of each country across the world in order to understand if these two affect the music genre popularity.


## DATASETS
In our project we used many datasets. The first one was taken from "last.fm Web Services": we exploited some of their API, after getting signed up and once obtained the key to use them, to get the informations we needed about music distribution all over the world. The API methods we used were "geo.getTopTracks" (in order to get the most popular tracks on Last.fm about last week by country) and "track.getInfo" (in order to get the metadata for a track on Last.fm using the artist/track name).
The next step was to obtain the HDI indexes. We downloaded them from here: http://hdr.undp.org/en/data; we had to choose “Dimension”: HDI, then again HDI on the next picker and then download data underneath.
We downloaded the depression rates data from [this](https://ourworldindata.org/mental-health) other website. The newest data is from year 2017, so we based our research on the results we got for that year.


## HOW DOES IT WORK?
The project is based on the map-reduce mode, using as programming language Python. We developed many phases to reach the final result.
