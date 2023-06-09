# Difuzer++

**Difuzer++** is a static logic bomb detector.
It is an improved version of our previous tool [*Difuzer*](https://github.com/Trustworthy-Software/Difuzer).

**Difuzer++** enhance the performance of *Difuzer* by taking into consideration the context of the analyzed apps. More in details, our novel approach involves utilizing multiple OCSVM models trained on sets of similar apps, as opposed to Difuzer, which utilizes a single OCSVM model trained on a set of unrelated apps.

## Getting started

### Downloading the tool

<pre>
git clone https://github.com/Trustworthy-Software/DifuzerPlusPlus
</pre>

### Setup
In the ```difuzerUtils.py``` file you should update the following values:
* **ANDROZOO_API_KEY:** your AndroZoo API KEY to download the apps from AndroZoo Repository.
* **ANDROID_PLATFORM_PATH:** The path to Android platofrms folder.
* **APK_PATH:** The path to the folder where you want to temporarily store the APK files while analyzing them.

### Usage
<pre>
python3 Difuzer++.py <i>approach</i> <i>dataset</i>
</pre>

Parameters:

* ```approach``` : The approach used to categorize the apps during the training phase: [**'category'** OR **'kmeans'** OR **'lda'**]
* ```dataset```  : The path to **CSV file** that contains the list of applications to be analyzed. It should have the following columns: [sha256, pkg_name, category_id, description]

## Models
The repository includes all the trained OCSVM models required for launching **Difuzer++**.

If you would like to train the model from scratch, the **'1_TrainingPhase'** folder contains the scripts utilized for preprocessing the data and training the models.

## Data
In the folder named **'0_Data'**, you will come across three distinct subfolders that contain multiple CSV files:
* The **'training'** folder comprises the list of applications utilized for training the models.
* The **'dataBomb_RQ2a'** folder contains our **DataBomb** dataset, which includes a list of apps confirmed to have at least one logic bomb, as described in our previous paper *Difuzer*. One version of this dataset already consists of the Google Play CategoryID and the Description of each app. This file is readily usable as input for *Difuzer++*, without the need for any additional processing.
* The **'manualAnalysis_RQ2b'** folder encompasses the list of new malicious apps that we analyzed in our new paper using*Difuzer++*. This folder also includes our new dataset, **DataBomb++**, which contains 44 new apps that were manually verified to have a logic bomb.

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details

## Contact

For any question regarding this study, please contact us at:
[Marco Alecci](mailto:marco.alecci@uni.lu)
[Jordan Samhi](mailto:jordan.samhi@uni.lu)
