# IMPORT
from difuzerUtils import *
from tqdm import tqdm
import pandas as pd
import numpy  as np

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

### PATH
# Goodwares with Descriptions
INPUT_PATH  = "../../0_Data/CSV/1_trainingAppsCategoriesAndDescriptions.csv"
OUTPUT_PATH = "../../0_Data/CSV/2_trainingAppsCategoriesAndDescriptionsAndFeatures.csv"

### INITIALIZATION 
print("⚡ START \n")

# Initialize TQDM library for Pandas
tqdm.pandas()

# Open CSV File
appsDF = pd.read_csv(INPUT_PATH, index_col=False)
print("#️⃣  APPS: {}\n".format(appsDF.shape[0]))

# TEST
appsDF = appsDF.head(10)

# Add new column for features
appsDF["features"] = np.nan

# Extract Features
print("⚙️  ExtractingFeatures\n")
appsDF["features"] = appsDF["sha256"].progress_apply(extractFeatures)
appsDF = appsDF.replace(r'^\s*$', np.nan, regex=True)
appsDF = appsDF.dropna(how='any')
print("\n#️⃣  APPS with features: {}\n".format(appsDF.shape[0]))

### END 
# Save the DF
print("⚙️  Saving the DF")
appsDF = appsDF.set_index('sha256')
appsDF.to_csv(OUTPUT_PATH)

print("\n🔚 END \n")