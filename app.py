import dill
import pandas as pd
from flask import Flask, render_template,request
from flask import Flask, render_template, url_for, flash, redirect


app = Flask(__name__)

df= pd.DataFrame(dill.load(open('Trailname_comments.pkd', 'rb')))
cosine_similarities= dill.load(open('cos_sim.pkd', 'rb'))

indices = pd.Series(df.index)
TrailName = 'Rock City to the Summit of Mount Diablo'


def recommend(Trail):
    recommended_trails = []
    p =[]
    a =[]
    b =[]

    idx = indices[indices == Trail].index[0]

    score_series = pd.Series(cosine_similarities[idx]).sort_values(ascending=False)
    top_5 = []
    # getting the indexes of the 5 most similar trails
    top_5 = list(score_series.iloc[1:4].index)
    # populating the list with the titles of the best 5 trails
    for i in top_5:
        recommended_trails.append(list(df.index)[i])

    for i in range(0, len(recommended_trails)):
        L = recommended_trails[i].replace(" ", "-")
        a.append(recommended_trails[i])
        url = "https://www.alltrails.com/trail/us/california/" + L
        b.append(url)
    p = list(zip(a,b))
    return p

#print(recommend(TrailName))
R_T = recommend(TrailName)



@app.route("/")
def home():
    return render_template('index.html')

@app.route('/about.html')
def about():
    return render_template('about.html')



@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        TrailName = request.form['TrailName']

        trails = recommend(TrailName)


    return render_template('trails.html',trails = trails,  message='San Francisco Bay Trail Loop')

if __name__== '__main__':

    app.run( )
