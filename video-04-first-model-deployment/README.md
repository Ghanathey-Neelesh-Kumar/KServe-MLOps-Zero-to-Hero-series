# Video 04 — Deploy Your First Model with KServe

**YouTube:** *To be added after publication.*

In this episode, we deploy a pre-trained Scikit-learn Iris model using a KServe `InferenceService`, check that it becomes ready, and send a prediction request with `curl`.

## What you will learn

- What an `InferenceService` represents and what KServe manages for you.
- How to specify a model format, model storage URI, and CPU/memory requests and limits.
- How to check the deployment and its Kubernetes resources.
- How to reach the predictor locally with port-forwarding.
- How to submit an inference request using the V1 prediction endpoint.
- The difference between the V1 and V2 inference request paths.

## Prerequisites

- A Kubernetes cluster with KServe installed, following [Video 03 — KServe installation](../video-03-kserve-installation/README.md).
- `kubectl` configured to access that cluster.
- A terminal with `curl`.

This walkthrough uses the Standard-mode setup and manifest shown in the episode.

## 1. What is an InferenceService?

An `InferenceService` is KServe's Kubernetes custom resource for defining how a model should be served. You describe the model format, where its files are stored, and the resources it needs. KServe then reconciles the required Kubernetes resources and brings up the model-serving workload.

For this episode, the model is a pre-trained Scikit-learn model stored in a public Google Cloud Storage bucket. We are deploying and calling the model; model training is not part of this episode.

## 2. The Iris model

The Iris dataset contains 150 flower observations across three species:

- Iris Setosa
- Iris Versicolor
- Iris Virginica

Each observation contains four measurements, in this order:

1. Sepal length
2. Sepal width
3. Petal length
4. Petal width

For example, `5.1, 3.5, 1.4, 0.2` represents one flower's four input measurements. The model uses these values to predict the flower class.

## 3. Review the InferenceService manifest

Manifest: [`sklearn-iris.yaml`](sklearn-iris.yaml)

The manifest defines:

| Field | Purpose |
|---|---|
| `apiVersion` | KServe API version used by this example: `serving.kserve.io/v1beta1`. |
| `kind` | Declares this resource as an `InferenceService`. |
| `metadata.name` | Names the service `sklearn-iris`. |
| `metadata.namespace` | Deploys it into `kserve-test`. |
| `spec.predictor.model.modelFormat.name` | Identifies the model format as `sklearn`. |
| `storageUri` | Points to the model files in the public GCS bucket. |
| `resources.requests` | Requests 100m CPU and 512Mi memory. |
| `resources.limits` | Sets limits of 1 CPU and 1Gi memory. |

The model location used in this episode is:

`gs://kfserving-examples/models/sklearn/1.0/model`

## 4. Create the namespace and deploy

Create a dedicated namespace:

```bash
kubectl create namespace kserve-test
```

Apply the InferenceService manifest from this directory:

```bash
kubectl apply -f sklearn-iris.yaml
```

Check its status:

```bash
kubectl get isvc sklearn-iris -n kserve-test
```

Wait until the `READY` column reports `True`. The episode notes that this can take approximately 1–2 minutes.

Check the pods:

```bash
kubectl get pods -n kserve-test
```

KServe's model initialization process retrieves the model files, after which the model server loads the model. Allow time for this process to complete.

## 5. Inspect the resources created by KServe

Run:

```bash
kubectl get deployment,svc,hpa,pods -n kserve-test
```

In this Standard-mode example, KServe manages the Kubernetes resources needed to serve the model, including a Deployment, Service, HPA, and Pod. The `InferenceService` is the resource you declare; KServe reconciles the underlying resources to match its desired configuration.

You can also list the Services:

```bash
kubectl get svc -n kserve-test
```

The predictor Service used in this walkthrough is `sklearn-iris-predictor`.

## 6. Prepare the prediction input

Sample request: [`iris-input.json`](iris-input.json)

The file contains two Iris observations. Each row follows the feature order described above:

```json
{
  "instances": [
    [6.8, 2.8, 4.8, 1.4],
    [6.0, 3.4, 4.5, 1.6]
  ]
}
```

The V1 request body uses the `instances` field to provide the input rows.

## 7. Forward the predictor Service to your machine

Run this command:

```bash
kubectl port-forward -n kserve-test svc/sklearn-iris-predictor 8080:80
```

Keep this terminal running while you send the request. Port-forwarding makes the Service reachable locally at `localhost:8080`.

## 8. Send a prediction request with curl

Open another terminal in this directory and run:

```bash
curl -s -H "Content-Type: application/json" \
  http://localhost:8080/v1/models/sklearn-iris:predict \
  -d @./iris-input.json
```

Expected response shown in the episode:

```json
{"predictions": [1, 1]}
```

Both observations are predicted as class `1`, which corresponds to Iris Versicolor in this example.

## 9. V1 and V2 inference paths

The episode introduces two inference request conventions:

| Protocol | Request path |
|---|---|
| V1 | `/v1/models/sklearn-iris:predict` |
| V2 (Open Inference Protocol) | `/v2/models/sklearn-iris/infer` |

The V1 example in this walkthrough sends an `instances` array and receives a `predictions` array. The V2 Open Inference Protocol provides a standard interface intended to improve compatibility across model-serving tools. This episode's demonstrated curl command uses V1.

## Key takeaways

- You can describe a model-serving deployment declaratively with an `InferenceService`.
- The manifest specifies the model format, storage location, and resource requirements.
- KServe manages the Kubernetes resources that implement the serving workload.
- Once the predictor is ready, you can reach it locally with port-forwarding and submit a JSON prediction request.

## Episode resources

- [InferenceService manifest](sklearn-iris.yaml)
- [Sample inference input](iris-input.json)
- [Video 03 — KServe installation notes](../video-03-kserve-installation/README.md)
- [KServe documentation](https://kserve.github.io/website/)
- [KServe GitHub repository](https://github.com/kserve/kserve)

**Next episode:** The series will move on to model storage options, including S3 and the permissions needed for model access.
