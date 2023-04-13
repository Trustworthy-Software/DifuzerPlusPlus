# IMPORT
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition           import LatentDirichletAllocation as LDA
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
N_TOPICS = 49
INPUT_PATH   = "../../0_Data/CSV/2_trainingAppsCategoriesAndDescriptionsAndFeatures.csv"
OUTPUT_PATH  = "../../0_Data/CSV/3_trainingAppsFeaturesLDA.csv"
RESULTS_PATH = "../../0_Data/CSV/statisticsLDA.csv"
MODEL_PATH   = "../../0_Data/MODELS/lda/"

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
print("\n🦾 LDA MODEL ")
# Get Feature Vectors from the corpus
NumApp      = len(corpus)   
vectorizer  = CountVectorizer(stop_words='english', strip_accents='ascii', dtype='int32')#, max_features=NumFeatures)
tf_array    = vectorizer.fit_transform(corpus).toarray()
vocab       = vectorizer.get_feature_names_out()

# Save the Vectorizer 
dump(vectorizer, MODEL_PATH + 'vectorizer.joblib')

# LDA MODEL
ldaModel = LDA(n_components = N_TOPICS, max_iter=100, random_state = 1,verbose=1)

# Fit the LDA Model and get the topics
ldaModel.fit_transform(tf_array)
topic_words = ldaModel.components_

# Save the LDA Model
dump(ldaModel, MODEL_PATH + 'ldaModel.joblib')

### RESULTS 
print("\n📝 RESULTS ")

# Create resultsDF to store results of clustering
resultsDF = pd.DataFrame(columns= ['topic_id','top10_words','num_apps', 'package_names'])

# Retrieve topics and 10 most used words for each topic
n_top_words = 10
for t, topic_dist in enumerate(topic_words):
    # Retrieve top 10 words for each topic
    topic_words = np.array(vocab)[np.argsort(topic_dist)][:-n_top_words:-1]

    # Add row to thre ResultDF
    insert_row = {
        "topic_id":      t,
        "top10_words":   topic_words.tolist(),
        "num_apps":      0,
        "package_names": []
    }
    resultsDF = pd.concat([resultsDF, pd.DataFrame([insert_row])])

# Set topic_id as index of ResultDF
resultsDF = resultsDF.set_index('topic_id')

# Add new empty columns to appsDF to store the topic_id
appsDF["topic_id"] = np.nan

# Retrieve topics of dapps and store them into appsDF
doc_topic = ldaModel.transform(tf_array)
for i in range(NumApp):
    # Get the first topic_id for each app
    topic_id = doc_topic[i].argmax()

    # Count num of apps for each topic and store the pkg_name into resultsDF
    resultsDF.at[topic_id,'num_apps'] += 1
    resultsDF.at[topic_id,'package_names'].append(appsDF.iloc[i]['pkg_name'])

    # Store topic_id also in appsDF
    appsDF.at[i,'topic_id'] = topic_id

### END 
# Print and save resultsDF into CSV
print("\n📝 RESULTS ")
print(resultsDF)
resultsDF.drop('package_names', axis=1, inplace=True)

# Remove description and category
appsDF = appsDF.drop(columns = ['description','category'])

# Use topic_id as index
appsDF['topic_id'] = appsDF['topic_id'].astype(int)
appsDF = appsDF.set_index('sha256')

# Store appsDF with topic_id for each app
appsDF.to_csv(OUTPUT_PATH)
resultsDF.to_csv(RESULTS_PATH)

print("🔚 END \n")