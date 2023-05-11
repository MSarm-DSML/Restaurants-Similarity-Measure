# Context

We use data from Web crawling to pinpoint restaurants similar to others. It may serve both for the purpose of recommendation system or lead for a b2b company intermediary between restaurants and clients. 

# Info

Each data set in the folder represents a city, and within each city, there is a collection of scraped restaurants, 
including comments from people who have visited these establishments. The NLP code I used employs doc2vec, a shallow neural network that provides similarities between topics, in this case, restaurants. I should also note that the data I shared is just a small subset of the larger dataset I have collected. The scraping code has not been displayed here. Whether this will be or not made available has not yet been decided.

# Instructions 


Run main to generate the model to production.
Deploy the model to production:
Running deploy.py you will create a server within your pc which can be used to respond clients requests. 
See a successful request in deploy-verified.ipynb. 

# Thanks

Thank you for your time and consideration.

Best regards,

M.A.Sarmento.

