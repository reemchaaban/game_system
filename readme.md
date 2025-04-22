# Game System

This project was developed to provide **Digital Game Storefronts and Services** (e.g. [Steam](https://store.steampowered.com/), [PSN](https://www.playstation.com/)) with ML models that provide business benefits. These ML models were containerized then deployed on [Railway](https://railway.com/) and linked to a user-friendly UI utilizing Streamlit, accessible via browser.

Link to Streamlit web application: [https://gamesystem-503n.up.railway.app/](https://gamesystem-503n.up.railway.app/)

## Dataset

Using [`SteamSpy`](https://steamspy.com/) API and [`SteamDB`](https://steamdb.info/), data on the top 200 most played games on Steam was collected. The training datasets were built based off these 200 games, as explained below. 
All datasets used to train the models can be accessed [`here`](https://drive.google.com/drive/folders/1fFQMx17cBngObj5GBxtfAppgTJzdmTIg?usp=sharing).

## Internal Endpoints (IEPs)

The following apply to each IEP:
- It is a model exposed through a [Flask](https://flask.palletsprojects.com/en/stable/) API.
- Containerized separately using [Docker](https://www.docker.com/) based on the `Dockerfile` in the corresponding folder.
- Model training metrics are logged by [MLflow](https://mlflow.org/) during the training process.
- System-level metrics are logged by [Prometheus](https://prometheus.io/) during the training process, and visualized on [Grafana](https://grafana.com/).
-  **Automatic Updates**: If the dataset updates, re-running the training notebook will re-train the model on the new dataset as it pulls the data from **Google Drive**. The new model is then automatically pushed to this repository, triggering the GitHub workflow `build_containers.yml`. This workflow checks which of the 2 models were updated, re-builds the corresponding container and pushes it to Docker Hub.
-  **Unit and Integration Test**: Tests that verify the query model functions and [Flask](https://flask.palletsprojects.com/en/stable/) API endpoints are working as expected.

### IEP #1

An LSTM model that predicts the number of online players on a given date in the future, allowing for dynamic infrastructure resource scaling, and thus, reduced infrastructure costs.

-  `input`: A date in the future (e.g. October 26, 2026).

-  `Output`: A predicted number of online players (e.g. 5,385,754 online players).

-  `Dataset`: For each of the 100 games, the daily player count was manually collected from the `SteamDB` API from a given start date (chosen based on the existence of player data for more recent games).

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

## Deployment 

Each Docker image (IEP1, IEP2, EEP, and frontend) was deployed on [Railway](https://railway.com/) straight from Docker Hub and given a public URL. 

## Docker Compose

Docker Compose was used to containerize the external endpoint and internal endpoints and orchestrate them.
- Frontend is exposed on port `8501`
- EEP is exposed on port `8000`
- IEP1 is exposed on port `8001`
- IEP2 is exposed on port `8002`

To build & start all images:
```bash
docker-compose up --build
```
- This will build the Docker images from their respective directories (./frontend, ./EEP, ./IEP1, ./IEP2) & start them with the aforementioned port mappings. After running the above command, go to the following URL to access the Streamlit app locally via browser: `http://localhost:8501/`

To stop them:
```bash
docker-compose down
```

## Swagger 

To document API interactions, I decided to add a Swagger file for the external endpoint, covering all endpoints. Swagger provides a visual interface to interact with the APIs, test the input & output, and validate the format of requests; this is used in the industry to enable frontend/backend collaboration, as it's helpful for understanding how to query the ML models.

To visualize the Swagger file, paste the full `swagger_eep.yaml` file in this repository in the following link: `https://editor.swagger.io/`
