from flask import Flask,render_template,request,jsonify

import requests
import pandas as pd
import data as dt



app = Flask(__name__)






def fetch_overview(movie_id):
    
   movies_overview = pd.read_csv('pkl/movie_overview.csv')
   movies_overview.drop('Unnamed: 0',axis=1,inplace=True)
   
   try:

    z= movies_overview[movies_overview['id']==movie_id].overview.values
    z=z[0]
   
   except:
    z="nothing"

   return z

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=a27a49bf043d4a93c59dccc8ffde1312&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def recommend(movie):
    
        
    movies = pd.read_csv('pkl/movie_list.csv')
    movies.drop('Unnamed: 0',axis=1,inplace=True)
        
    
    similarity = dt.similar()
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    
    recommended_movie=[]

    for i in distances[0:6]:
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].movie_id

        movie_name=movies.iloc[i[0]].title
        try:
            movie_poster=fetch_poster(movie_id)
          
        except:
            movie_poster="image not found"
    
        finally:
            movies_overviews=fetch_overview(movie_id)
            recommended_movie.append((movie_name,movies_overviews,movie_poster))
        


    return recommended_movie

@app.route("/")
def home():
 
    return render_template("home.html")


@app.route('/gettext', methods=["POST"])
def gettext():
    movie=request.json['text_data']
    
    recommended_movie = recommend(movie.lower())
    
    
    return jsonify(recommended_movie)
    

@app.route('/update', methods=['POST'])
def update():
    obj = pd.read_csv('pkl/data.csv')
    obj.drop('Unnamed: 0',axis=1,inplace=True)
    df=obj

#there are three paramether update_name,detail,old_name 
#update name is new name of task
#detail is new detail of task
#old_name is to identify the data in database
    update_name = request.json['user_input']
    update_name=update_name.lower()
    
    datas=df[df['title'].str.match(update_name)].values

    datas=datas.flatten()
    print(datas)
    ls=[]
    for i in datas[0:6]:
        ls.append(i)
    
    
    return ls


@app.route('/movies_data',methods=['GET'])
def movies_data():
    new=pd.read_csv('pkl/movies.csv')
    new.drop('Unnamed: 0',axis=1,inplace=True)
    df=new
    
    x=df.sample(12)
    x['image']=x['movie_id'].apply(fetch_poster)
    list=[]
    for i in zip(x['title'],x['tags'],x['image']):
        list.append(i)
    return jsonify(list)
    


#invalid url
@app.errorhandler(404)
def page_not_found(e):
    return  "404"

#internal server
@app.errorhandler(500)
def page_not_found(e):
    return "500"




if __name__ == "__main__":
    


    app.run(debug=False)
