# IMPORT
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

    # API Key for Androzoo download
    ANDROZOO_API_KEY = "228e31a59fe25413472e41b7da2ba2f6296435a141f34f3259edb02152c85372"
    ANDROID_PLATFORM_PATH = "/home/marco/android/platforms"
    APK_PATH   = "../../0_Data/APK/"
    
    # Download apk from Androzoo
    apkUrl = "https://androzoo.uni.lu/api/download?apikey={}&sha256={}".format(ANDROZOO_API_KEY, sha256)
    req = requests.get(apkUrl, allow_redirects=True)
    open(APK_PATH+'{}.apk'.format(sha256), "wb").write(req.content)

    # Get the features using Difuzer
    command = 'java -jar ./DifuzerAll.jar -a {}{}.apk -p {}'.format(APK_PATH,sha256,ANDROID_PLATFORM_PATH)
    #print("EXECUTING: {}\n".format(command))
    
    # Output from Difuzer
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()

    # Remove apk file
    os.remove(APK_PATH + '{}.apk'.format(sha256))

    # Split features and put a ;
    features = output.decode("utf-8").replace("\n", ";")

    # Return
    if features is not None and features is not np.nan:
        return features
    else:
        return np.nan