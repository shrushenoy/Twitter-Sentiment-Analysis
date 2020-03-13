"""                                 TITLE: 
Twitter Sentiment Analysis of Attitudes About Measles Vaccinations for 2019 Measles Outbreak

"""
'''                               Citations 
Matplotlib. (2019). Matplotlib version 3.0.3. Retrieved from https://atplotlib.org/
TextBlob. (2018). Tutorial: Quickstart Sentiment Analysis. Retrieved from https://textblob.readthedocs.io/en/dev/quickstart.html#sentiment-analysis
Tweepy. (2019). Retrieved from http://docs.tweepy.org/en/3.7.0/
Hutto, C.J., Gilbert, E.E. (2014). VADER: A Parsimonious Rule-based Model for Sentiment Analysis of Social Media Text. Eighth International Conference on Weblogs and Social Media (ICWSM-14). Ann Arbor, MI, June 2014.
'''

"""*****     PART 1: To retrive tweets from twitter using twitter API        ******"""
'''Coder: Shruti'''
import tweepy
import csv
import twitter_credentials    #twitter_credentials is file where twitter credentials are stored

'''           Retriving data from Twitter & storing in 2 files              '''               
##             Providing the twitter credential and authority                   ##
auth = tweepy.OAuthHandler(twitter_credentials.consumer_key, twitter_credentials.consumer_secret)
auth.set_access_token(twitter_credentials.access_token, twitter_credentials.access_token_secret)
api = tweepy.API(auth)

##                          Reading tweets                                      ##
class StreamListener(tweepy.StreamListener):
    def on_status(self, status):
        print(status.text)

##             Retrieving data and saving it to measles_hashtag.csv file         ##
csvFile = open('/../measles_hashtag.csv', 'w')
csvWriter = csv.writer(csvFile)
##   Filtering the tweet with hash_tag, language, and retriving data from 03/26 to 04/03  ##
hash_tag = [ "Measles", "Vaccine", "2019"]

for tweet in tweepy.Cursor(api.search,  
                           q=hash_tag, count = 1000,
                           since = "2019-03-26",
                           until="2019-04-03",
                           lang="en").items():
    print(tweet.created_at, tweet.text)
    csvWriter.writerow([tweet.created_at, tweet.text.encode('utf-8')])
 
##          Retrieving data for #Vaccine and saving it to Vaccination.csv file    ##
csvFile1 = open('/../Vaccination.csv', 'w')
csvWriter1 = csv.writer(csvFile1)

##   Filtering the tweet with #Vaccine, language, and retriving data from 03/26 to 04/03  ##
for tweet1 in tweepy.Cursor(api.search,
                           q="#Vaccine", count = 1000,
                           since = "2019-03-26",                            
                           until="2019-04-03",
                           lang="en").items():
    print(tweet1.created_at, tweet1.text)
    csvWriter1.writerow([tweet1.created_at, tweet1.text.encode('utf-8')])


"""*****             PART 2: Data Cleaning for both the files                *****"""    
'''Coder: Shruti'''
####                      Cleaning data from measles_hashtag.csv file             ####

import csv
import re
##  It was easier to clean the data when stored in list, so we convert the data into list 
##  and then perform data cleaning on that list and the store it back to original csv file

with open('/../measles_hashtag.csv', 'r') as f:
    reader=csv.reader(f)
    your_list= list(reader)                 # list() converts the data into list
print(your_list)

final_list=[]
for i in your_list:
    final_list.append(i)
print(final_list)

##  In the csv file, alternate rows where null, the code below removes the empty rows and 
##  appends our final list
final_list=list(filter(None, final_list))   
print(final_list)

final_list_version1=[]
for i in final_list:
    for j in i:
        final_list_version1.append(j)

##  We filter the tweet dates as it is not required for out analysis purpose
for i in final_list_version1:
    if '2019' in i:
        final_list_version1.remove(i) 
print(final_list_version1)

##  Removing user names, twitter handles and URL's  
final_list_version2=[]
for i in final_list_version1:
    i=' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)"," ",i).split())
    final_list_version2.append(i)
print(final_list_version2)

## Seprating each word for making it easier to remove the stop_words
final_list_version3=[]
for i in final_list_version2:
    i=i.split(" ")
    final_list_version3.append(i)
print(final_list_version3)

