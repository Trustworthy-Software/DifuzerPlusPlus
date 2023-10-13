# IMPORT
from difuzerUtils import *
from joblib       import dump, load
import pandas as pd
import numpy  as np
import sys

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

# For Windows OS
import warnings
warnings.filterwarnings('ignore') 

# DifuzerPRO
print("⚡ DIFUZER++ ⚡\n")

import time
start_time = time.time()

####  CMD LINE ARGS
if len(sys.argv) != 3 :
    print("⚠️  Error: Incorrect Usage")
    print("1-approach: 'category' OR 'kmeans' OR 'lda' OR 'gcata'")
    print("2-dataset :  Path to CSV file with [sha256,pkg_name,category_id,description]")
    sys.exit()

### APPROACH CHOICE 
if sys.argv[1] not in ["category", "kmeans", "lda","gcata"]:
    print("⚠️  Error: Invalid approach provided. Please use 'category' OR 'kmeans' OR 'lda' OR 'gcata'")
    sys.exit()
APPROACH = sys.argv[1]

### Initialize MODEL PATH
MODEL_PATH  = "./0_Data/MODELS/{}/".format(APPROACH)
 
### DATASET 
if ".csv" not in sys.argv[2]:
    print("⚠️  Error: Not a CSV File")
    sys.exit()
DATASET_PATH = sys.argv[2]

### INITIALIZATION 
appsDF = pd.read_csv(DATASET_PATH, index_col=False)
print("#️⃣   APPS      : {}".format(appsDF.shape[0]))
print("⚙️   APPROACH  : {}".format(APPROACH))
print("🗂️   DATASET   : {}".format(DATASET_PATH))

print("\n⚡ RESULTS: ")
# For each app to be analyzed
for i, row in appsDF.iterrows():

    print("\n🔑  SHA256   : {}".format(row['sha256']))
    print("📦  PkgName  : {}".format(row['pkg_name']))

    # 1. Get the ID to load the correct model
    if(APPROACH == 'category'):
        modelID = row['categoryID']
        print("📝  Category : {}".format(modelID))

    if(APPROACH == 'kmeans'):
        vectorizer  = load(MODEL_PATH + "vectorizer.joblib")
        kmeansModel = load(MODEL_PATH + "kmeansModel.joblib")
        modelID = getKmeansID(vectorizer, kmeansModel, row['description'])
        print("📝  KMeans ID : {}".format(modelID))

    if(APPROACH == 'lda'):
        vectorizer  = load(MODEL_PATH + "vectorizer.joblib")
        ldaModel    = load(MODEL_PATH + "ldaModel.joblib")
        modelID = getLdaID(vectorizer, ldaModel, row['description'])
        print("📝  LDA ID   : {}".format(modelID))

    if(APPROACH == 'gcata'):
        gcataModel = load(MODEL_PATH + "gcataModel.joblib")
        modelID  = getGcataID(gcataModel, row['description'])
        print("📝  G-CatA ID   : {}".format(modelID))

    # 2. Load the correspective Model
    try: 
        model = load(MODEL_PATH + 'OCSVM_{}.joblib'.format(modelID)) 
    except FileNotFoundError:
        print("❌ MODEL MISSING")
        continue
    
    # 3. Extract the features using Difuzer
    triggersFeaturesList = extractFeatures(row['sha256'])

    # If empty --> no logic bomb
    if triggersFeaturesList is np.nan:
        continue
    else:
        # 4. For each trigger use the model to predict if it is a SHSO
        for trigger in triggersFeaturesList:    
            # Get the fv
            fv = [np.array([int(c) for c in trigger[0].split(',')])]

            #Predict
            label = model.predict(fv)
        
            # 5. SHSO found
            if(label == -1):
                # Print details about the SHSO
                printTrigger(trigger)

print("🔚 END \n")

# record the ending time
end_time = time.time()
elapsed_time = end_time - start_time
print("Elapsed time:", elapsed_time, "seconds")