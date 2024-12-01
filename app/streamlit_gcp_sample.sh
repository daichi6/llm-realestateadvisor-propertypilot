gcloud config set project adsp-capstone-property-pilot

cd Property-Pilot

cd app


# Clean-up (to get fresh experience) and remove all unused and dangling images
docker system prune -a -f


# Enable Artifact Registry
# gcloud services enable artifactregistry.googleapis.com


# Verify / list repositories
gcloud artifacts repositories list


# Create a repository (if it does  not exist)
# gcloud artifacts repositories create property-pilot-app-final --repository-format=docker --location=us --description="PropertyPilot"


# Build Docker image
docker image build -t us-docker.pkg.dev/adsp-capstone-property-pilot/property-pilot-app-final/cloud-app:latest .


# Push Docker image into artifact registry
docker push us-docker.pkg.dev/adsp-capstone-property-pilot/property-pilot-app-final/cloud-app:latest


# Enable  Cloud Run API
#gcloud services enable run.googleapis.com


# Deploy the Streamlit app to Cloud Run
# Must enable session affinity (sticky routing between a browser session and a serving container)
# This is because Streamlit uses WebSocket connections for rendering the app but it uses an HTTP connection for the file uploader widget. 
# For the app to work correctly, both WebSocket and HTTP connections must be established with the same container instance.
# gcloud run deploy cloud-app \
#  --image=us-docker.pkg.dev/adsp-capstone-once-upon/once-upon/cloud-app:latest \
#  --platform managed \
#  --allow-unauthenticated \
#  --region=us-central1 \
#  --project=adsp-capstone-once-upon


# Delete Streamlit app when no longer needed
#gcloud run services delete cloud-app --region=us-central1 --quiet
