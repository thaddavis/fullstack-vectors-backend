# TLDR

Documenting steps of deploying `Fullstack R.A.G.` to GCP

## Reference links

- https://cloud.google.com/run/docs/quickstarts/frameworks/deploy-nextjs-service
- https://cloud.google.com/run/docs/quickstarts/build-and-deploy/deploy-nodejs-service

## Deployment steps

- install gcloud - `gcloud --version`
  - if gcloud isn't installed: https://cloud.google.com/sdk/docs/install
- focused on deploying the frontend
- after dealing with the frontend, I continued with backend: `https://medium.com/@smoolagani.dev/building-a-gcp-postgresql-connector-with-fastapi-sqlalchemy-and-docker-974620be635b`

## Setting up Postgres in Render.com

- Go to: `https://render.com/`
- `External Database URL` provides you with a connection string
  - used for `POSTGRES_URL` url

## Set up GCR config

- add `Dockerfile.prod`
- add `cloudbuild.yaml`
- add `service.yaml`

## Fullstack R.A.G. FastAPI service deployment steps

- Enable the Artifact Registry API on your GCP project
  - `gcloud artifacts repositories create fullstack-rag-fastapi --repository-format docker --project fullstack-rag --location us-central1` √
  - VERIFY: https://console.cloud.google.com/artifacts?project=fullstack-rag
- `touch Dockerfile.prod`
- `touch cloudbuild.yaml`
- `gcloud builds submit --config=cloudbuild.yaml --project fullstack-rag .` √

## Settings up secrets "properly"

- check out `README.google_secrets.md`

## Back at it

- Check the GCP console after submitting the build: https://console.cloud.google.com/artifacts
  - `touch service.yaml`
- `gcloud run services replace service.yaml --region us-east1`
- `touch gcr-service-policy.yaml`
- `gcloud run services set-iam-policy fullstack-rag-fastapi-service gcr-service-policy.yaml --region us-east1`

