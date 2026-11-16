# Video 05 — Deploy ML Models from Private S3 Storage with KServe and MinIO

**YouTube video:** To be added after publication.

In this episode, we configure KServe to download a model from **private S3-compatible object storage**. We run MinIO locally inside Kubernetes, train and upload a Scikit-learn Iris model, configure storage credentials, and deploy the model through a KServe `InferenceService`.

The demonstration uses MinIO so that you can learn the S3 authentication workflow locally without an AWS account or cloud storage charges.

## What you will learn

- Where KServe can retrieve model artifacts from using `storageUri`.
- How the KServe storage initializer downloads model files before the model server starts.
- How to run MinIO as a local S3-compatible object-storage service in Kubernetes.
- How to train and serialize a Scikit-learn model and upload it to MinIO with Boto3.
- How a Kubernetes Secret stores the S3-compatible endpoint settings and access credentials.
- How a ServiceAccount references that Secret.
- How an InferenceService selects the ServiceAccount using `serviceAccountName`.
- How to check deployment readiness and troubleshoot storage-initializer failures.
- How the local static-credential demonstration relates to AWS IAM Roles for Service Accounts (IRSA).

## Prerequisites

- A Kubernetes cluster with KServe installed. The earlier episodes use a local `kind` cluster and KServe Standard mode.
- `kubectl` configured to access the cluster.
- Python 3 and `pip` on the machine where you will run the upload script.
- The ability to run `kubectl port-forward`.
- The Episode 4 sample request file, also included in this directory as [`iris-input.json`](iris-input.json).

If you are following the series in order, start with [Video 03 — Installing KServe](../video-03-kserve-installation/README.md) and [Video 04 — Deploying your first model](../video-04-first-model-deployment/README.md).

## Files in this directory

| File | Purpose |
|---|---|
| [`minio.yaml`](minio.yaml) | Deploys MinIO and creates an internal Kubernetes Service in the `minio` namespace. |
| [`train_and_upload.py`](train_and_upload.py) | Trains a small Iris SVM model, saves `model.joblib`, creates the `models` bucket, and uploads the artifact. |
| [`s3-secret.yaml`](s3-secret.yaml) | Defines the S3-compatible endpoint settings and MinIO access credentials for KServe. |
| [`s3-sa.yaml`](s3-sa.yaml) | Creates the ServiceAccount that references the Secret. |
| [`sklearn-iris-s3.yaml`](sklearn-iris-s3.yaml) | Defines the KServe InferenceService and points it to the private model location. |
| [`iris-input.json`](iris-input.json) | Sample V1 inference request used to test the deployed model. |

## 1. Where can a model live?

The `storageUri` field in an InferenceService tells KServe where the model artifacts are stored. The URI scheme indicates the storage type.

| URI prefix | Storage type |
|---|---|
| `s3://` | Amazon S3 and S3-compatible object storage such as MinIO |
| `gs://` | Google Cloud Storage |
| `https://` | A file available at a web address |
| `pvc://` | A Kubernetes PersistentVolumeClaim |
| `hf://` | A model hosted on Hugging Face |

The episode focuses on `s3://`. The script also introduces Git repositories and OCI container images with Modelcars as other ways to package or retrieve model artifacts.

## 2. How KServe retrieves a private model

When the serving workload starts, KServe's **storage initializer** reads the model's `storageUri`, connects to the storage backend, and downloads the model artifacts. The model server can then load the downloaded files.

For private S3-compatible storage, this demonstration connects three Kubernetes resources:

1. **Secret — `s3creds`:** contains the access key, secret key, and KServe S3 connection annotations.
2. **ServiceAccount — `sa`:** references the `s3creds` Secret.
3. **InferenceService — `sklearn-iris-s3`:** selects the ServiceAccount through `predictor.serviceAccountName`.

Keep this relationship in mind when troubleshooting: the InferenceService must name the correct ServiceAccount, the ServiceAccount must reference the correct Secret, and the Secret must contain valid credentials and endpoint settings.

## 3. Deploy MinIO inside Kubernetes

The supplied [`minio.yaml`](minio.yaml) creates a Deployment and Service in the `minio` namespace. The Deployment runs one MinIO instance, stores its data under `/data` inside the container, and exposes the S3 API on port `9000`.

Create the namespace:

```bash
kubectl create namespace minio
```

Deploy MinIO:

