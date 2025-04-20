
# RAILWAY BRIEFLY MENTIONED IN CASE WE NEED TO CHANGE IT; WHOLE SECTION LATER

# ADD ACTUAL DEPLOYMENT LINK

# Game System

This project was developed to provide **Digital Game Storefronts and Services** (e.g. [Steam](https://store.steampowered.com/), [PSN](https://www.playstation.com/)) with ML models that provide business benefits. These ML models were containerized then deployed on [Railway](https://railway.com/) and linked to a user-friendly UI utilizing Streamlit, accessible via browser.
## Dataset

Using [`SteamSpy`](https://steamspy.com/) and [`SteamDB`](https://steamdb.info/) API, data on the top 200 most played games on Steam was collected. The training datasets were built based off these 200 games, as explained below.

## Internal Endpoints (IEPs)

The following apply to each IEP:
- It is a model exposed through a [Flask](https://flask.palletsprojects.com/en/stable/) API.
- Containerized separately using [Docker](https://www.docker.com/) based on the `Dockerfile` in the corresponding folder.
- Model training metrics are logged by [MLflow](https://mlflow.org/) during the training process.
- System-level metrics are locked by [Prometheus](https://prometheus.io/) during the training process, and visualized on [Grafana](https://grafana.com/).
-  **Automatic Updates**: If the dataset updates, re-running the training notebook will re-train the model on the new dataset as it pulls the data from **Google Drive**. Then, the new model is automatically pushed to this repository, triggering the GitHub workflow `build_containers.yml`. This workflow checks which of the 2 models was updated, re-builds the corresponding container and pushes it to Docker Hub.
-  **Unit and Integration Test**: Tests that verify the query model functions and [Flask](https://flask.palletsprojects.com/en/stable/) API endpoints are working as expected.

### IEP #1

An LSTM model that predicts the number of online players on a given date in the future, allowing for dynamic infrastructure resource scaling, and thus, reduced infrastructure costs.

-  `input`: A date in the future (e.g. October 26, 2026).

-  `Output`: A predicted number of online players (e.g. 5,385,754 online players).

-  `Dataset`: For each of the 200 games, the daily player count was collected from the `SteamDB` API from a given start date (chosen based on the existence of player data for more recent games).

- The model accounts for weekends and holidays to provide more accurate predictions.
 

### IEP #2

A LightFM model that recommends games to gamers based on their existing game library, which would increase game sales through targeted advertising, similar to Steam's "[Discovery Queue](https://store.steampowered.com/about/newstore)" feature.

-  `input`: A player's game library, including number of hours in each game to signify their likeness to the game.

```json
{

"Call of Duty": 145,

"Apex Legends": 213,

...
}
```
-  `Output`: A list of 5 game recommendations, including each game's price, rating, genre and tags.

-  `Dataset`: For each of the 200 games, metadata was collected (price, rating, genre and tags). Then, a sample of 50,000 player game libraries was synthetically generated through code, ensuring that all genres had players who had it as their preferred genre, thus creating an exhaustive dataset.

- The model accounts for preferred genres and number of hours played to make better recommendations.

## External Endpoint (EEP)

A user-friendly UI built through the [Streamlit](https://streamlit.io/) framework and an intermediate [Flask](https://flask.palletsprojects.com/en/stable/) API that handles data validation, querying and providing the responses of the models. The intermediate [Flask](https://flask.palletsprojects.com/en/stable/) app was also containerized separately using [Docker](https://www.docker.com/).