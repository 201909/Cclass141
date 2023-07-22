from flask import Flask, jsonify, request
import pandas as pd
from demographic_filtering import output
from contentBased_filtering import get_recommendations

articles = pd.read_csv("articles.csv")
app = Flask(__name__)

all_articles = articles[["timestamp","eventType","contentId","authorPersonId","authorSessionId","authorUserAgent","authorRegion","authorCountry"
                         ,"contentType","url","title"]]

liked_articles = []
not_liked_articles = []
@app.route("/article")
def get_movie():
    a_data = {
        "title": all_articles.iloc[0,0],
        "url": all_articles.iloc[0,1],
        "text": all_articles.iloc[0,2] or "N/A",
        "lang": all_articles.iloc[0,3],
        "total_events":all_articles.iloc[0,4]/2
    }
    return jsonify({
        "data": all_articles[10],
        "status": "success"
    })

@app.route('/liked')
def liked():
    global liked_articles    

    return jsonify({
        'data' : liked_articles , 
        'status' : 'success'
    })

@app.route("/dislike")
def unliked_movie():
    global not_liked_articles
    not_liked_articles.append(articles)
    all_articles.drop([0], inplace=True)
    all_articles=all_articles.reset_index(drop=True)
    
    return jsonify({
        "status": "success"
    })

@app.route("/get_reccomendations")
def get_reccomendation():
    col_names=["url","title", "text", "lang", "total_events"]
    all_recommended = pd.DataFrame(columns=col_names)
    
    for liked_movie in liked_articles:
        
        output = get_recommendations(liked_movie["contentId"])
        all_recommended=all_recommended.append(output)

    all_recommended.drop_duplicates(subset=["contentId"],inplace=True)

    recommended_articles=[]

    for index, row in all_recommended.iterrows():
        _p = {
            "title": row["title"],
            "url":row['url'],
            "text":row['text'] or "N/A",
            "lang": row['lang'],
            "total_events": row['total_events']/2
        }
        recommended_articles.append(_p)

    return jsonify({
        "data":recommended_articles,
        "status": "success"
    })

if __name__ == "__main__":
  app.run()