##  Identifying the unwanted words and emoji's mentioned in Stop_word to remove it 
stop_word =  ['x9f', 'x93', 'x9f', 'xac', 'x9f', 'x93', 'x9f','x82', "x99m", "xa9", "x9d", 'http',
             "gt", "xe2", "x99m", "['']", "xa6","000","x80", "x99m", "b", 'RT', "xe2", "x81", "x99re",
              'xf0','x9f','x98','xac','xf0','x9f','xa4','x93', 'qu', 'x99s','xa6', 'x9f','x8d', "x99",
              'x81', 'n', 'nFirst', 'xa6', "x9c", "x9cimmune" ]

final_list_version4=[]
for i in final_list_version3:               #This outer for loop reads each list 
    for j in i:                             #This inner for loop reads each word within the list
        if j in stop_word:                  #This if statement checks if the word matches to any word listed in stop_word
            i.remove(j)                     #If the word matches any word from stop_word list, it will remove the word 
    final_list_version4.append(i)           
print(final_list_version4)    

##  As the stop_word list was big, split the list and repeated cleaning of non text characters  
remove_words = ['xa0Axios', 'x9cThere', 'B','C', 'x9cHealth','c', 'P','S', 'x80', 'x9cviral', 'RT', 
                 'xa0measles', 'x99t',  'x81', 's', 'x94', 'xf0', 'x90', 'x9f','x92', 'x89', 'http', 
                 'xe2', 'xa9', 'xa02000', 'xa8', "xc2",  'x9cYou', 'x99ve', 'xa6', 'xa2','x9coutbreaks',
                 'x9cNation', 'x9cThe','xa0debate', 'x9cOutbreaks','x9cThe','x9cNation', 'x8f', 'x8c', 
                 'x9a', 'A', 'x9Cviral' ]

final_list_version5=[]
for i in final_list_version4:               #This outer for loop reads each list 
    for j in i:                             #This inner for loop reads each word within the list
        if j in remove_words:               #This if statement checks if the word matches to any word listed in remove_words
            i.remove(j)                     #If the word matches any word from remove_words list, it will remove the word 
    final_list_version5.append(i)
print(final_list_version5)    

##  Removing repetative tweets 
final_list_version6=[]
for i in final_list_version5:
    if i not in final_list_version6:
        final_list_version6.append(i)
print(final_list_version6) 

##  Storing the clean data back to clean_measles_hashtag file
import pandas as pd
df = pd.DataFrame(final_list_version6)
df.to_csv("/../clean_measles_hashtag.csv",index=False)

## Performing sentiment analysis was easier in .txt file, converted .csv to .txt file
df.to_csv('/../clean_measles_hashtag_txt.txt', sep='\t', index=False)


####                      Cleaning data from Vaccination.csv file                 ####
'''Coder: Shruti'''
import csv
import re

##  It was easier to clean the data when stored in list, so we convert the data into list 
##  and then perform data cleaning on that list and the store it back to original csv file

with open('/../Vaccination.csv', 'r') as v:
    reader=csv.reader(v)
    vaccinate_list= list(reader)         # list() converts the data into list
print(vaccinate_list)

final_vac=[]
for i in vaccinate_list:
    final_vac.append(i)
print(final_vac)

##  In the csv file, alternate rows where null, the code below removes the empty rows and 
##  appends our final list

final_vac=list(filter(None, final_vac))
print(final_vac)

final_vac_version1=[]
for i in final_vac:
    for j in i:
        final_vac_version1.append(j)

##  We filter the tweet dates as it is not required for out analysis purpose        
for i in final_vac_version1:
    if '2019' in i:
        final_vac_version1.remove(i) 
print(final_vac_version1)

##  Removing user names, twitter handles and URL's  
final_vac_version2=[]
for i in final_vac_version1:
    i=' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)"," ",i).split())
    final_vac_version2.append(i)
print(final_vac_version2)

## Seprating each word for making it easier to remove the stop_words
final_vac_version3=[]
for i in final_vac_version2:
    i=i.split(" ")
    final_vac_version3.append(i)
print(final_vac_version3)

##  Identifying the unwanted words mentioned in Stop_word to remove it 
stop_word1 =  ['x9f', 'x93', 'x9f', 'xac', 'x9f', 'x93', 'x9f','x82', "x99m", "xa9", "x9d", 'http',
             "gt", "xe2", "x99m", "['']", "xa6","000","x80", "x99m", "b", 'RT', "xe2", "x81", "x99re",
              'xf0','x9f','x98','xac','xf0','x9f','xa4','x93', 'qu', 'x99s','xa6', 'x9f','x8d', "x99",
              'x81', 'n', 'nFirst', 'xa6', "x9c", "x9cimmune" ]

