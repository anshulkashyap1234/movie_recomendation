
import pandas as pd 


from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def similar():
    new=pd.read_csv('pkl/movies.csv')
    new.drop('Unnamed: 0',axis=1,inplace=True)

   


    cv = CountVectorizer(max_features=5000,stop_words='english')
    vector = cv.fit_transform(new['tags']).toarray()
    similarity = cosine_similarity(vector)
    return similarity

    
   







