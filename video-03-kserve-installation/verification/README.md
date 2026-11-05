# Step 4 — Verify the KServe installation

The episode verifies three things: the KServe controller, the installed CRDs, and the available serving runtimes.

## Check 1 — Controller is running

```bash
kubectl get pods -n kserve
kubectl logs -n kserve deployment/kserve-controller-manager --tail=20
```

Wait until the controller pod is Running and all its containers are ready.

## Check 2 — KServe CRDs are installed

```bash
kubectl get crd | grep serving.kserve.io
```

The episode introduces the following resources:

| Resource | Purpose |
|---|---|
| InferenceService | Describes the model you want to serve |
| ServingRuntime | Describes how a model is served within a namespace |
| ClusterServingRuntime | Describes a runtime available across the cluster |
| InferenceGraph | Connects multiple models into a pipeline |
| TrainedModel | Used for multi-model serving |
| LocalModelCache | May appear in newer versions |
| LLMInferenceService | May appear in newer versions |

The exact resources returned depend on the KServe version installed.

## Check 3 — Runtimes are available

```bash
kubectl get clusterservingruntimes
```

Look for built-in runtimes such as Scikit-learn and XGBoost.

The word **Cluster** indicates that these runtimes are available across namespaces, rather than being limited to one namespace.

## Installation complete

If the controller is ready, the expected CRDs are installed, and the runtime resources are available, the cluster is ready for the first model deployment.

The next episode will create an InferenceService for a Scikit-learn model and send an inference request.
