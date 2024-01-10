# Difuzer++

**Difuzer++** is a static logic bomb detector.
It is an improved version of our previous tool *Difuzer*.

**Difuzer++** enhance the performance of *Difuzer* by taking into consideration the context of the analyzed apps. More in details, our novel approach involves utilizing multiple OCSVM models trained on sets of similar apps, as opposed to Difuzer, which utilizes a single OCSVM model trained on a set of unrelated apps.

## Getting started

### Downloading the tool

<pre>
git clone https://github.com/Trustworthy-Software/DifuzerPlusPlus
</pre>

### Setup
### 
To execute the entire code, two API keys are required. They should be set in an environment file named *config.env* using the following names: **ANDROZOO_API_KEY** and **OPENAI_API_KEY**.

- 🗝️ **ANDROZOO_API_KEY**: This key is necessary to download apps from the *AndroZoo* Repository, as various operations on the APK files are performed "on-the-fly," such as app download, extraction, and deletion. It can be requested here: [https://androzoo.uni.lu/access](https://androzoo.uni.lu/access)

- 🗝️ **OPENAI_API_KEY**: This key is required to utilize the Embedding models from OpenAI through their official API ([https://platform.openai.com/overview](https://platform.openai.com/overview)).

Moreoveryou need to set in the same *config.env* file:
- **ANDROID_PLATFORM_PATH:** The path to Android platofrms folder.
- **APK_PATH:** The path to the folder where you want to temporarily store the APK files while analyzing them.

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
* The **'manualAnalysis_RQ2b'** folder encompasses the list of new malicious apps that we analyzed in our new paper using*Difuzer++*. This folder also includes our new dataset, **DataBomb++**, which contains 51 new apps that were manually verified to have a logic bomb.

## Google Play Categories

Here, we provide the list of Google Play Categories utilized for our experiments:

| categoryID           | category               |
|----------------------|------------------------|
| ART_AND_DESIGN       | Art & Design           |
| AUTO_AND_VEHICLES    | Auto & Vehicles        |
| BEAUTY               | Beauty                 |
| BOOKS_AND_REFERENCE  | Books & Reference      |
| BUSINESS             | Business               |
| COMICS               | Comics                 |
| COMMUNICATION        | Communication          |
| DATING               | Dating                 |
| EDUCATION            | Education              |
| ENTERTAINMENT        | Entertainment          |
| EVENTS               | Events                 |
| FINANCE              | Finance                |
| FOOD_AND_DRINK       | Food & Drink           |
| GAME_ACTION          | Action                 |
| GAME_ADVENTURE       | Adventure              |
| GAME_ARCADE          | Arcade                 |
| GAME_BOARD           | Board                  |
| GAME_CARD            | Card                   |
| GAME_CASINO          | Casino                 |
| GAME_CASUAL          | Casual                 |
| GAME_EDUCATIONAL     | Educational            |
| GAME_MUSIC           | Music                  |
| GAME_PUZZLE          | Puzzle                 |
| GAME_RACING          | Racing                 |
| GAME_ROLE_PLAYING    | Role Playing           |
| GAME_SIMULATION      | Simulation             |
| GAME_SPORTS          | Sports                 |
| GAME_STRATEGY        | Strategy               |
| GAME_TRIVIA          | Trivia                 |
| GAME_WORD            | Word                   |
| HEALTH_AND_FITNESS   | Health & Fitness       |
| HOUSE_AND_HOME       | House & Home           |
| LIBRARIES_AND_DEMO   | Libraries & Demo       |
| LIFESTYLE            | Lifestyle              |
| MAPS_AND_NAVIGATION  | Maps & Navigation      |
| MEDICAL              | Medical                |
| MUSIC_AND_AUDIO      | Music & Audio          |
| NEWS_AND_MAGAZINES   | News & Magazines       |
| PARENTING            | Parenting              |
| PERSONALIZATION      | Personalization        |
| PHOTOGRAPHY          | Photography            |
| PRODUCTIVITY         | Productivity           |
| SHOPPING             | Shopping               |
| SOCIAL               | Social                 |
| SPORTS               | Sports                 |
| TOOLS                | Tools                  |
| TRAVEL_AND_LOCAL     | Travel & Local         |
| VIDEO_PLAYERS        | Video Players & Editors|
| WEATHER              | Weather                |


## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details

## Contact

For any question regarding this study, please contact us at:
[Marco Alecci](mailto:marco.alecci@uni.lu)
[Jordan Samhi](mailto:jordan.samhi@uni.lu)