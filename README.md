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

To deploy the restaurant similarity recommendation system model, you can begin by running the `training.py` script. This will generate the essential model file called "doc2vec_model.pkl". Once created, you can find the model in the `mlruns/0/<run id>/artifacts/model/` directory.

To proceed with the production deployment on Google Cloud, kindly follow the step-by-step instructions below:

1. Make sure you have a Google Cloud account set up and logged in.
2. Create a new project on Google Cloud if you haven't already.
3. Verify that Google Run and Google Build services are activated for your project.

If you don't have the Google Cloud SDK Command-Line Interface (CLI) installed, you can install it by referring to the documentation at `https://cloud.google.com/sdk/docs/install?hl=en`. Once installed, log in and select your project using the provided instructions in the command line.

Afterwards, execute the following commands to deploy the model:

```bash
gcloud builds submit --tag gcr.io/<APP_ID>/similarity_measure
gcloud run deploy --image gcr.io/<APP_ID>/similarity_measure --platform managed
```

For your convenience, you can explore a successful request example in the `app-request.py` file. Additionally, if you're interested in the web crawling classes, you can find them available in the `WebCrawling` folder.


## Conclusion

Thank you for considering our restaurant similarity recommendation system. We hope that our model and deployment guide have been helpful to you. If you have any questions or require assistance, please don't hesitate to contact us.

Best Regards,

M.A. Sarmento
