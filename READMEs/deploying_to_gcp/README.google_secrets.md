##

- `gcloud services list --enabled`
- `gcloud services enable secretmanager.googleapis.com`

- `echo -n "YOUR_SECRET_VALUE" | gcloud secrets create SECRET_NAME --data-file=-`
- ie: `echo -n "your_anthropic_api_key" | gcloud secrets create ANTHROPIC_API_KEY --data-file=-`
- ie: `echo -n "render.com url" | gcloud secrets create POSTGRES_URL --data-file=-`
- ie: `echo -n "key for signing JWT" | gcloud secrets create AUTH_SECRET_KEY --data-file=-`
- ie: `echo -n "hashing algorithm" | gcloud secrets create AUTH_ALGORITHM --data-file=-`
- ie: `echo -n "langsmith endpoint" | gcloud secrets create LANGCHAIN_ENDPOINT --data-file=-`
- ie: `echo -n "langsmith API keys" | gcloud secrets create LANGCHAIN_API_KEY --data-file=-`
- ie: `echo -n "embedding api url" | gcloud secrets create EMBEDDING_API_URL --data-file=-`

- CHECK OUT: `https://console.cloud.google.com/security/secret-manager?project=fullstack-rag`

## Granting Cloud Run the permissions to access secrets

- gcloud secrets add-iam-policy-binding SECRET_NAME \
  --member="serviceAccount:YOUR_PROJECT_NUMBER-compute@developer.gserviceaccount.com" \
  --role="roles/secretmanager.secretAccessor"

## ie: this should be scripted

- gcloud secrets add-iam-policy-binding ANTHROPIC_API_KEY \
  --member="serviceAccount:370967482684-compute@developer.gserviceaccount.com" \
  --role="roles/secretmanager.secretAccessor"
- gcloud secrets add-iam-policy-binding POSTGRES_URL \   
  --member="serviceAccount:370967482684-compute@developer.gserviceaccount.com" \
  --role="roles/secretmanager.secretAccessor"
- gcloud secrets add-iam-policy-binding AUTH_SECRET_KEY \  
  --member="serviceAccount:370967482684-compute@developer.gserviceaccount.com" \
  --role="roles/secretmanager.secretAccessor"
- gcloud secrets add-iam-policy-binding AUTH_ALGORITHM \   
  --member="serviceAccount:370967482684-compute@developer.gserviceaccount.com" \
  --role="roles/secretmanager.secretAccessor"
- gcloud secrets add-iam-policy-binding LANGCHAIN_ENDPOINT \   
  --member="serviceAccount:370967482684-compute@developer.gserviceaccount.com" \
  --role="roles/secretmanager.secretAccessor"
- gcloud secrets add-iam-policy-binding LANGCHAIN_API_KEY \   
  --member="serviceAccount:370967482684-compute@developer.gserviceaccount.com" \
  --role="roles/secretmanager.secretAccessor"
- gcloud secrets add-iam-policy-binding EMBEDDING_API_URL \
  --member="serviceAccount:370967482684-compute@developer.gserviceaccount.com" \
  --role="roles/secretmanager.secretAccessor"