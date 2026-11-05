# Step 3 — Install KServe in Standard mode

The episode installs KServe in three parts: **CRDs, controller, and runtime configurations**.

The commands below use KServe **v0.18.0**, as shown in the episode script.

## Set the KServe version

```bash
export KSERVE_VERSION=v0.18.0
```

## Part 1 — Install the Custom Resource Definitions

CRDs add KServe-specific resource types to Kubernetes, including InferenceService, ServingRuntime, ClusterServingRuntime, and InferenceGraph.

```bash
helm install kserve-crd oci://ghcr.io/kserve/charts/kserve-crd \
  --version ${KSERVE_VERSION} \
  --namespace kserve \
  --create-namespace
```

## Part 2 — Install the KServe controller

The controller watches KServe resources, such as an InferenceService, and creates the Kubernetes resources required to run them.

```bash
helm install kserve oci://ghcr.io/kserve/charts/kserve-resources \
  --version ${KSERVE_VERSION} \
  --namespace kserve \
  --set kserve.controller.deploymentMode=Standard \
  --set kserve.controller.gateway.disableIngressCreation=true
```

### Understand the two settings

- `deploymentMode=Standard`: selects Standard mode. The episode notes that the chart defaults to Knative, so this setting prevents the controller from waiting for Knative to be installed.
- `disableIngressCreation=true`: disables KServe ingress resource creation for this setup. The episode explains that Gateway API networking will be covered separately; for now, access to the model will use `kubectl port-forward`.

## Part 3 — Install runtime configurations

A runtime is the model server that knows how to load a particular model format and process prediction requests.

```bash
helm install kserve-runtime-configs oci://ghcr.io/kserve/charts/kserve-runtime-configs \
  --version ${KSERVE_VERSION} \
  --namespace kserve \
  --set kserve.servingruntime.enabled=true
```

## Next: verify the installation

Continue to the [installation verification checklist](../verification/README.md).

**Version note:** These commands reproduce the versions and settings in the episode script. Check the matching KServe release documentation before adapting them to a different version.

Documentation: https://kserve.github.io/website/
