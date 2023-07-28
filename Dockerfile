#    http://www.apache.org/licenses/LICENSE-2.0
FROM python:3.10.9-slim

# Allow statements and log messages to immediately appear in the Knative logs
ENV PYTHONUNBUFFERED True

# Copy local code to the container image.
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

# Install production dependencies.
RUN pip install -r requirements.txt

# Run the web service on container startup. Here we use the gunicorn
# webserver, with one worker process and 8 threads.
# For environments with multiple CPU cores, increase the number of workers
# to be equal to the cores available.
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 main:app


## gcloud builds submit --tag gcr.io/testoncloud-394113/similarity_measure
## gcloud run deploy --image gcr.io/testoncloud-394113/similarity_measure --platform managed

