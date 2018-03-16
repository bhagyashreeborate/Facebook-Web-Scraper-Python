#---- Author: Bhagyashree Borate ------
#--- Facebook script to collect data from Facebook Public pages and cannot recieve private data.
#The file should be provided with the API KEYS from Facebook Graph API to work correctly.
#The page_id should be given with the total number of public pages to collect data from.
# How to run? - Just run the script as it is without any arguments at runtime. i.e. python Facebook.py 
# ---- PYTHON LIBRARIES ----
import urllib.request
import json
import datetime
import csv
import time
import re
import os
global acc_name, fan_count

# ------ -------


# -- Facebook app Id and secret key ( TO BE KEPT CONFIDENTIAL )
app_id = "your app_id goes here"
app_secret = "your app_secret"
access_token = app_id + "|" + app_secret
# --------



#---- Mention id of page which you want to get data from ---

page_id = ['sortedfood', ..., 'name_of_facebook_pages']  #you can find this name in the profile link for particular page


# --- Function to get Id, Name, TOTAL LIKES, Link of the PAGE ----

def get_FB_Page_Details(page_id,access_token):
    api_endpoint = "https://graph.facebook.com/v2.4/"
    fb_graph_url = api_endpoint+page_id+"?fields=id,name,fan_count,link&access_token="+access_token
    
    try:
        api_request = urllib.request.Request(fb_graph_url)
        api_response = urllib.request.urlopen(api_request)
        
        try:
            data = json.loads(api_response.read())
            return data
        except (ValueError, KeyError, TypeError):
            return "0"

    except IOError as e:
        if hasattr(e, 'code'):
            return "no"
        elif hasattr(e, 'reason'):
            return "no"



#--- Funtion to check if requested URL exists --

def request_until_succeed(url):
    req = urllib.request.Request(url)
    success = False
    while success is False:
        try: 
            response = urllib.request.urlopen(req)
            if response.getcode() == 200:
                success = True
        except Exception as e:
            time.sleep(5)
            
            #print("Error for URL %s: %s" % (url, datetime.datetime.now()))

    return response.read().decode('utf-8')



# ----- Get Details of POSTS ------
def get_FB_Page_Post_Details(page_id, access_token, num_statuses):
    
    # construct the URL string
    base = "https://graph.facebook.com"
    node = "/" + page_id + "/feed" 
    parameters = "/?fields=place,message_tags,message,link,created_time,type,name,id,likes.summary(true).limit(0),reactions.type(LOVE).limit(0).summary(1).as(love),reactions.type(HAHA).limit(0).summary(1).as(haha),reactions.type(WOW).limit(0).summary(1).as(wow),reactions.type(ANGRY).limit(0).summary(1).as(angry),comments.limit(1).summary(true),shares&limit=%s&access_token=%s" % (num_statuses, access_token) # URL DATA
    url = base + node + parameters
    
    # retrieve data
    data = json.loads(request_until_succeed(url))
    
    return data


def getFacebookPagePostData(i,access_token): # Get Details of Particular Post
    # construct the URL string
    base = "https://graph.facebook.com/v2.6/?fields=place,message_tags,message,link,created_time,type,name,id,likes.summary(true).limit(0),reactions.type(LOVE).limit(0).summary(1).as(love),reactions.type(HAHA).limit(0).summary(1).as(haha),reactions.type(WOW).limit(0).summary(1).as(wow),reactions.type(ANGRY).limit(0).summary(1).as(angry),comments.limit(1).summary(true),shares&id="+i+"&access_token="+access_token
    # retrieve data
    data = json.loads(request_until_succeed(base))
    
    return data


# ---- main function where counts and other data is retrived ---