final_vac_version4=[]
for i in final_vac_version3:                #This outer for loop reads each list 
    for j in i:                             #This inner for loop reads each word within the list           
        if j in stop_word1:                 #This if statement checks if the word matches to any word listed in stop_word1
            i.remove(j)                     #If the word matches any word from stop_word1 list, it will remove the word 
    final_vac_version4.append(i)
print(final_vac_version4)    

##  As the stop_word list was big, split the list and repeated cleaning of words  
remove_words1 = ['xa0Axios', 'x9cThere', 'B','C', 'x9cHealth','c', 'P','S', 'x80', 'x9cviral', 'RT', 
                 'xa0measles', 'x99t',  'x81', 's', 'x94', 'xf0', 'x90', 'x9f','x92', 'x89', 'http', 
                 'xe2', 'xa9', 'xa02000', 'xa8', "xc2",  'x9cYou', 'x99ve', 'xa6', 'xa2','x9coutbreaks',
                 'x9cNation', 'x9cThe','xa0debate', 'x9cOutbreaks','x9cThe','x9cNation', 'x8f', 'x8c', 
                 'x9a', 'A' ]

final_vac_version5=[]
for i in final_vac_version4:                #This outer for loop reads each list 
    for j in i:                             #This inner for loop reads each word within the list     
        if j in remove_words1:              #This if statement checks if the word matches to any word listed in remove_words1
            i.remove(j)                     #If the word matches any word from remove_words1 list, it will remove the word 
    final_vac_version5.append(i)
print(final_vac_version5)    

##  Removing repetitive tweets 
final_vac_version6=[]
for i in final_vac_version5:
    if i not in final_vac_version6:
        final_vac_version6.append(i)
print(final_vac_version6) 

##  Storing the clean data back to clean_measles_hashtag file
import pandas as pd
df = pd.DataFrame(final_vac_version6)
df.to_csv('/../clean_vac_tweets.csv',index=False)

## Performing sentiment analysis was easier in .txt file, converted .csv to .txt file
df.to_csv('/../clean_vac_tweets_txt.txt', sep='\t', index=False)


"""****     PART 3: Sentiment Analysis using TextBlob for Measles Outbreak 2019      ****"""
''' Coder: Brenda'''
##  In textblob, we use the polarity to differentiate the sentiment of the statement.
##  If polarity > 0.00, then its a positive sentiment, if polarity < 0.00, negative sentiment
##  and if polarity == 0.00, its a neutral sentiment 
##  We use for loop for iteration and reading full text file. 

from textblob import TextBlob

positive = 0 
pos_count = 0
negative = 0
neg_count = 0
neutral =0
neut_count = 0

with open('/../clean_measles_hashtag_txt.txt', 'r') as Cfile:
    
    # Using the for loop to check and store positive sentiment
    for line in Cfile.read().split('\n'):
        #print(line)
        Posanalysis = TextBlob(line)                    # Sentiment analysis
        if (Posanalysis.sentiment.polarity > 0.00):     # defining polarity to check if sentiment is positive
            #print(Posanalysis.sentiment.polarity)
            positive +=1; 
        pos_count +=1
        
    # Using the for loop to check and store negative sentiment
    for line in Cfile.read().split('\n'):
        Neganalysis = TextBlob(line)                    # Sentiment analysis
        if (Neganalysis.sentiment.polarity < 0.00):     # defining polarity to check sentiment is negative
            #print(Neganalysis.sentiment.polarity)
            negative += 1
        neg_count +=1
        
    # Using the for loop to check and store neutral sentiment    
    for line in Cfile.read().split('\n'):
        Neutanalysis = TextBlob(line)                   # Sentiment analysis
        if (Neutanalysis.sentiment.polarity == 0.00):   # defining polarity to check sentiment is neutral
            #print(Neutanalysis.sentiment.polarity)
            neutral +=1
        neut_count +=1
       
print("Positive Responses:", pos_count)
print("Negative Responses:", neg_count)
print("Neutral Responses:", neut_count)

## Finding the accracy of the for each sentiment. Concatinating strings using the format fuction 

print("Positive accuracy = {} % via {}smaples".format(positive/pos_count*100.0, pos_count))
print("Negati ve accuracy = {} % via {}smaples".format(negative/neg_count*100.0, neg_count))
print("Neutral accuracy = {} % via {}smaples".format(neutral/neut_count*100.0, neut_count))


