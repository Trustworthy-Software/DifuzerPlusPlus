# IMPORT
from   joblib import dump, load
import nltk, re
import subprocess
import requests
import numpy as np
import os

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


# extractFeatures()
# 1) Download APK from AndroZoo
# 2) Launch Difuzer with all details about possible logic bombs (filtering applied)
# 3) Combine the features using predefined delimitators and return them
def extractFeatures(sha256):

    # API Key for Androzoo download and PATHS
    ANDROZOO_API_KEY      = "TO UPDATE"
    ANDROID_PLATFORM_PATH = "TO UPDATE"
    APK_PATH              = "TO UPDATE"
    
    # Download apk from Androzoo
    apkUrl = "https://androzoo.uni.lu/api/download?apikey={}&sha256={}".format(ANDROZOO_API_KEY, sha256)
    req = requests.get(apkUrl, allow_redirects=True)
    open(APK_PATH+'{}.apk'.format(sha256), "wb").write(req.content)

    # Get the features using Difuzer
    command = 'java -jar ./Difuzer-0.1-jar-with-dependencies.jar -a {}{}.apk -p {}'.format(APK_PATH,sha256,ANDROID_PLATFORM_PATH)
    #print("EXECUTING: {}\n".format(command))
    
    # Output from Difuzer
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()

    # Remove apk file
    os.remove(APK_PATH + '{}.apk'.format(sha256))

    # Reorganize features using predefined delimitators
    triggersFeaturesList = output.decode("utf-8").split("@@@\n")[:-1]

    # If empty list
    if len(triggersFeaturesList) == 0:
        return np.nan
        
    for i in range(0,len(triggersFeaturesList)):
        triggersFeaturesList[i] = triggersFeaturesList[i].replace("\n",";")

    if triggersFeaturesList[0] != "":
        for i in range(0, len(triggersFeaturesList)):
            triggersFeaturesList[i] = triggersFeaturesList[i].split(";")
            triggersFeaturesList[i][3] = triggersFeaturesList[i][3].split("$$$")[:-1]

    # Return
    if triggersFeaturesList is not np.nan:
        return triggersFeaturesList
    else:
        return np.nan

# Print a trigger
def printTrigger(trigger):
    fv          = trigger[0]
    method      = trigger[1]
    condition   = trigger[2]
    sources     = trigger[3]

    print("\n⚠️ 💣 - Possible Logic Bomb")
    print("FV       : {}".format(fv))
    print("Method   : {}".format(method))
    print("Condition: {}".format(condition))
    print("Sources  :")
    for s in sources:
        print("     - {}".format(s))

    return

# Get the fields of a trigger
def getTriggerMethodAndSources(trigger):
    fv          = trigger[0]
    method      = trigger[1]
    condition   = trigger[2]
    sources     = trigger[3]

    return method, sources

# Get the ID of the topic assigned by the LDA Model
def getLdaID(vectorizer, ldaModel ,description):
    
    # Needed for NLP
    st              = nltk.stem.snowball.EnglishStemmer()
    english_vocab   = set(w.lower() for w in nltk.corpus.words.words())
    stopwords       = nltk.corpus.stopwords.words('english')
    corpus          = []

    string = description
    string = re.sub(r'\W',' ',string)
    string = re.sub(r'\d','',string)
    tokens = nltk.word_tokenize(string)
    words  = [st.stem(w) for w in tokens if len(w)>=3 and w.lower() not in stopwords and w.lower() in english_vocab]          
    descriptionProcessed = ' '.join(words)       
    corpus.append(descriptionProcessed)

    # Retrieve the Topic ID 
    tf_array  = vectorizer.transform(corpus)
    doc_topic = ldaModel.transform(tf_array)
    lda_id    = doc_topic[0].argmax()

    return lda_id

# Get the ID of the cluster assigned by the KMeans Model
def getKmeansID(vectorizer, kmeansModel ,description):
    
    # Needed for NLP
    st              = nltk.stem.snowball.EnglishStemmer()
    english_vocab   = set(w.lower() for w in nltk.corpus.words.words())
    stopwords       = nltk.corpus.stopwords.words('english')
    corpus          = []

    string = description
    string = re.sub(r'\W',' ',string)
    string = re.sub(r'\d','',string)
    tokens = nltk.word_tokenize(string)
    words  = [st.stem(w) for w in tokens if len(w)>=3 and w.lower() not in stopwords and w.lower() in english_vocab]          
    descriptionProcessed = ' '.join(words)       
    corpus.append(descriptionProcessed)

    # Retrieve the kmeans ID 
    tf_array  = vectorizer.transform(corpus)
    kmeans_id = kmeansModel.predict(tf_array)

    return int(kmeans_id)