```bash
kubectl apply -f minio.yaml
```

Wait for the Deployment:

```bash
kubectl rollout status deployment/minio -n minio
```

Forward the MinIO Service to your local machine:

```bash
kubectl port-forward -n minio svc/minio 9000:9000
```

Keep this terminal running. Your local upload script will connect to MinIO at `http://localhost:9000`.

### Important: demonstration credentials

The supplied demonstration manifests and Python script use the sample MinIO credentials `minioadmin` / `minioadmin123` so the local walkthrough is reproducible. **These are demonstration-only credentials. Do not reuse them in production or expose real credentials in source control.** For a real deployment, use strong credentials, restrict access, and manage secrets through an appropriate secure process.

## 4. Train a model and upload it to MinIO

The [`train_and_upload.py`](train_and_upload.py) script performs three actions:

1. Loads the Iris dataset and trains a Scikit-learn Support Vector Classifier (SVC).
2. Serializes the trained model to `model.joblib`.
3. Creates a bucket named `models` and uploads the model to the object key `iris/model.joblib`.

Install the Python dependencies:

```bash
pip install boto3 joblib scikit-learn
```

With the MinIO port-forward still running, execute the script from this directory:

```bash
python train_and_upload.py
```

The script uses Boto3 with the local endpoint `http://localhost:9000` and the same sample credentials configured in the MinIO Deployment.

The model is uploaded to:

```text
s3://models/iris/model.joblib
```

The bucket is `models`; the object key is `iris/model.joblib`. The InferenceService will use the folder-style URI `s3://models/iris/`.

## 5. Give KServe access to MinIO

The upload script connects from your machine through `localhost:9000`. KServe runs inside Kubernetes, so it must use the in-cluster Service DNS name instead:

```text
minio.minio.svc.cluster.local:9000
```

This distinction is important: **localhost is the host-side port-forward; the Kubernetes DNS name is the endpoint used by KServe inside the cluster.**

### 5.1 Create the Kubernetes Secret

Review [`s3-secret.yaml`](s3-secret.yaml). It creates a Secret named `s3creds` in the `kserve-test` namespace.

The Secret contains two categories of configuration:

- Annotations that tell KServe the MinIO endpoint, that this local endpoint uses HTTP, and the S3 region setting.
- `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` values under `stringData`.

The annotations used in this local demo are:

| Annotation | Value | Purpose |
|---|---|---|
| `serving.kserve.io/s3-endpoint` | `minio.minio.svc.cluster.local:9000` | In-cluster MinIO endpoint |
| `serving.kserve.io/s3-usehttps` | `0` | Uses HTTP for this local MinIO setup |
| `serving.kserve.io/s3-region` | `us-east-1` | S3 region setting expected by the client; this does not mean the demo connects to AWS |

### 5.2 Create the ServiceAccount

Review [`s3-sa.yaml`](s3-sa.yaml). It creates a ServiceAccount named `sa` in `kserve-test` and references the `s3creds` Secret.

### 5.3 Configure the InferenceService

Review [`sklearn-iris-s3.yaml`](sklearn-iris-s3.yaml).

Important fields:

| Field | Value | Purpose |
|---|---|---|
| `metadata.name` | `sklearn-iris-s3` | InferenceService name |
| `metadata.namespace` | `kserve-test` | Namespace for the model |
| `predictor.serviceAccountName` | `sa` | Selects the ServiceAccount linked to the Secret |
| `model.modelFormat.name` | `sklearn` | Identifies the model format |
| `model.storageUri` | `s3://models/iris/` | Points to the model's bucket and prefix |

The `storageUri` still uses the `s3://` scheme even though the storage server is MinIO. The custom endpoint annotation in the Secret tells KServe where that S3-compatible service is running.

## 6. Apply the resources in order

The `kserve-test` namespace is where the Secret, ServiceAccount, and InferenceService are created. If you already created this namespace in the previous episode, you can skip the namespace creation command.

```bash
kubectl create namespace kserve-test
```

Apply the Secret first:

```bash
kubectl apply -f s3-secret.yaml
```

Apply the ServiceAccount:

```bash
kubectl apply -f s3-sa.yaml
```

Finally, deploy the InferenceService:

```bash
kubectl apply -f sklearn-iris-s3.yaml
```

The relationship is now:

