import firebase_admin
from firebase_admin import credentials

cred = credentials.Certificate("firebaseServiceKey.json")
firebase_admin.initialize_app(cred)

import os
from dotenv import load_dotenv

load_dotenv()

# firestore
from firebase_admin import firestore

db = firestore.client()

# load business_data.json

import json
import tqdm
import uuid
from transformers import pipeline
import random
import requests
import nltk

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

sentiment_pipeline = pipeline("sentiment-analysis")

# # clear the collection
deleted_nums = 0
for doc in db.collection("businesses").stream():
    doc.reference.delete()
    deleted_nums += 1
print(f"Deleted {deleted_nums} businesses")

    # print(f"Deleted {doc.id}")

# for doc in db.collection("reviews").stream():
#     doc.reference.delete()
#     print(f"Deleted {doc.id}")

with open("business_data.json") as f:
    data = json.load(f)
    # print(data[0].keys(), data[0]["business_reviews"][0].keys())
    biz_num = 0
    for business in data:
        biz_num += 1
        print(f"Processing business {biz_num}/{len(data)}")
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
        for r in tqdm.tqdm(reviews):
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
        
        print(avg_rating, 'from', review_count, 'reviews')
        print('Average sentiment:', avg_sentiment)
        print('Topics:', topics)
        # print('Lowest elite review:', low_elite)
        # print('Highest elite review:', high_elite)
        print()
        
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
            "business_description": business["business_description"],
            "good_review": high_elite,
            "bad_review": low_elite,
            "business_cost": business["business_cost"],
        }
        
        db.collection("businesses").add(document)
        
        
    # for business in tqdm.tqdm(data):
    #     review_ids = []
    #     for review in business["business_reviews"]:
    #         review_id = str(uuid.uuid4())
    #         db.collection("reviews").document(review_id).set(review)
    #         review_ids.append(review_id)
    #     business["business_reviews"] = review_ids
    #     business_id = str(uuid.uuid4())
    #     db.collection("businesses").document(business_id).set(business)
    #     db.collection("businesses").add(business)
