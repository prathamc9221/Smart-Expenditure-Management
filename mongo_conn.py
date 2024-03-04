#!/usr/bin/env python
"""
_file name_ = mongo_conn.py
_date created_ = 11/20/2023
_date last modified_ = 12/07/2023
__python version = 3.11
_author_ = "Prathamesh Chaudhari - pchaudhari2@binghamton.edu - B01039752",
           "Anagha Ghate"
           "Swapnil Mane"
_status_ = "Development"
"""

from pymongo import MongoClient
from collections import OrderedDict
import configparser

# Importing database objects from config
config_obj = configparser.ConfigParser()
config_obj.read("config.py")
db_config = config_obj["mongodb"]

db_connection_name = db_config["mongo_client"]
db_name = db_config["mongo_db"]
collection_name = db_config["mongo_conn"] 

client = MongoClient() 

client = MongoClient(db_connection_name) 
mydatabase = client[db_name]
mycollection = mydatabase[collection_name]


def run_query1():
    # Define the aggregation pipeline
    pipeline = [
        {"$unwind": "$reviews"},
        {"$group": {
            "_id": {
                "hotel": "$name",
                "year": {"$year": "$reviews.date"},
                "month": {"$month": "$reviews.date"}
            },
            "averageRating": {"$avg": "$reviews.rating"},
            "categories": {"$first": "$categories"},  # Use $first to get a value from the group
            "province": {"$first": "$province"}
        }},
        {"$group": {
            "_id": "$_id.hotel",
            "ratings": {"$push": {
                "year": "$_id.year",
                "month": "$_id.month",
                "averageRating": "$averageRating",
                "categories": "$categories",
                "province": "$province"
            }},
            "trend": {
                "$last": {
                    "$cond": {
                        "if": {
                            "$gte": [
                                {"$cond": {"if": {"$isArray": "$averageRating"}, "then": {"$arrayElemAt": ["$averageRating", -1]}, "else": "$averageRating"}},
                                {"$cond": {"if": {"$isArray": "$averageRating"}, "then": {"$arrayElemAt": ["$averageRating", 0]}, "else": "$averageRating"}}
                            ]
                        },
                        "then": "Upward",
                        "else": "Downward"
                    }
                }
            },
            "categories": {"$first": "$categories"},  # Use $first to get a value from the group
            "province": {"$first": "$province"}
        }},
        {"$project": {"hotel": "$_id", "ratings": 1, "trend": 1, "categories": 1, "province": 1, "_id": 0}}
    ]
    # Execute the aggregation query
    result = list(mycollection.aggregate(pipeline))

    data_list = []
    # Print the result
    for document in result:
        doc_json = {}
        rating_list = []
        doc_json["hotel"] = document["hotel"]
        doc_json["trend"] = document["trend"]
        ratings = document["ratings"]
        for x in ratings:
            rating_list.append(x["averageRating"])
        avg_rating = sum(rating_list) / len(rating_list)
        doc_json["avg_rating"] = avg_rating
        doc_json["categories"] = document["categories"]
        doc_json["province"] = document["province"]
        data_list.append(doc_json)
    return data_list


def run_query2():
    # Define the aggregation pipeline
    pipeline = [
        {"$group": {
            "_id": {
                "state": "$province",
                "month": {"$month": {"$toDate": "$dateAdded"}}
            },
            "averageRating": {"$avg": "$reviews.rating"}
        }},
        {"$group": {
            "_id": "$_id.state",
            "ratingsByMonth": {"$push": {"month": "$_id.month", "averageRating": "$averageRating"}}
        }},
        {"$project": {"_id": 0, "state": "$_id", "ratingsByMonth": 1}},
        {"$sort": {"ratingsByMonth.month": 1}}
    ]    
    # Execute the aggregation query
    result = list(mycollection.aggregate(pipeline))
    
    data_list = []
    # Print the result
    for x in result:
        doc_json = {}
          
        monthly_ratings = {}     
        for i in x["ratingsByMonth"]:
            monthly_ratings[i['month']] = i['averageRating']
        monthly_ratings = dict(sorted(monthly_ratings.items()))
        doc_json["state"] = x["state"]
        doc_json["monthly_ratings"] = monthly_ratings
        data_list.append(doc_json)
    return data_list


def run_query3():
    # Define the aggregation pipeline
    pipeline = [
        {"$match": {"reviews.rating": {"$in": [4, 5]}}},
        {"$group": {
            "_id": {"city": "$city", "hotel_id": "$id"},
            "name": {"$first": "$name"},
            "address": {"$first": "$address"},
            "website": {"$first": {"$arrayElemAt": [{"$split": ["$websites", ","]}, 0]}},
            "ratings": {"$push": "$reviews.rating"}
        }},
        {"$addFields": {"averageRating": {"$avg": "$ratings"}}},
        {"$group": {
            "_id": "$_id.city",
            "hotels": {"$push": {
                "name": "$name",
                "address": "$address",
                "website": "$website",
                "averageRating": {"$avg": "$averageRating"}
            }}
        }},
        {"$project": {"_id": 0, "city": "$_id", "hotels": {"$slice": [{"$map": {"input": "$hotels", "as": "hotel", "in": {"name": "$$hotel.name", "address": "$$hotel.address", "website": "$$hotel.website", "averageRating": "$$hotel.averageRating"}}}, 5]}}}
    ]

    # Execute the aggregation query
    result = list(mycollection.aggregate(pipeline))
    
    data_list = []
    # Print the result
    for x in result:
        city = x["city"]
        for i in x["hotels"]:
            doc_json = {}
            doc_json["city"] = city
            doc_json["hotel"] = i["name"]
            doc_json["address"] = i["address"]
            doc_json["website"] = i["website"]
            doc_json["averageRating"] = i["averageRating"]
            data_list.append(doc_json) 
    return data_list


def run_query4():
    # Define the aggregation pipeline
    pipeline = pipeline = [
        {"$match": {"reviews.rating": {"$gte": 4.0}}},
        {
            "$group": {
                "_id": {
                    "name": "$name",
                    "city": "$city",
                    "province": "$province",
                    "username": "$reviews.username",
                    "rating": "$reviews.rating",
                    "date": "$reviews.date"
                }
            }
        },
        {
            "$project": {
                "name": "$_id.name",
                "city": "$_id.city",
                "province": "$_id.province",
                "username": "$_id.username",
                "rating": "$_id.rating",
                "date": "$_id.date"
            }
        },
        {
            "$sort": {
                "date": -1,
                "province": 1,
                "city": 1,
                "name": -1,
                "rating": -1
            }
        }
    ]

    # Execute the aggregation query
    result = list(mycollection.aggregate(pipeline))
    
    data_list = []
    for i in result:        
        doc_json = {}        
        doc_json["hotel"] = i["name"]
        doc_json["city"] = i["city"]
        doc_json["province"] = i["province"]
        doc_json["username"] = i["username"]
        doc_json["rating"] = i["rating"]
        doc_json["date"] = i["date"]
        data_list.append(doc_json)
    return data_list


