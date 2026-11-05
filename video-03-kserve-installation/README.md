# Video 03 — Installing KServe Locally with kind

These notes accompany the local installation episode in the **KServe MLOps Zero to Hero** series.

By following this walkthrough, you will install KServe on your laptop using a local Kubernetes cluster. No cloud account is required.

## Installation mode selected

KServe can run in different modes. The mode affects the Kubernetes resources and dependencies required.

| Mode | What it uses | Main characteristic |
|---|---|---|
| Standard mode | Regular Kubernetes resources such as Deployment, Service and HPA | Lighter installation; conventional Kubernetes autoscaling |
| Knative mode (Serverless) | Knative Serving | Request-based autoscaling and scale-to-zero; installation is heavier |

The episode also mentions **LLMInferenceService**, a path designed for large language models that will be explored in a later video.

For this series, we use **Standard mode** because it is lighter and simpler. The InferenceService concept remains relevant in both Standard and Knative modes.

## Prerequisites

Install the following tools before starting:

- Docker
- kind
- kubectl
- Helm

Check that they are available:

```bash
docker --version
kind --version
kubectl version --client
helm version
```

Installation links and other resources are available in the repository's [useful links](../../resources/useful-links.md).

## Installation sequence

KServe is installed in the following stages:

1. Create a local kind cluster.
2. Install cert-manager.
3. Install KServe Custom Resource Definitions (CRDs).
4. Install the KServe controller in Standard mode.
5. Install the KServe runtime configurations.
6. Verify the controller, CRDs, and runtimes.

Detailed commands for each stage are provided below.

## 1. Create the cluster

Create a single-node cluster:

```bash
kind create cluster --name kserve-demo
kubectl cluster-info --context kind-kserve-demo
kubectl get nodes
```

Confirm that the node reaches the `Ready` state. Check the Kubernetes version as well, and ensure it meets the requirements of the KServe release being installed:

```bash
kubectl version
```

## 2. Install cert-manager

KServe uses webhooks to validate and configure resources. Kubernetes communicates with these webhooks over a secure TLS connection, which requires certificates. cert-manager creates and renews those certificates.

The episode uses cert-manager **v1.17.0**:

```bash
helm repo add jetstack https://charts.jetstack.io
helm repo update

helm install cert-manager jetstack/cert-manager \
  --namespace cert-manager --create-namespace \
  --version v1.17.0 \
  --set crds.enabled=true
```

Wait for all cert-manager pods to become ready:

```bash
kubectl wait --for=condition=Ready pods --all -n cert-manager --timeout=120s
kubectl get pods -n cert-manager
```

The episode expects to see three pods: `cert-manager`, `cainjector`, and `webhook`.

**Do not continue until these pods are ready.** An unready cert-manager installation is a common cause of later installation failures.

## 3. Install KServe

The episode installs KServe in three parts:

1. **CRDs:** Add KServe resource types to Kubernetes, such as InferenceService, ServingRuntime, ClusterServingRuntime, and InferenceGraph.
2. **Controller:** Watches KServe resources and creates the Kubernetes resources required to run them.
3. **Runtimes:** Tell KServe how to serve different model types.

Set the KServe version once so that all installation commands use the same version:

```bash
export KSERVE_VERSION=v0.18.0
```

### Part 1 — Install the CRDs

```bash
helm install kserve-crd oci://ghcr.io/kserve/charts/kserve-crd \
  --version ${KSERVE_VERSION} \
  --namespace kserve \
  --create-namespace
```

### Part 2 — Install the controller

```bash
helm install kserve oci://ghcr.io/kserve/charts/kserve-resources \
  --version ${KSERVE_VERSION} \
  --namespace kserve \
  --set kserve.controller.deploymentMode=Standard \
  --set kserve.controller.gateway.disableIngressCreation=true
```

Two settings are important:

- `deploymentMode=Standard` selects Standard mode. The episode notes that the chart's default is Knative; without this setting, the controller would wait for Knative to exist.
- `disableIngressCreation=true` tells KServe not to create ingress resources. The episode explains that KServe recommends the Kubernetes Gateway API for networking, but a gateway controller is needed. For this installation walkthrough, the model will initially be accessed using `kubectl port-forward`.

### Part 3 — Install runtime configurations

A runtime is the model server that knows how to load a model format and handle inference requests.

Install the runtime configurations:

```bash
helm install kserve-runtime-configs oci://ghcr.io/kserve/charts/kserve-runtime-configs \
  --version ${KSERVE_VERSION} \
  --namespace kserve \
  --set kserve.servingruntime.enabled=true
```

## 4. Verify the installation

The episode uses three checks.

### Check 1 — Controller

```bash
kubectl get pods -n kserve
kubectl logs -n kserve deployment/kserve-controller-manager --tail=20
```

Wait until the controller pod is Running and all its containers are ready.

### Check 2 — CRDs

```bash
kubectl get crd | grep serving.kserve.io
```

The episode introduces these KServe resources:

| Resource | Purpose described in the episode |
|---|---|
| InferenceService | Main resource describing a model to serve |
| ServingRuntime | Describes how a model is served within a namespace |
| ClusterServingRuntime | Describes a runtime available across the cluster |
| InferenceGraph | Connects multiple models into a pipeline |
| TrainedModel | Used for multi-model serving |
| LocalModelCache | A newer resource that may appear depending on the version |
| LLMInferenceService | A newer resource that may appear depending on the version |

The exact CRDs visible depend on the installed version.

### Check 3 — Available runtimes

```bash
kubectl get clusterservingruntimes
```

You should see built-in runtimes such as Scikit-learn and XGBoost. The word **Cluster** means these runtimes are available across namespaces.

If all three checks pass, KServe is installed and the cluster is ready for the first model deployment.

## Troubleshooting

### Webhook or x509 certificate errors

The episode identifies cert-manager readiness as the first thing to check. Confirm that its pods are healthy:

```bash
kubectl get pods -n cert-manager
```

Wait for them to become ready. The episode suggests reinstalling KServe after cert-manager is ready if the installation was attempted too early.

### Pods stuck in Pending or ImagePullBackOff

First check Docker's CPU and memory settings. Then inspect the affected pod:

```bash
kubectl describe pod <pod-name> -n kserve
```

The pod description and events are the first places to investigate.

For more general guidance, see the repository's [troubleshooting notes](../../resources/troubleshooting.md).

## Clean up

When you have finished experimenting, delete the local cluster:

```bash
kind delete cluster --name kserve-demo
```

## Recap

In this episode, we:
- Chose Standard mode rather than Knative mode.
- Created a local kind cluster.
- Installed cert-manager.
- Installed KServe in three parts: CRDs, controller, and runtime configurations.
- Verified the controller, CRDs, and available runtimes.

## Next episode

In the next video, we will deploy our first InferenceService using a Scikit-learn model, call it through the API, and explore the inference protocol used by KServe.
