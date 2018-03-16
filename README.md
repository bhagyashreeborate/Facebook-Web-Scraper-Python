# Facebook-Web-Scraper-Python
I have created a Facebook Page and Posts scraper in Python. The python script collects posts of the facebook page and also other details like Comments, likes, haha, wow's, texts, links, hashtags, etc.

The scraper collect details of Public Facebook Page using Facebook Graph API. In order to use the script, you should have a Facebook Graph API activated and their Security credentials as mentioned below in the code.

To get the credentials for Graph API you must have a Facebook Developers Account. Here you will create a Developer account and also your intended app for facebook scraping. Once the account and app is created you can access your app_id and app_secret key in settings of that particular app. Once you get this details, you have to add them in app_id and app_secret variables in the script.

Once the script is run the data is collected and stored in a CSV format with the name facebook_details.csv in the directory where the script is stored.

Note: My script collects data from Facebook at 12 AM and 12 PM twice a day. If you dont want the script to continously run and collect data at specific times then you can remove the timer set in the script.

The results fetched are: 

# Facebook Account details - 
  Facebook Account Name, Facebook total Page likes, Data Collection time.
# Post details - 
  Facebook Post id, Post URL, Post Creation Time, total Post likes, total Post loves, total Post haha' s, total Post wow's, total Post sad's, total Post angary's, total Post comments, total Post shares, Post Text, Total post Hashtags, Hashtag texts, total links in post and 3 separate links in separate cells.
  
# How to run the script -
1. Download Facebook.py file 
2. The Facebook graph api version is v2.4 Make sure you app supports this version
3. Update the app_id and app_secret with your app's id and secret key
4. Update the page_id list with the name of Facebook Page e.g. Suppose page you want to scrape is - https://www.facebook.com/sortedfood then give page_id as 'sortedfood' in the page_id list. You can add multiple page ids in this list to collect data for all the pages at once. Make sure the page is public and name you are giving is correct.
5. In the code there is a line - statuses = getFacebookPageFeedData(i, access_token, 30) this line collects data for maximum of 30 posts. You can change this number to 1 - 500 to fetch 1-500 posts at time for one page.
6. If you dont want script to run on specified time then modify the code by removing 
//**while True:
  now = datetime.datetime.now()
    if (now.hour == 19 and now.minute == 24 and now.second==50) or (now.hour == 12 and now.minute == 00 and now.second == 00): **//
    
lines from the code. (Modify the code as per your own requirements)
