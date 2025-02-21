import random
from flask import Flask
import tqdm
from transformers import pipeline
import os
from dotenv import load_dotenv
import requests
import firebase_admin
from firebase_admin import credentials, firestore
import time

load_dotenv()

cred = credentials.Certificate("firebaseServiceKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()
# from dotenv import load_dotenv

# load_dotenv()

from async_scraper import async_scrape

app = Flask(__name__)

sentiment_pipeline = pipeline("sentiment-analysis")

@app.route('/')
def hello_world():
    return 'Welcome to mtrx!'

@app.route('/sentiment/text=<text>')
def sentiment_analysis(text):
    return sentiment_pipeline(text)

@app.route('/topic/prompt=<prompt>')
def topic_classifier(prompt):
    url = "https://proxy.tune.app/chat/completions"
    headers = {
        "Authorization": os.getenv("TUNE_API_KEY"),
        "Content-Type": "application/json",
    }
    data = {
    "temperature": 0.9,
        "messages":  [
        {
            "role": "system",
            "content": "You will be given text from reviews on a restaurant. Classify the main focus of the review as either food, service, or environment. Only provide the one word answer."
        },
        {
            "role": "user",
            "content": prompt,
        }
        ],
        "model": "meta/llama-3.1-8b-instruct",
        "stream": False,
        # "frequency_penalty":  0.2,
        "max_tokens": 4
    }
    response = requests.post(url, headers=headers, json=data)
    return response.json()["choices"][0]["message"]["content"]

@app.route('/suggestions/prompt=<prompt>')
def cerebras(prompt):
    url = "https://proxy.tune.app/chat/completions"
    headers = {
        "Authorization": os.getenv("TUNE_API_KEY"),
        "Content-Type": "application/json",
    }
    data = {
    "temperature": 0.9,
        "messages":  [
        {
            "role": "user",
            "content": prompt,
        }
        ],
        "model": "meta/llama-3.1-8b-instruct",
        "stream": False,
        # "frequency_penalty":  0.2,
        # "max_tokens": 100
    }
    response = requests.post(url, headers=headers, json=data)
    return response.json()["choices"][0]["message"]["content"]

@app.route('/db/competitors/business_id=<business_id>')
def get_competitors(business_id):
    doc_ref = db.collection("businesses").document(business_id)
    doc = doc_ref.get().to_dict()
    tags = doc["business_tags"]
    
    # find businesses with shared tags
    competitors = {}
    for tag in tags:
        for doc in db.collection("businesses").where("business_tags", "array_contains", tag).stream():
            if doc.id in competitors:
                competitors[doc.id] += 1
            else:
                competitors[doc.id] = 1
    # sort by number of shared tags, descending order, give as list
    competitors = [k for k, v in sorted(competitors.items(), key=lambda item: item[1], reverse=True) if k != business_id]
    if len(competitors) > 2:
        return competitors[:2]
    return competitors
    
@app.route('/yelp/url=<url>')
def yelp(url):
    # url should just everything after '/biz' in a yelp url
    start_time = time.time()
    business = async_scrape(url.replace('"', ''), 2)
    review_sum, review_count = 0, 0
    low_elite = (6, '')
    high_elite = (-1, '')
    
    # each review has "review_date": "Mon D, YYYY"
    # calculate monthly average rating and 3-month moving average rating
    
    # variable inits
    monthly_avg_rating = {}
    moving_avg_rating = {}
    
    for review in business["business_reviews"]:
        date = review["review_date"]
        month = date.split(" ")[0]
        year = date.split(" ")[2]
        if month + " " + year in monthly_avg_rating:
            monthly_avg_rating[month + " " + year].append(review["review_rating"])
        else:
            monthly_avg_rating[month + " " + year] = [review["review_rating"]]
        
        review_sum += review["review_rating"]
        review_count += 1
        if review["elite"]:
            if review["review_rating"] <= low_elite[0] and len(review["review_content"]) > len(low_elite[1]):
                low_elite = (review["review_rating"], review["review_content"])
            if review["review_rating"] >= high_elite[0] and len(review["review_content"]) > len(high_elite[1]):
                high_elite = (review["review_rating"], review["review_content"])
    avg_rating = review_sum / review_count
    
    for month in monthly_avg_rating:
        monthly_avg_rating[month] = sum(monthly_avg_rating[month]) / len(monthly_avg_rating[month])
        
    # calculate 3-month moving average rating
    months = list(monthly_avg_rating.keys())
    for i in range(2, len(months)):
        moving_avg_rating[months[i]] = (monthly_avg_rating[months[i]] + monthly_avg_rating[months[i-1]] + monthly_avg_rating[months[i-2]]) / 3
        
    print("Monthly average rating")
    print("3-month moving average rating")
    
    # if len(reviews) > 500:
    # choose 500 as spread out as possible, not random
    reviews = [business["business_reviews"][i] for i in range(0, len(business["business_reviews"]), max(len(business["business_reviews"]) // 500, 1))][:500]
    sentiments = []
    topics = {"food": [], "service": [], "environment": []}
    elite_indices = [i for i in range(len(reviews)) if reviews[i]["elite"]]
    elite_indices = random.sample(elite_indices, min(50, len(elite_indices)))
    idx = 0
    for r in reviews:
        try:
            sentiment = sentiment_pipeline(r["review_content"])
            sentiments.append(sentiment[0])
            if idx in elite_indices:
                topic = topic_classifier(r["review_content"]).lower()
                if "food" in topic:
                    topics["food"].append(sentiment[0])
                elif "service" in topic:
                    topics["service"].append(sentiment[0])
                elif "environment" in topic:
                    topics["environment"].append(sentiment[0])
        except:
            pass
        idx += 1
                
    for topic in topics:
        if len(topics[topic]) == 0:
            topics[topic] = 0
        else:
            topics[topic] = sum([sentiment["score"] * (1 if sentiment["label"] == "POSITIVE" else -1) for sentiment in topics[topic]]) / len(topics[topic])
    
    sentiment_sum = 0
    for sentiment in sentiments:
        sentiment_sum += sentiment["score"] * (1 if sentiment["label"] == "POSITIVE" else -1)
    avg_sentiment = sentiment_sum / review_count
    
    document = {
        "business_name": business["business_name"],
        "business_rating": avg_rating,
        "business_sentiment": avg_sentiment,
        "business_topics": topics,
        "monthly_avg_rating": monthly_avg_rating,
        "moving_avg_rating": moving_avg_rating,
        "business_address": business["business_address"],
        "num_reviews": review_count,
        "business_tags": [tag.lower().strip() for tag in business["business_tags"]],
        "description": "No description available." if not business["business_description"] else (business["business_description"][11:] if business["business_description"].startswith("Specialties") else business["business_description"]),
        "good_review": high_elite,
        "bad_review": low_elite,
        "business_cost": business["business_cost"],
    }
    
    monthly_reviews_count = {}
    for review in business["business_reviews"]:
        date = review["review_date"]
        month = date.split(" ")[0]
        year = date.split(" ")[2]
        if month + " " + year in monthly_reviews_count:
            monthly_reviews_count[month + " " + year] += 1
        else:
            monthly_reviews_count[month + " " + year] = 1
    # find monthly average rating
    monthly_avg_rating = {}
    for review in business["business_reviews"]:
        date = review["review_date"]
        month = date.split(" ")[0]
        year = date.split(" ")[2]
        if month + " " + year in monthly_avg_rating:
            monthly_avg_rating[month + " " + year].append(review["review_rating"])
        else:
            monthly_avg_rating[month + " " + year] = [review["review_rating"]]
    for month in monthly_avg_rating:
        monthly_avg_rating[month] = sum(monthly_avg_rating[month]) / len(monthly_avg_rating[month])
    
    document["monthly_reviews_count"] = monthly_reviews_count
    
    num_promoters, num_detractors = 0, 0
    # find net promoter score - promoter = >=4, detractor = <4
    for review in business["business_reviews"]:
        if review["review_rating"] >= 4:
            num_promoters += 1
        else:
            num_detractors += 1
    document["nps"] = (num_promoters - num_detractors) / len(business["business_reviews"])
    
    # calculate monthly average nps
    monthly_nps = {}
    for review in business["business_reviews"]:
        date = review["review_date"]
        month = date.split(" ")[0]
        year = date.split(" ")[2]
        if month + " " + year in monthly_nps:
            monthly_nps[month + " " + year].append(review["review_rating"])
        else:
            monthly_nps[month + " " + year] = [review["review_rating"]]
    for month in monthly_nps:
        num_promoters, num_detractors = 0, 0
        for rating in monthly_nps[month]:
            if rating >= 4:
                num_promoters += 1
            else:
                num_detractors += 1
        monthly_nps[month] = (num_promoters - num_detractors) / len(monthly_nps[month])
    document["monthly_nps"] = monthly_nps
    
    db.collection("businesses").add(document)
    
    print(f"Time taken: {time.time() - start_time}")
    print(review_count, "reviews")
    
    return document

if __name__ == '__main__':
    app.run(debug=True, port=5000)