"""****  PART 4: Sentiment Analysis using VaderSentiment for Measles Outbreak 2019    ****"""
''' Coder: Brenda'''
##  In VaderSentiment, for each statement we get the positive, negative, neutral and compound values.
##  compound states the overall sentiment of the statement, if compound > 0.00, then its positive statement. 
##  if compound < 0.00, its negative sentiment and if compound == 0.00, its a neutral sentiment. 
##  For further analysis, we categorized each sentiment to 3 section. 
##  We use for loop for iteration and if statement for categorization. 

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer 

analyzer = SentimentIntensityAnalyzer()

positive_count = 0.00 
highly_positive = 0.00
positive = 0.00
slight_positive = 0.00
negative_count = 0.00
slight_negative = 0.00
negative = 0.00
highly_negative = 0.00
neutral_count = 0.00

with open('/../clean_measles_hashtag_txt.txt', 'r') as Vfile:
    for line in Vfile.read().split('\n'):
        #print(line)
        vs = analyzer.polarity_scores(line)             # Sentiment analysis
        #print(vs)
        # Checking for positive sentiment 
        if vs['compound'] > 0.00:                       
            # Categorizing positive sentiment as slightly positive, positive and highly positive 
            # if pos < 0.30, tagging it as slightly positive 
            if vs['pos'] < 0.30:                        
                slight_positive +=1 
            # if pos is greater than 0.30 and less than 0.60, tagging it as positive 
            elif vs['pos'] < 0.60: 
                positive +=1
            # if pos is greater than 0.60 and less than or equal to 1.00, tagging it as highly positive 
            elif vs['pos'] <= 1.00: 
                highly_positive +=1
            #counting number of positive tweets
            positive_count +=1; 
        # Checking for negative sentiment 
        elif vs['compound'] < 0.00:
            # Categorizing negative sentiment as slightly negative, negative and highly negative 
            # if neg < 0.30, tagging it as slightly negative 
            if vs['neg'] < 0.30:
                slight_negative +=1
            # if neg is greater than 0.30 and less than 0.60, tagging it as negative
            elif vs['neg'] < 0.60: 
                negative +=1
            # if neg is greater than 0.60 and less than or equal to 1.00, tagging it as highly negative 
            elif vs['neg'] <= 1.00: 
                highly_negative  +=1
            #counting number of negative tweets
            negative_count += 1        
        # Checking for neutral sentiment 
        elif vs['compound'] == 0.00:
            #counting number of neutral tweets
           neutral_count += 1  

print('\n')        
print("Total positive responses:", positive_count)
print("Slightly positive responses:", slight_positive)
print("Average positive responses:", positive)
print("Highly positive responses:", highly_positive)
print('\n')
print("Total negative responses:", negative_count)
print("Slightly negative responses:", slight_negative)
print("Average negative responses:", negative)
print("Highly negative responses:", highly_negative)
print('\n')
print("Total neutral responses:", neutral_count)

"""*****                   PART 4: Visualization                               ****"""
'''Coder: Shruti'''
'''                             Pie-chart                                      '''
## Plotting pie chart for different categorizes defined via VaderSentiment for positive & negative sentiments ##

## Plotting for positive sentiment 
import matplotlib.pyplot as plt

# Data to plot
labels =['slight positive response', 'pos', 'high_pos']
sizes = [slight_positive, positive, highly_positive]
colors = ['green', 'yellow', 'red']
explode = [0.1,0,0]

# Plot
plt.pie(sizes, explode=explode, labels=labels, colors=colors,
autopct='%1.1f%%', shadow=True, startangle=140)
plt.axis('equal')
plt.title('VaderSentiment Adjusted Positive Sentiment Polarity for the combined Hashtags 2019/Measles/Vaccination Dataset (n=457)')
plt.show()

## Plotting for positive sentiment 
import matplotlib.pyplot as plt

# Data to plot
labels =['slight negative response', 'neg', 'high_neg']
sizes = [slight_negative, negative, highly_negative]
colors = ['blue', 'orange','pink']
explode = (0.1, 0, 0)  # explode 1st slice
 
plt.pie(sizes, explode=explode, labels=labels, colors=colors,
autopct='%1.1f%%', shadow=True, startangle=140)
 
plt.axis('equal')
plt.title('VaderSentiment Adjusted Negative Sentiment Polarity for the combined Hashtags 2019/Measles/Vaccination Dataset (n=457)')
plt.show()

'''                                 Grouped Bar Graph                          '''
''' Coder: Shruti'''
## Grouped Bar Graph to depict the difference between textBlob and VaderSentiment Analysis  ##
import numpy
import matplotlib.pyplot as plt 
import matplotlib.patches as mpatches

