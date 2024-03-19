# Use Google Cloud SDK's container as the base image
FROM google/cloud-sdk

# Specify your e-mail address as the maintainer of the container image
LABEL maintainer="dherron@pdx.edu"

# Copy the contents of the current directory into the container directory /app
COPY . /app

# Set the working directory of the container to /app
WORKDIR /app

# Install the Python packages specified by requirements.txt into the container
RUN curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add - && apt update --allow-releaseinfo-change -y && apt install -y python3-pip && pip3 install -r requirements.txt

# This is really just a reminder
# If you stop using secret manager, e.g.,
#gcloud run deploy your-service-name \
#  --image gcr.io/your-project-id/your-image-name \
#  --add-cloudsql-instances your-cloudsql-instance-connection-name \
#  --update-env-vars #OPENAI_API_KEY="secret",GIPHY_API_KEY="secret"
    
ENV OPENAI_API_KEY=
ENV GIPHY_API_KEY=

# Set the parameters to the program
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 app:app
