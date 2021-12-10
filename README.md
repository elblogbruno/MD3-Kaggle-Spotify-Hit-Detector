
![Logo](dataset-cover.jpg)

    
# The Spotify Hit Predictor Dataset (1960-2019)

This repository contains the aproachment to a model to treat the Spotify
hit predictor dataset from [theoverman](https://www.kaggle.com/theoverman) at [Kaggle](https://www.kaggle.com/theoverman/the-spotify-hit-predictor-dataset)

This dataset contains over 40,000+ Tracks labeled hit or flop, with their features extracted from the Spotify Sound Analysis API.

The repository holds the source code of the website https://hitornot.ml/ develop by myself, which uses the model deployed here to simply let you search if your future song will be a hit!



## Features

- Prediction of a song being flop or a hit based on song data such as danceability or song energy! At the time of writing this down, it has this rendiment metrics:
    
| Model Name | Accuracy | Precision | Recall | F1 Score | MSE | Parameters|
| ------------- | ------------- |------------- |------------- |------------- |------------- |------------- |
| Logistic Regression | 50.79   | 50.60  | 62.20   | 0.55 | 0.49  | No Parameters |
| K-Nearest Neighbors | 57.08   | 56.51  | 61.02   | 0.58 | 0.429  | No Parameters |
| Decision Tree| 71.45   | 71.19  | 71.96   | 0.71 | 0.28  |No Parameters |
| Support Vector Machine (Linear Kernel) | 50.98   | 50.47  | 99.85   | 0.67 | 0.49  | { max_iter=5000 } |
| Random Forest | 80.00   | 77.40  | 84.70   | 0.80 | 0.19  |No Parameters |
| Naive Bayes | 62.08   | 57.45  | 92.84   | 0.70 | 0.379  |No Parameters |
| Neural Net | 65.09   | 61.30  | 81.64   | 0.70 | 0.34  |No Parameters |
| AdaBoost | 76.24   | 73.16  | 82.80 | 0.77 | 0.23  |No Parameters |
| Gradient Boosting | 78.76   | 75.08  | 86.04   | 0.80 | 0.21  |No Parameters |


- The website saves the song you search as input data to retrain the model itself so it learns by user new input as well! (Work in progress)
- Jupyter notebook inside with an explanation of the Dataset and my current aproachment to it with an stadistic model!

## Folder Structure

- Src contains the model code
  - You can run model_test.py to test the model and get accuracies.
- Deploy contains the website code
- Jupyter Notebook available at root folder. (md3-spotify-hit-or-not.ipynb)

## Run Website Locally

Clone the project

```bash
  git clone https://github.com/elblogbruno/MD3-Kaggle-Spotify-Hit-Detector
```

Go to the project directory

```bash
  cd MD3-Kaggle-Spotify-Hit-Detector
```

Install dependencies

```bash
  python -m pip install -r requirements.txt
```

Start the server

```bash
  cd deploy && python app.py
```

  
## Tech Stack

**Client:** Plain CSS and HTML, thanks to [@samratcliffe](https://codepen.io/samratcliffe/pen/xOqEZg) 

**Server:** Flask, Jinja2 Templates and SQLAlchemy.

**Model:** Sklearn for model fit and scoring, joblib for deploying the model into the web.

  
## Acknowledgements

 - [@samratcliffe](https://codepen.io/samratcliffe/pen/xOqEZg) for its search design I used on the website.
 - [theoverman](https://www.kaggle.com/theoverman) at [Kaggle](https://www.kaggle.com/theoverman/the-spotify-hit-predictor-dataset) for creating this dataset I really enjoyed working on! I am a music nerd.
 - [annekaosmun](https://www.kaggle.com/annekaosmun/predicting-hit-songs-using-spotify) inspiration for the jupyter notebook.

## Feedback

If you have any feedback, please reach out me at me@brunomoya.com

  