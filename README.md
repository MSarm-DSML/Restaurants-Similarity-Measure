# Restaurant Similarity Recommendation System

## Context

Our system utilizes data from web crawling to identify restaurants that are similar to others. This information can be used for various purposes, including building recommendation systems or providing leads for B2B companies acting as intermediaries between restaurants and clients.

## Data Information

Each dataset in the folder represents a specific city, and within each city, there is a collection of scraped restaurants, along with comments from people who have visited these establishments. The core of our system relies on Natural Language Processing (NLP) techniques, specifically the use of doc2vec, a shallow neural network that measures similarities between topics, in this case, restaurants. It's essential to note that the data shared here is just a small subset of the larger dataset we have collected.

## Deployed Model on Google Cloud

We have deployed our restaurant similarity model on Google Cloud and made it accessible through a POST request on the following URL:
'https://similaritymeasure-74h7jr6qka-oc.a.run.app/similarity_measure'

The input data structure for the request is as follows:
```python
data = {'number': 2}
```
In this structure, each number represents a specific restaurant. The output of the request is a dictionary containing a list of lists, where each list consists of the index of a restaurant and its corresponding degree of similarity to the input restaurant. We provide the 20 closest restaurants based on similarity.

Example Output:
```python
{
    'result': [
        [1421, 0.44397521018981934],
        [8300, 0.4105151295661926],
        [7, 0.4056991934776306],
        ...
    ]
}
```

## Deployment Information

To deploy the model, you must run `training.py`, it will generate the model "doc2vec_model.pkl",
which will be found at `mlruns/0/<run id>/artifacts/model/doc2vec_model.pkl`. To deploy the model to production on Google Cloud, follow these steps:
```bash
gcloud builds submit --tag gcr.io/<APP_ID>/similarity_measure
gcloud run deploy --image gcr.io/<APP_ID>/similarity_measure --platform managed
```

Additionally, you can refer to a successful request example in `app-request.py`, and the web crawling classes are available in the `WebCrawling` folder.

## Thank You

We sincerely appreciate your time and interest in our restaurant similarity recommendation system. If you have any questions or feedback, please feel free to reach out.

Best Regards,

M.A. Sarmento