```text
InferenceService: sklearn-iris-s3
        |
        | serviceAccountName: sa
        v
ServiceAccount: sa
        |
        | references Secret: s3creds
        v
Secret: s3creds
        |
        | MinIO endpoint + credentials
        v
MinIO: s3://models/iris/
        |
        | contains model.joblib
        v
Storage initializer downloads the model
        |
        v
Scikit-learn model server loads the model
```

## 7. Verify the deployment

Check the InferenceService:

```bash
kubectl get inferenceservice sklearn-iris-s3 -n kserve-test
```

Check the pods:

```bash
kubectl get pods -n kserve-test
```

Wait until the InferenceService reports `READY=True` and the serving pod is healthy. The storage initializer must successfully retrieve the model before the model server can serve predictions.

## 8. Send a prediction request

The sample request is included as [`iris-input.json`](iris-input.json). Forward the predictor Service to local port `8081`:

```bash
kubectl port-forward -n kserve-test svc/sklearn-iris-s3-predictor 8081:80
```

Keep the port-forward terminal running. In another terminal, run:

```bash
curl -s -H "Content-Type: application/json" \
  http://localhost:8081/v1/models/sklearn-iris-s3:predict \
  -d @./iris-input.json
```

The request uses the same V1 prediction API pattern as the previous episode. The important difference is where the model came from: this time, KServe retrieved it from the private MinIO bucket using the configured Secret and ServiceAccount.

## 9. Troubleshooting storage access

If the InferenceService does not become ready, inspect the pod and the storage-initializer logs.

List pods:

```bash
kubectl get pods -n kserve-test
```

Describe the affected pod:

```bash
kubectl describe pod <pod-name> -n kserve-test
```

Read the storage-initializer logs:

```bash
kubectl logs <pod-name> -n kserve-test -c storage-initializer
```

The storage-initializer logs are the most direct place to investigate model download and storage authentication errors.

Use this checklist:

| Resource or setting | What to verify |
|---|---|
| InferenceService | Does `serviceAccountName` match the ServiceAccount name? |
| ServiceAccount | Does it reference the `s3creds` Secret? |
| Secret | Are the endpoint annotation and both access-key values correct? |
| MinIO Service | Is the endpoint reachable at `minio.minio.svc.cluster.local:9000` from inside the cluster? |
| Model object | Does the `models` bucket contain `iris/model.joblib`? |
| Storage URI | Does it point to the correct bucket and prefix: `s3://models/iris/`? |

A generic download or connection error may not identify which part of the chain is incorrect. Check each link and use the storage-initializer logs to find the underlying error.

## 10. From local MinIO credentials to AWS IRSA

This episode uses static access keys stored in a Kubernetes Secret. KServe supports this pattern for S3-compatible storage, and it is useful for understanding the authentication flow.

For production workloads on Amazon EKS, the episode introduces **IAM Roles for Service Accounts (IRSA)** as the preferred direction:

- Associate an IAM role with the Kubernetes ServiceAccount.
- Define the S3 permissions on that IAM role.
- Let the workload obtain temporary AWS credentials through its ServiceAccount identity.
- Avoid storing long-lived AWS access keys in a Kubernetes Secret.

The episode will configure this approach on Amazon EKS later in the series.

## Key takeaways

- A model's `storageUri` identifies where KServe should retrieve its artifacts.
- The storage initializer downloads model files before the inference server loads them.
- MinIO provides a local S3-compatible environment for learning private model storage.
- KServe's private-storage access in this example depends on the Secret → ServiceAccount → InferenceService relationship.
- The endpoint used by a local upload script (`localhost:9000`) differs from the in-cluster endpoint used by KServe.
- Static credentials are suitable for this controlled demonstration, while production AWS deployments should use an identity-based approach such as IRSA.

## Episode resources

- [MinIO Deployment and Service](minio.yaml)
- [Model training and upload script](train_and_upload.py)
- [S3 credentials and endpoint Secret](s3-secret.yaml)
- [ServiceAccount](s3-sa.yaml)
- [KServe InferenceService](sklearn-iris-s3.yaml)
- [Sample inference input](iris-input.json)
- [Video 04 — Deploy your first model](../video-04-first-model-deployment/README.md)
- [KServe documentation](https://kserve.github.io/website/)
- [MinIO documentation](https://min.io/docs/)

**Next episode:** ServingRuntimes — how KServe selects the model server that loads and runs your model, and how to define your own.
