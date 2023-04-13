# IMPORT
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster                 import KMeans
from joblib                          import dump, load
import re, nltk
import numpy  as np 
import pandas as pd

# Difuzer++
# 
# Copyright (C) 2023 Marco Alecci
# University of Luxembourg - Interdisciplinary Centre for
# Security Reliability and Trust (SnT) - TruX - All rights reserved
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as
# published by the Free Software Foundation, either version 2.1 of the
# License, or (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Lesser Public License for more details.
# 
# You should have received a copy of the GNU General Lesser Public
# License along with this program.  If not, see <http://www.gnu.org/licenses/lgpl-2.1.html>.

### CONSTANTS 
N_CLUSTERS = 49
INPUT_PATH   = "../../0_Data/CSV/2_trainingAppsCategoriesAndDescriptionsAndFeatures.csv"
OUTPUT_PATH  = "../../0_Data/CSV/3_trainingAppsFeaturesKMEANS.csv"
RESULTS_PATH = "../../0_Data/CSV/statisticsKMEANS.csv"
MODEL_PATH   = "../../0_Data/MODELS/kmeans/"

### INITIALIZATION 
print("⚡ START \n")

# Open CSV File
appsDF = pd.read_csv(INPUT_PATH, index_col=False)
print("#️⃣  APPS: {}\n".format(appsDF.shape[0]))

### PRE PROCESSING 
print("📚  DESCRIPTIONS PRE PROCESSING")
# Needed for NLP
st              = nltk.stem.snowball.EnglishStemmer()
english_vocab   = set(w.lower() for w in nltk.corpus.words.words())
stopwords       = nltk.corpus.stopwords.words('english')
corpus          = []

# Processing the descriptions
for i in range(0,appsDF.shape[0]):
    # Print progress
    if(i%1000==0):
        print("     {} out of {}".format(i,appsDF.shape[0]))

    # Removing stopwords and perform stemming
    string = appsDF.iloc[i]['description'] 
    string = re.sub(r'\W',' ',string)
    string = re.sub(r'\d','',string)
    tokens = nltk.word_tokenize(string)
    words = [st.stem(w) for w in tokens if len(w)>=3 and w.lower() not in stopwords and w.lower() in english_vocab]          
    description = ' '.join(words)       
    corpus.append(description)

###  CLUSTERING 
print("\n🦾 CLUSTERING ")

# Vectorize the descriptions using TF-IDF
vectorizer = TfidfVectorizer()
vectors = vectorizer.fit_transform(corpus)

# Save the Vectorizer 
dump(vectorizer, MODEL_PATH + 'vectorizer.joblib')

# Apply k-means clustering to the vectors
kmeans = KMeans(n_init = 'auto', n_clusters = N_CLUSTERS, random_state = 77, verbose = 1).fit(vectors)

# Save the KMEANS Model
dump(kmeans, MODEL_PATH + 'kmeansModel.joblib')

# Save cluster assingment into appsDF
appsDF['cluster_id'] = kmeans.labels_

# Store num of apps for each cluster
resultsDF = appsDF['cluster_id'].value_counts().to_frame().reset_index()
resultsDF = resultsDF.rename(columns={'index': 'cluster_id', 'cluster_id': 'num_apps'})
resultsDF.set_index('cluster_id',inplace=True)
resultsDF = resultsDF.sort_index()

### RESULTS 
print("\n📝 RESULTS ")
print(resultsDF)

# Remove description and category
appsDF = appsDF.drop(columns = ['description','category'])

# Use cluster_id as index
appsDF['cluster_id'] = appsDF['cluster_id'].astype(int)
appsDF = appsDF.set_index('sha256')

# Store DFs
appsDF.to_csv(OUTPUT_PATH)
resultsDF.to_csv(RESULTS_PATH)

print("🔚 END \n")