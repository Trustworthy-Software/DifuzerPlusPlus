#Import
from sklearn.ensemble   import IsolationForest
from sklearn.svm        import OneClassSVM
from joblib             import dump, load
from tqdm               import tqdm
import pandas   as pd
import numpy    as np
import itertools
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

# Initializing
print("⚡ STARTING ⚡\n")

####  CMD LINE ARGS
if len(sys.argv) != 2 :
    print("⚠️  Error: Incorrect Usage")
    print("1-approach: 'category' OR 'kmeans' OR 'lda'")
    sys.exit()

### APPROACH CHOICE 
if sys.argv[1] not in ["category", "kmeans", "lda"]:
    print("⚠️  Error: Invalid approach provided. Please use 'category' OR 'kmeans' OR 'lda'")
    sys.exit()
APPROACH = sys.argv[1]

### Initialize MODEL PATH
MODEL_PATH  = "../../0_Data/MODELS/{}/".format(APPROACH)

### Initialize INPUT PATH
if APPROACH == 'category':
    INPUT_PATH   = "../../0_Data/CSV/2_trainingAppsCategoriesAndDescriptionsAndFeatures.csv"
else:
    INPUT_PATH   = "../../0_Data/CSV/3_trainingAppsFeatures{}.csv".format(str.upper(APPROACH))

# Initialize TQDM library for Pandas
tqdm.pandas()

# Load CSV File
appsDF = pd.read_csv(INPUT_PATH,index_col=False)
appsDF = appsDF.rename(columns={'category': 'category_id'})
print("#️⃣  APPS: {}\n".format(appsDF.shape[0]))

# Reorganize features
print("⚙️  Reorganize features")
appsDF['features'] = appsDF['features'].progress_apply(lambda x: [[c for c in r.split(',')] for r in x[:-1].split(';')])

# Renaming
appsDF = appsDF.rename(columns={'category_id': 'approach_id'})
appsDF = appsDF.rename(columns={'topic_id': 'approach_id'})
appsDF = appsDF.rename(columns={'cluster_id': 'approach_id'})

### TRAINING 
print("🦾 TRAINING\n")

# For each category train a model
for approach_id, approachDF in appsDF.groupby('approach_id'):

    # Get the features as a list
    X = list(itertools.chain(*approachDF['features'].tolist()))

    model = OneClassSVM(kernel='rbf',
                        gamma=0.001,
                        cache_size=100,
                        tol=0.0001,         # eps = tol  
                        nu=0.001,
                        shrinking = 1
                        ).fit(X)

    # Dump the model
    dump(model, MODEL_PATH + 'OCSVM_{}.joblib'.format(approach_id))

    # Print statistics about training
    Y = model.predict(X)
    numOutliers = np.count_nonzero(Y == -1)

    print("📝 APPROACH_ID: {}".format(approach_id))
    print("#️⃣  TRIGGERS   : {}".format(len(Y)))
    print("⚠️  OUTLIERS   : {} ({:.0%}) \n".format(numOutliers,numOutliers/len(Y)))

print("🔚 END \n")