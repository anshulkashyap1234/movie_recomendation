
import pandas as pd 


from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
new=pd.read_csv('pkl/movies.csv')

def similar():

   


    cv = CountVectorizer(max_features=5000,stop_words='english')
    vector = cv.fit_transform(new['tags']).toarray()
    similarity = cosine_similarity(vector)
    return similarity

    
   