def get_FB_Page_Post_Data(page_id,account, page_likes, status):
    
    status_id = status['id']
    s = status_id.split('_')
    post_url = "https://www.facebook.com/"+page_id+"/posts/"+s[1]

    status_message = '' if 'message' not in status.keys() else status['message'].encode('utf-8')
    status_message1 = '' if 'message' not in status.keys() else status['message']
    link_name = '' if 'name' not in status.keys() else status['name'].encode('utf-8')
    status_type = status['type']
    
    
    location = 0 if 'place' not in status.keys() else 1
    messagetags = '' if 'message_tags' not in status.keys() else status['message_tags']
    
    tags = []
    if len(messagetags)>0:
        for i in range(len(messagetags)):
            if any('name' in d for d in messagetags):
                tags.append(messagetags[i]['name'])
                
            else:
                tags = []
    else:
        tags = []

    #tagged people count
    with_people = len(tags)

    #get hashtags from status
    x =  re.compile(r'\B#\w+')
    hashtags = len(x.findall(status_message1))
    hashtag_list = x.findall(status_message1)
    hashtag_text = ' '.join(hashtag_list)
    

    #get Links from status
    urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', status_message1)
    links = []
    for url in urls:
        links.append(url)

    
    #total links
    num_links = len(links)          
    link_data = []
    #link1 2 3 
    if len(links)>0:
        if len(links)==3:
            for i in range(0,3):
                link_data.append(links[i])
        elif len(links)< 3:
            count = 3 - len(links)
            for j in range(len(links)):
                link_data.append(links[j])
            for j in range(0,count):
                link_data.append(" ")
    else:
        for i in range(0,3):
            if i>2:
                break
            else:
                link_data.append(" ")
    
    link1 = link_data[0]
    link2 = link_data[1]
    link3 = link_data[2]

    data_collected_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    #time conversion - CREATION time of post
    status_published = datetime.datetime.strptime(status['created_time'],'%Y-%m-%dT%H:%M:%S+0000')
    status_published = status_published + datetime.timedelta(hours=-5) # EST
    status_published = status_published.strftime('%Y-%m-%d %H:%M:%S') # best time format for spreadsheet programs
    
    
    num_likes = 0 if 'likes' not in status.keys() else status['likes']['summary']['total_count']
    num_loves = 0 if 'love' not in status.keys() else status['love']['summary']['total_count']
    num_haha = 0 if 'haha' not in status.keys() else status['haha']['summary']['total_count']
    num_wow = 0 if 'wow' not in status.keys() else status['wow']['summary']['total_count']
    num_sad = 0 if 'sad' not in status.keys() else status['sad']['summary']['total_count']
    num_angry = 0 if 'angry' not in status.keys() else status['angry']['summary']['total_count']
    num_comments = 0 if 'comments' not in status.keys() else status['comments']['summary']['total_count']
    num_shares = 0 if 'shares' not in status.keys() else status['shares']['count']

    # return a tuple of all processed data
    return (account,page_likes, status_id, post_url, data_collected_time, status_published,
            num_likes,num_loves, num_haha,num_wow,num_sad,num_angry,num_comments, num_shares,status_message, hashtags, hashtag_text, num_links,link1,link2,link3)


#---main call function --

def get_FB_Page_Posts(page_id,access_token):
    try:
        flag = 0 
        while True:
            now = datetime.datetime.now()
            if (now.hour == 19 and now.minute == 24 and now.second==50) or (now.hour == 12 and now.minute == 00 and now.second == 00):              #checking if current time is 0:00 i.e. 12AM or 12:00 i.e. 12:00 PM
                for i in page_id:
                    has_next_page = True
                    num_processed = 0   # keep a count on how many we've processed
                    script_starttime = datetime.datetime.now()
                    statuses = get_FB_Page_Post_Details(i, access_token, 30)    #here 4 means 4 posts can be fetched at a time
                    flag = 0
                    with open('facebook_details.csv', 'a', newline='') as file:
                        w = csv.writer(file)
                        for status in statuses['data']:
                            if flag == 0:
                                page_data = get_FB_Page_Details(i, access_token)
                                account = str(page_data['name'])
                                page_likes = str(page_data['fan_count'])                                
                                flag = 1
                                acc_name = account
                                fan_count = page_likes
                            else:
                                account = ""
                                page_likes =""
                                w.writerow(get_FB_Page_Post_Data(i, acc_name, fan_count, status))
                    
                            # output progress 
                            num_processed += 1
                            if num_processed % 1000 == 0:
                                print("%s Statuses Processed: %s" % (num_processed, datetime.datetime.now()))
                    print("\nDone!\n%s Statuses Processed in %s" % (num_processed, datetime.datetime.now() - script_starttime))
                    
            else:
                a=0
    except KeyboardInterrupt:
        print("exit!")


#---CREATE EXCEL SHEET ---
with open('facebook_details.csv', 'w', newline='') as file:
    w = csv.writer(file)
    w.writerow(["Account", "#pagelike", "post_id", "url","Data Collected Time","Post Creation Time","#likes","#loves", "#haha",",#wow","#sad","angry","num_comments", "num_shares","text","#hashtags","hashtag_text","#links","link1","link2","link3"])
# --- start of program ----

get_FB_Page_Posts(page_id,access_token)
