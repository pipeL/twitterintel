# Twitter Intel

##DataBase
https://www.mongodb.org/ -> MongoDB is the next-generation database that lets you create applications never before possible

https://api.mongodb.org/python/current/ -> Python distribution containing tools for working with MongoDB

##Multi-process
http://kafka.apache.org/ -> Publish-subscribe messaging rethought as a distributed commit log

http://storm.apache.org/ -> Free and open source distributed realtime computation system

https://github.com/AirSage/Petrel -> Petrel offers some important improvements over the storm.py module provided with Storm

##Twitter
http://www.tweepy.org/ -> Python library for accessing the Twitter API


##Web
http://webpy.org/ -> Web framework for Python that is as simple as it is powerful

https://jquery.com/ -> jQuery is a fast, small, and feature-rich JavaScript library

https://dc-js.github.io/dc.js/ -> Javascript charting library with native crossfilter support and allowing highly efficient exploration on large multi-dimensional dataset (inspired by crossfilter's demo)

http://square.github.io/crossfilter/ -> Crossfilter is a JavaScript library for exploring large multivariate datasets in the browser






##Directory Details

Twitter Intel [ Site , console-analazy , python-service , topology [ TopologyBad , TopologyGood , TopologySpam ]

###Site

Simple html website for service interaction
Steps:
Index Page -> Insert words to track in twitter feed
           -> Tweets apper to analyze
           -> Analyze each tweet
           -> Submit data for analyze
           -> Redirect to tweets.html page
Tweets Page -> Start Feed will start getting tweets from twitter and classifie them based on user classification and vaderSentiment library from nltk
            ->Start div will show all tweets with classification
            
TopWords Page -> Graphs with top words from each classification (good, bad , spam)
ContagemTotal Page -> Total count of good, bad , spam tweets based on user classification

###Console-Analazy
Linux terminal interface same application as PythonService 

###Python-Service
Directory containing all .py files needed to provide information to WebSite 
Contain also the service consumed by website in order to provide information and get information from the user

###Topology
Contains the 3 topology's needed to separate and count words (1 word , 2 words , 3 words)
Same topology different uses - Good , Bad , Spam
Each topology will consume the tweet's from kafka topic's and divide the tweet into words for counting







