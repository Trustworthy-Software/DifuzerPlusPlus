# IMPORT
from   tqdm import tqdm
import google_play_scraper
import langdetect
import numpy  as np
import pandas as pd
import redis

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

# Retrieve Category and Descriptions from Apps present on the Google Play Store + removing non english descriptions

# PATH
INPUT_PATH  = "../../0_Data/CSV/0_trainingApps.csv"
OUTPUT_PATH = "../../0_Data/CSV/1_trainingAppsCategoriesAndDescriptions.csv"

### INITIALIZATION 
print("⚡ START \n")

# Initialize TQDM library for Pandas
tqdm.pandas()

# Open CSV File
appsDF = pd.read_csv(INPUT_PATH, index_col=False)
print("#️⃣  APPS: {}".format(appsDF.shape[0]))

# Keep only sha256 and pkg_name and add new columns for description and category_id
appsDF = appsDF[['sha256','pkg_name']]

# Add new columns for Category,Description and Language
appsDF["category_id"]    = np.nan
appsDF["description"] = np.nan

###  PREPROCESS
# Function to get Category and Description from PlayStore
def getCategoryAndDescription(pkg_name):
    try:
        result = google_play_scraper.app(   pkg_name, 
                        lang='en', 
                        country='us')

        if result != None:
            if result['description'] != None:
                return pd.Series([result['genreId'], result['description'].replace('\n', ' ').replace('\r', '')],index=['category_id','description'])
            else:
                return pd.Series([np.nan,np.nan],index=['category_id','description'])
        else:
            return pd.Series([np.nan,np.nan],index=['category_id','description'])
    except google_play_scraper.exceptions.NotFoundError:
        return pd.Series([np.nan,np.nan],index=['category_id','description'])
    
# Function to detect language
def getLang(text):
    try:
        lang = langdetect.detect(text)
        return lang
    except langdetect.lang_detect_exception.LangDetectException:
        return np.nan    
    
print("⚙️  Get info from Google Play Store")
appsDF[['category_id','description']] = appsDF["pkg_name"].progress_apply(getCategoryAndDescription)
appsDF = appsDF.dropna()
print("\n#️⃣  APPS AVAILABLE WITH CATEGORY AND DESCRIPTION: {}\n".format(appsDF.shape[0]))

print("⚙️  Removing non English Descriptions")
appsDF["language"] = np.nan
appsDF["language"] = appsDF["description"].progress_apply(getLang)
appsDF = appsDF[appsDF['language'] == 'en']
appsDF = appsDF.drop(columns=['language'])
print("\n#️⃣  APPS AVAILABLE : {}\n".format(appsDF.shape[0]))

### END
# Store results
appsDF = appsDF.set_index('sha256')
appsDF.to_csv(OUTPUT_PATH)

print("🔚 END \n")