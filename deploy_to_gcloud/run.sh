# Run this script from the repository root.

export PROJECT="piranha-plants-as-charade"
export REGION="us-east4"
export CLOUD_RUN_SERVICE="backend"
export ARTIFACT_REGISTRY_REPOSITORY="backend"
export ARTIFACT_REGISTRY_IMAGE="docker-image"

export URL="${REGION}-docker.pkg.dev"
export ARTIFACT_REGISTRY_IMAGE_URI="$URL/$PROJECT/$ARTIFACT_REGISTRY_REPOSITORY/$ARTIFACT_REGISTRY_IMAGE:latest"

# Deploy Docker image to Artifact Registry.
docker build -f ./Dockerfile -t $ARTIFACT_REGISTRY_IMAGE_URI --no-cache --platform linux/amd64 .
gcloud auth configure-docker $URL
docker push $ARTIFACT_REGISTRY_IMAGE_URI

# Deploy service to Cloud Run.
python3 ./deploy_to_gcloud/compile_yaml.py ./deploy_to_gcloud/service.yaml > ./deploy_to_gcloud/service.compiled.yaml
python3 ./deploy_to_gcloud/compile_yaml.py ./deploy_to_gcloud/policy.yaml > ./deploy_to_gcloud/policy.compiled.yaml
gcloud run services delete --region $REGION $CLOUD_RUN_SERVICE
gcloud run services replace ./deploy_to_gcloud/service.compiled.yaml
gcloud run services set-iam-policy --region $REGION $CLOUD_RUN_SERVICE ./deploy_to_gcloud/policy.compiled.yaml