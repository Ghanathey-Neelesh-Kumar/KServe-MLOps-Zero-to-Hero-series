# Video 01 — Introduction to KServe

These notes accompany the [Introduction to KServe](https://www.youtube.com/watch?v=o9Gkx0TgkK4) episode in the **MLOps Zero to Hero** series.

The purpose of this episode is to understand why KServe is useful, how it fits with Kubernetes, and the main concepts we will use in the hands-on episodes.

## 1. What is KServe?

KServe is an open-source platform for serving machine-learning models on Kubernetes.

It provides a high-level way to deploy and use models. Rather than manually creating and managing all the Kubernetes resources needed for model serving, we describe the model we want to serve. KServe then creates and manages the required serving resources.

KServe supports:
- Traditional machine-learning inference.
- Generative AI workloads.
- Kubernetes-native resources designed specifically for model serving.

## 2. Model serving without KServe

Without a model-serving platform such as KServe, we are responsible for assembling the serving infrastructure ourselves.

A typical workflow includes:

1. Start with the trained model.
2. Build an API around the model so applications can send prediction requests.
3. Package the API and model into a container.
4. Create Kubernetes Deployments and Services.
5. Configure scaling.
6. Expose the model to other applications and manage networking.

This approach provides control, but it also means more configuration and ongoing maintenance.

## 3. How KServe simplifies model serving

With KServe, we describe the serving requirements instead of manually creating every resource.

For a supported model format, the information can include:
- The model format.
- The location of the model artifact.
- The computing resources required.
- How the model should be served.

We provide this information through a Kubernetes resource called an **InferenceService**.

KServe then creates and manages the serving infrastructure required for the model. Depending on the configuration, this can include the model server, Deployment, Service, scaling configuration, and networking. It also provides an endpoint that applications can use to send inference requests.

**Key idea:** We can focus more on the model and less on manually assembling the Kubernetes resources around it.

## 4. KServe and Kubernetes

KServe does not replace Kubernetes. It runs on top of Kubernetes and uses Kubernetes to deploy and manage model-serving workloads.

| Kubernetes | KServe |
|---|---|
| Provides the container orchestration platform | Adds specialised model-serving capabilities |
| Manages Pods, Services, Deployments, networking and scaling | Provides concepts such as InferenceService, model runtimes and model-specific serving |
| Supplies the underlying infrastructure | Simplifies how models are deployed and served |

Kubernetes remains important when working with KServe. To use KServe effectively, you should understand Kubernetes resources, Deployments, networking, and scaling.

## 5. KServe deployment modes

The selected deployment mode affects the Kubernetes resources and autoscaling mechanism used to serve a model.

### Standard mode

- Uses regular Kubernetes resources.
- Can use the Kubernetes Horizontal Pod Autoscaler (HPA).
- Can scale the number of model replicas using metrics such as CPU utilisation.
- Does not normally scale the model down to zero.

### Knative mode

- Uses Knative Serving.
- Uses the Knative Pod Autoscaler to respond to incoming request traffic.
- With the appropriate configuration, can scale down to zero when there are no requests.

### KEDA

KEDA is an external Kubernetes autoscaling component. It can scale workloads using Kubernetes or external metrics. In KServe, it is used with Raw deployment mode and can support more advanced metrics-driven scaling scenarios.

**Remember:** KServe does not always mean Knative. The deployment mode determines which Kubernetes resources and autoscaling mechanisms are used.

## 6. Why KServe is useful in MLOps

KServe helps standardise how models are deployed and served. Instead of manually building similar serving infrastructure for every model, we can describe the model-serving requirements using KServe resources such as an InferenceService.

For example, earlier in this learning series we served a Customer Churn model manually:
- Built a FastAPI application.
- Created a Docker image.
- Deployed Kubernetes resources.

With KServe, the same trained model can be described using an InferenceService and its model storage location. Because the model is saved as a Joblib file and KServe supports Scikit-learn models, we can use the Scikit-learn serving runtime to load the model and create an inference endpoint, rather than building another custom FastAPI application from scratch.

## 7. Serving runtimes

A **serving runtime** is the model server that knows how to load a particular model format and handle prediction requests.

KServe can work with a range of model frameworks and serving technologies, including:
- Scikit-learn
- XGBoost
- TensorFlow
- LightGBM
- MLflow-packaged models
- Hugging Face models
- NVIDIA Triton for several deep-learning model formats

A runtime should match the format and requirements of the model.

### Custom serving runtimes

If the built-in runtimes do not meet our requirements, KServe also allows us to define a custom serving runtime.

A custom runtime may be useful when:
- We use our own model format.
- We need custom preprocessing or postprocessing.
- We have a specialised inference server.
- We require additional libraries or custom dependencies.

This gives us ready-made runtimes for common frameworks while retaining flexibility for specialised use cases.

## 8. Model storage

KServe can load model artifacts from different supported storage systems, including:
- Cloud object storage such as Amazon S3.
- Google Cloud Storage.
- Persistent volumes.
- Other supported model sources.

This separates the model artifact from the serving infrastructure: the artifact is stored in a supported location, and the serving platform loads it when the inference service starts.

## 9. Three concepts to understand next

Before installing and deploying a model, become familiar with these three core concepts:

1. **InferenceService** — describes the model we want to serve.
2. **ServingRuntime** — describes how a model is served.
3. **Model storage** — identifies where the model artifact is stored.

The next episode explains how these pieces work together to serve a model.

## Key takeaways

- KServe is an open-source model-serving platform that runs on Kubernetes.
- It simplifies model serving by managing the required serving resources from a high-level declaration.
- Kubernetes provides the underlying orchestration; KServe adds model-serving capabilities.
- Standard mode, Knative mode, and KEDA-based approaches have different scaling behaviour.
- Serving runtimes load model formats and handle inference requests.
- Model artifacts can be loaded from supported storage systems.
- InferenceService, ServingRuntime, and model storage are foundational concepts for the hands-on work.

## Continue learning

- **Previous context:** The Customer Churn model-serving workflow built manually with FastAPI, Docker, and Kubernetes.
- **Next episode:** [KServe Architecture — How an InferenceService Becomes a Running Model Endpoint](../video-02-kserve-architecture/README.md)
- **Official documentation:** [KServe](https://kserve.github.io/website/)