# Data to plot 
y1 = [pos_count, neg_count, neut_count]
y2 = [positive_count, negative_count, neutral_count]
y3 = [121, 246, 111]

# defining x axis and width of each bar
x = numpy.arange(len(y1))
bar_width = 0.15

# Ploting graphs  
plt.bar(x, y1, width = bar_width, color = 'green', zorder = 2)
plt.bar(x + bar_width, y2, width = bar_width, color = 'blue', zorder = 2)

plt.xticks(x + bar_width, ['Positive', 'Negative', 'Neutral'])
plt.title('Sentiment Analysis Comparison of TextBlob and VaderSentiment')
plt.xlabel('Sentiments')
plt.ylabel('No. of tweets')

green_patch = mpatches.Patch(color = 'green', label='TextBlob')
red_patch = mpatches.Patch(color = 'blue', label='VaderSentiment')

plt.legend(handles = [green_patch, red_patch])

plt.grid(axix = 'y')
plt.show()

'''                               Word Count & Bar Graphs                             '''
##       Performing word count for words from clean_measles_hashtag_txt file          ##
'''Coder: Ashley'''
file = open('/../clean_measles_hashtag_txt.txt', 'r')
book = file.read()

# Defining tokenize function to change all the words to lower case, which makes it easy to count
def tokenize():
    if book is not None:
        words = book.lower().split()
        return words
    else:
        return None

# Defining count_word function to count words and ignore the ',' and ' '
def count_word(tokens, token):
    count = 0

    for element in tokens:
        # Remove Punctuation
        word = element.replace(",","")
        word = word.replace(".","")

        # Found Word?
        if word == token:
            count += 1
    return count

# Tokenize the Book
words = tokenize()

# Get Word Count
word = 'measles'
frequency1 = count_word(words, word)
print('Word: [' + word + '] Frequency: ' + str(frequency1))

word2 = 'autism'
frequency2 = count_word(words, word2)
print('Word2: [' + word2 + '] Frequency: ' + str(frequency2))

word3 = 'vaccination'
frequency3 = count_word(words, word3)
print('Word3: [' + word3 + '] Frequency: ' + str(frequency3))

word4 = 'vaccinate'
frequency4 = count_word(words, word4)
print('Word4: [' + word4 + '] Frequency: ' + str(frequency4))

word5 = 'outbreak'
frequency5 = count_word(words, word5)
print('Word5: [' + word5 + '] Frequency: ' + str(frequency5))

word6 = "vaccine"
frequency6 = count_word(words, word6)
print('Word6: [' + word6 + '] Frequency: ' + str(frequency6))
  
# plotting graph for above word count 

import matplotlib.pyplot as plt

# data to plot 
fig=plt.figure(figsize=(7,5))
names=["Measles", "Autism", "Vaccination", "Vaccinate", "Outbreak", "Vaccine"]
positions=[frequency1, frequency2, frequency3, frequency4, frequency5, frequency6]

# Plotting graph 
plt.bar(names, positions, width=0.5, color = 'purple')
plt.title('Hashtag Frequency Count')
plt.show()

#       Performing word count for words from clean_vac_measles_hashtag_txt file          ##
'''Coder: Qian'''
file = open('/../clean_vac_tweets_txt.txt', 'r')
book = file.read()

# Defining tokenize function to change all the words to lower case, which makes it easy to count
def tokenize():
    if book is not None:
        words = book.lower().split()
        return words
    else:
        return None

# Defining count_word function to count words and ignore the ',' and ' '
def count_word(tokens, token):
    count = 0
    
    for element in tokens:
        # Remove Punctuation
        word = element.replace(",","")
        word = word.replace(".","")
        
        # Found Word?
        if word == token:
            count += 1
    return count

# Tokenize the Book
words = tokenize()

# Get Word Count
word_1 = 'measles'
fmeasles = count_word(words, word_1)

word_2 = 'flu'
flu = count_word(words, word_2)

# plotting graph for above word count 

import matplotlib.pyplot as plt
import numpy as np

# data to plot 
objects = ("Measles", "Flu")
y_pos = np.arange(len(objects))
numbers = [fmeasles, flu]

#plotting 
plt.barh(y_pos, numbers, align='center', alpha=0.5)
plt.yticks(y_pos, objects)
plt.xlabel('Frequency')
plt.title('Flu vs Measles Hashtag Frequency Count')
plt.show()
