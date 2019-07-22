#!/usr/bin/env python
# coding: utf-8

# # Dataquest Project 1 
# Build Android and iOS mobile apps. Our goal for this project is to analyze data to help our developers understand what kinds of apps are likely to attract more users.

# In[2]:


#Open the two data sets and save both as lists
def open_dataset(file_name, header=True):        
    opened_file = open(file_name)
    from csv import reader
    read_file = reader(opened_file)
    data = list(read_file)
     
    if header:
        return (data[0],data[1:])
    else:
        return data

apple_header = open_dataset('AppleStore.csv',header=True)[0]
apple_data = open_dataset('AppleStore.csv',header=True)[1]
android_header= open_dataset('googleplaystore.csv',header=True)[0]
android_data= open_dataset('googleplaystore.csv',header=True)[1]


# In[3]:


#Explore bothe data sets use the function
def explore_data(dataset,start,end,rows_and_columns=False):
    dataset_slice = dataset[start:end]    
    for row in dataset_slice:
        print(row)
        print('\n') # adds a new (empty) line after each row

    if rows_and_columns:
        print('Number of rows:', len(dataset))
        print('Number of columns:', len(dataset[0]))

explore_data(apple_data,0,3,rows_and_columns=True)
explore_data(android_data,0,3,rows_and_columns=True)


# In[4]:


#Data Cleaning
explore_data(android_data,10472,10473,rows_and_columns=True)
del android_data[10472]


# In[5]:


# Remove duplicate entries
for app in android_data:
    name = app[0]
    if name == 'Instagram':
        print(app)


# In[6]:


duplicate_apps = []
unique_apps = []

for app in android_data:
    name = app[0]
    if name in unique_apps:
        duplicate_apps.append(name)
    else:
        unique_apps.append(name)
        
print('Number of duplicat apps:',len(duplicate_apps))
print('\n')
print('Examples of duplicate apps:',duplicate_apps[:15])


# In[7]:


# Remove Duplicate Entries
#Since we do not want to remove the duplicate items randomly,we might want to keep the higher number of reviews in our data. 
# Dictionary would be a good choice
# Create a dictionary where each key is a unique app name and the correponding dictionary value is the highest number of reviews of that app
reviews_max = {}
for app in android_data:
    name = app[0]
    n_reviews = float(app[3])
    if name in reviews_max and reviews_max[name] < n_reviews:
        reviews_max[name] = n_reviews
    elif name not in reviews_max:
        reviews_max[name] = n_reviews
print(len(reviews_max))
        


# In[8]:


# Remove the dupliacte rows
android_clean = [] # store our new cleaned data set
already_added = [] # will just store app names 
for app in android_data:
    name = app[0]
    n_reviews = float(app[3])
    if (n_reviews == reviews_max[name]) and (name not in already_added):
        android_clean.append(app)
        already_added.append(name)

print(len(android_clean))


# In[9]:


# Remove Non-English Apps
def check_english(text):
    count = 0
    for i in text:
        if ord(i) > 127 or ord(i)<0:
            count +=1
    if count >= 3:
        return False
    else:
        return True # Loop the whole text finish and then in the end return 

# Filter non-English APPS
android_English=[]
ios_English =[]

for i in android_clean:
    name = i[0]
    if check_english(name) == True:
        android_English.append(i)

for i in apple_data:
    name = i[1]
    if check_english(name) == True:
        ios_English.append(i) 

explore_data(android_English, 0, 3, True)
print('\n')
explore_data(ios_English, 0, 3, True)


# In[10]:


# Isolate the Free Apps
android_free_apps =[]
apple_free_apps =[]
for i in android_English:
    price = i[6]
    if price == 'Free':
        android_free_apps.append(i)
for i in ios_English:
    price = i[4]
    if price == '0.0':
        apple_free_apps.append(i) 

explore_data(android_free_apps, 0, 3, True)
print('\n')
explore_data(apple_free_apps, 0, 3, True)


# # Most Common Apps by Genre: Part one
# 
# ## To minimize risks and overhead, our validation strategy for an app idea is comprised of three steps:  
# 
# Build a minimal Android version of the app, and add it to Google Play.
#     If the app has a good response from users, we develop it further.
#     If the app is profitable after six months, we build an iOS version of the app and add it to the App Store.
# 
# Because our end goal is to add the app on both Google Play and the App Store, we need to find app profiles that are successful on both markets.
# For instance, a profile that works well for both markets might be a productivity app that makes use of gamification.

