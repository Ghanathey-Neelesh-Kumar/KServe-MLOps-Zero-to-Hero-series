# Step 1 — Create a local kind cluster

kind runs Kubernetes clusters in Docker containers and is useful for local learning.

## Before starting
- Confirm Docker is running.
- Install kind and kubectl.
- Check that your machine has enough resources.

Use the kind configuration and create-cluster command demonstrated in the video. After creation, verify the cluster:

```bash
kind get clusters
kubectl cluster-info
kubectl get nodes
```

Wait for the node to reach `Ready` before continuing.

To remove the cluster when finished:

```bash
kind delete cluster
```

Documentation: https://kind.sigs.k8s.io/
