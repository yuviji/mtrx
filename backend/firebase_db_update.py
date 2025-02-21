import firebase_admin
from firebase_admin import credentials

cred = credentials.Certificate("firebaseServiceKey.json")
firebase_admin.initialize_app(cred)

# firestore
from firebase_admin import firestore

db = firestore.client()

import json
import tqdm

with open("business_data.json") as f:
    data = json.load(f)
    biz_num = 0
    for business in tqdm.tqdm(data):
        biz_num += 1
        # print(f"Processing business {biz_num}/{len(data)}")
        
        # check if business with this name is already in database
        
        doc_ref = db.collection("businesses").where("business_name", "==", business["business_name"]).get()
        if len(list(doc_ref)) > 0:
            # print(doc_ref[0].to_dict())
            data = doc_ref[0].to_dict()
            business_id = doc_ref[0].id
            data["description"] = "No description available." if not business["business_description"] else (business["business_description"][11:] if business["business_description"].startswith("Specialties") else business["business_description"])

            """
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
            """
            
            # find monthly reviews count
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
            
            data["monthly_reviews_count"] = monthly_reviews_count
            data["num_reviews"] = len(business["business_reviews"])
            
            num_promoters, num_detractors = 0, 0
            # find net promoter score - promoter = >=4, detractor = <4
            for review in business["business_reviews"]:
                if review["review_rating"] >= 4:
                    num_promoters += 1
                else:
                    num_detractors += 1
            data["nps"] = (num_promoters - num_detractors) / len(business["business_reviews"])
            
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
            data["monthly_nps"] = monthly_nps
            
            db.collection("businesses").document(business_id).set(data)