# In[11]:


def freq_table(dataset,index):
    genre_counting = {}
    for each_row in dataset:
        genre = each_row[index]
        count = 1 + genre_counting.get(genre, 0)
        genre_counting[genre] = count
    return genre_counting

def display_table(dataset, index): # This one is quite useful too. Can sorted a dataset and display it in order 
    table = freq_table(dataset, index)
    table_display = []
    for key in table:
        key_val_as_tuple = (table[key], key)
        table_display.append(key_val_as_tuple)

    table_sorted = sorted(table_display, reverse = True)
    for entry in table_sorted:
        print(entry[1], ':', entry[0])
    


# In[12]:


### Analyse the frequency table I generated for the the android dataset and the apple dataset.
#### Apple dataset:

display_table(apple_free_apps , -5)


# From the table above, we can see Games is the most popular genre. And most of the apps designed for entertainment, like games, photo and video, social neteworking. I don't think we can conclude that this genre also have a large number of users. A large number of apps does  not equals to the large number of users.
# 

# In[13]:


### Analyse the frequency table I generated for the the android dataset and the apple dataset.
#### Android dataset:
display_table(android_free_apps , 1) #Category
print('-------')
display_table(android_free_apps , -4) # Genres


# Based on the table above, we could find the most common genres is Entertainment. Education and business are also remarkable.
# 
# Family, games and tools are both the most common genres in Google Play and also Apple store. But compare in a more detailed level, we could find Google app has more pratical purpose use than Apple store. I cannot tell much difference between genre and category. But it seems that genre has a more detailed information. Google play seems has a more balanced app categories.

# ### Most Popular Apps by Genre on the App Store

# In[42]:


# Generate a unique frequency table for the prime_genre column 
prime_genre = freq_table(android_free_apps,-5)
ratings_apple = []
# Loop over the unique genres of the App Store data set
for genre in prime_genre:# all unique genre collection
    total = 0  # fpr each new genre you need to start over, go back to 0 and count from beginning
    len_genre = 0
    for i in apple_free_apps:# get the ranking data 
        genre_app = i[-5]
        if genre_app == genre:
            ratings = float(i[5])
            total += ratings
            len_genre += 1
    ave_ratings = total/len_genre   #all this genre's ranking add up and be divided by how many app are in this genre
    rating_as_tuple = (ave_ratings,len_genre, genre) # Dictionary sort method!! 
    ratings_apple.append(rating_as_tuple)

ranking_sorted = sorted(ratings_apple, reverse = True)
for entry in ranking_sorted:
        print(entry[2], ':', entry[0],',',entry[1])

                
            



    
    
    


# Considering above data result, we can see that Navigation is the largest ranking number!. For now I would like to recommend that Navigation app would be great. However, we may concern that there could be some "so popular" app under Navigation categary, which cause the data skewed. Therefore, we should find out the most len_genre in next step. Correct the code above, we couuld see that Navigation just has 6 apps, which could be considered that apps like "Google map" make this situation. But reference and social work have more apps under their categories. 

# ### Most Popular Apps by Genre on Google Play 
# #### find out which app genres attract the most users, 

# In[44]:


display_table(android_free_apps, 5)


# In[47]:


# remove characters from strings: str.replace(old, new) 
#calculate the average number of installs per app genre for the Google Play data set.


#Generate a unique frequency table for the prime_genre column 
genre_android= freq_table(android_free_apps ,1)
install_android = []
# Loop over the unique genres of the App Store data set
for genre in genre_android:# all unique genre collection
    total = 0  # for each new genre you need to start over, go back to 0 and count from beginning
    len_genre = 0
    for i in android_free_apps :# get the ranking data 
        genre_app = i[1]
        if genre_app == genre:
            n_installs = i[5]
            n_installs= n_installs.replace('+','')
            n_installs = n_installs.replace(',','')
            total += int(n_installs)
            len_genre += 1
    ave_installs = total/len_genre   #all this genre's ranking add up and be divided by how many app are in this genre
    installs_as_tuple = (ave_installs,len_genre, genre) # Dictionary sort method!! 
    install_android.append(installs_as_tuple)

install_android_sorted = sorted(install_android, reverse = True)
for entry in install_android_sorted:
        print(entry[2], ':', entry[0],',',entry[1])
    
    


# Based on the result above, we could find that communication has the most installs. However, as we discussed above, we are nor sure that if there are some "main popular apps

# In[ ]:




