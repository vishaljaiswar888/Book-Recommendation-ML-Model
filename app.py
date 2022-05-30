from flask import Flask, render_template, request
import pickle
import numpy as np


app = Flask(__name__)

popular_df = pickle.load(open("model/popular.pkl", "rb"))
pt = pickle.load(open("model/pt.pkl", "rb"))
books = pickle.load(open("model/books.pkl", "rb"))
similarity_scores = pickle.load(open("model/similarity_scores.pkl", "rb"))


@app.route("/")
def index():
    return render_template("index.html", 
    book_name=list(popular_df["Book-Title"].values[:25]),
    author=list(popular_df["Book-Author"].values),
    image=list(popular_df["Image-URL-M"].values),
    votes=list(popular_df["num_ratings"].values),
    ratings=list(np.round(popular_df["avg_ratings"].values, 2))
    )


@app.route("/recommend")
def recommend_ui():
    return render_template("recommend.html")


@app.route("/recommend_books", methods=["POST"])
def recommend():
    user_input = request.form.get("user_input")
    index = np.where(pt.index==user_input)[0][0]
    similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x:x[1], reverse=True)[1:6]
    
    data=[]
    for i in similar_items:
        item = []
        
        # list ko append karne se 2D list ban jata hai, that's why extend
        temp_df = books[books["Book-Title"]==pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates("Book-Title")["Book-Title"].values))
        item.extend(list(temp_df.drop_duplicates("Book-Title")["Book-Author"].values))
        item.extend(list(temp_df.drop_duplicates("Book-Title")["Image-URL-M"].values))
        
        data.append(item)

    print(data)

    return render_template("recommend.html", data=data)


if __name__ == "__main__":
    app.run(debug=True)