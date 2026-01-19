# %%
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
import time
import random
from fake_useragent import UserAgent
#libs used to do web scraping and sending req

# %%
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.pakwheels.com/used-cars/honda/32"
}

#these are the headers to mimic th human behavior

# %%
base_url="https://www.pakwheels.com/used-cars/honda-lahore/201"#URL of the page

# %%
from dotenv import load_dotenv#importing
import os

# %%
load_dotenv()#load everything from env folder
mongo_url=os.getenv("DB_URL")
proxy_auth=os.getenv("proxy_key")

# %%
proxies={
    'http':f'http://{proxy_auth}',
    'https':f'http://{proxy_auth}'
}
#proxies list to save us from blocking 

# %%
session=requests.Session()#set session as making request for session 

# %%
client=MongoClient(mongo_url)
data_base=client["Honda_cars"]#set database name
collection=data_base["listings"]#set collection/table


# %%
#this code is used to get and save all the pages of honda brand 
def get_all_pages_of_honda():
    
    for page in range(1, 90):  # first 90 pages
        url = f"{base_url}?page={page}&_pjax=%5Bdata-pjax-container%5D"
        print(f"Saving page {page}: {url}")

        r = requests.get(url, headers=headers)

        with open(f"pages/page_{page}.html", "w", encoding="utf-8") as f:
            f.write(r.text)

        time.sleep(1 + 2 * random.random())


# %%
get_all_pages_of_honda()#calling function 

# %%
import json
#importing json so that we can read and write json

# %%
#from the saved html get all the links so that we can later scrap by using this link 
def extract_ads_link_and_title_from_html():
    urls=[]
    titles=[]
    for i in range (1,90):
        with open(f"pages/page_{i}.html","r",encoding="utf-8") as f:
            html=f.read()
        soup=BeautifulSoup(html,'html.parser')
        script_tag=soup.find("script", type="application/ld+json")
        data =json.loads(script_tag.string)
        listings=data.get("itemListElement", [])
        for j in listings:
            urls.append(j.get("url"))
            titles.append(j.get("name"))
    return urls, titles

# %%
urls,titles=extract_ads_link_and_title_from_html()#calling function and store urls and title 

# %%
print(len(urls)) #print to check its value

# %%
#this code is getting ada and save it so that later we can parse on it 
def get_ads_html():
    for i, url in enumerate( urls):
        print(f"saving add: {i}\n")
        r=session.get(url,headers=headers)
        with open (f"listings/listing_{i}.html","w",encoding="utf-8") as f: #open files and save as listing_{i} name 
            f.write(r.text)#open as written form
        time.sleep(1 + 2 * random.random())#mimic human behaviour add time delay 

# %%
get_ads_html()# calling a function 

# %%
#This is the code that is extracting brands, name, description and price from the saved htmls
def extract_all_fields():
    brands=[]
    names=[]
    descriptions=[]
    prices=[]

    for i in range(len(urls)):#run loop until total ads
        try:
            with open(f"listings/listing_{i}.html","r",encoding="utf-8") as f:
                html=f.read()#opened in read format

            soup=BeautifulSoup(html,'html.parser')

            script_tags=soup.find_all("script", type="application/ld+json")# find the tag like this and store it so that we 
            #can extract the info from this tag as we want 

            # default values so that alignment never breaks
            brand=None
            name=None
            description=None
            price=None

            for tag in script_tags:
                data=json.loads(tag.string)#loads json in data

                if isinstance(data, dict) and "Product" in data.get("@type", []):# if product exist 
                    brand=data.get("brand",{}).get("name")#get brand name
                    name=data.get("model")#get model name
                    description=data.get("description")#get description 
                    price=data.get("offers", {}).get("price")#get price

                    #basically it finds objects like these and store their values and append to main var as I did below
                    break

            brands.append(brand)
            names.append(name)
            descriptions.append(description)
            prices.append(price)

        except:
            brands.append(None)
            names.append(None)
            descriptions.append(None)
            prices.append(None)

    return names, brands, descriptions, prices


# %%
names,brands,descriptions,prices=extract_all_fields()#calling a function

# %%
#this function get the url of the images so that we can get the image and evaluate on our model
def get_image_urls(total_files):
    all_ads_images_urls = []

    for i in range(total_files):
        with open(f"listings/listing_{i}.html", "r", encoding="utf-8") as f:
            html = f.read()

        soup = BeautifulSoup(html, "html.parser")
        gallery = soup.find("ul", class_="gallery")

        ad_images_url = []

        if gallery:
            for li in gallery.find_all("li"):#find the tag like this
                img = li.find("img")
                if img:
                    url = img.get("data-original")#if image found then go to the original line and get the line do not take thumb one 
                    if url:
                        ad_images_url.append(url)# create image array

        all_ads_images_urls.append(ad_images_url)# create array of arrays so that every ad contain more pics not one

    return all_ads_images_urls

# %%
image_urls=get_image_urls(len(urls)) #calling a function

# %%
#this function get the the inspection rating if available other wise store none
def get_inspection_report(total_files):
    ratings=[]
    for i in range(total_files):
        with open(f"listings/listing_{i}.html", "r", encoding="utf-8") as f:
            html = f.read()

        soup = BeautifulSoup(html, "html.parser")
        rating_div=soup.find("div",class_="right pull-right primary-lang")
        if not rating_div:
            ratings.append(None)
            continue 
        try:
            text = rating_div.text.strip()     # get ratings
            score = float(text.split("/")[0])  # 9.4 store only first one
            rating_int = int(round(score))     # 9 convert to int
            ratings.append(rating_int)
        except:
            ratings.append(None)
    return ratings

# %%
ratings=get_inspection_report(len(urls))#calling a functions

# %%
print(ratings)#check

# %%
print (image_urls[0])#check
print(prices[0])#check

# %%
# urls=[....]
# title=[....]
# brands = [...]
# names = [...]
# descriptions = [...]
# images = [...]      # list of lists
# ratings = [...]
# price=[...]
#variables name 

# %%
#this function is basically making array of array of listing and each index contain one ad so that we cn push it into DB
def save_to_mongodb(total_files):
    listings=[]
    for i in range(total_files):
        listing={
        "URL":urls[i],
        "Title":titles[i],
        "brand": brands[i],
        "name": names[i],
        "description": descriptions[i],
        "images": image_urls[i],
        "rating": ratings[i],
        "price":prices[i]
        }
        listings.append(listing)
    return listings

# %%
listings=save_to_mongodb(len(urls))#calling a function

# %%
#save to db
collection.insert_many(listings)

# %%



