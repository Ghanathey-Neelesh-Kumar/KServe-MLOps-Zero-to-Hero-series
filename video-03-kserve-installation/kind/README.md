# Step 1 — Create a local kind cluster

The episode uses **kind** to create a single-node Kubernetes cluster locally. kind runs Kubernetes clusters using Docker containers.

## Prerequisites

Make sure Docker, kind, and kubectl are installed.

Check the tools:

```bash
docker --version
kind --version
kubectl version --client
```

## Create the cluster

```bash
kind create cluster --name kserve-demo
```

Check the cluster context and node:

```bash
kubectl cluster-info --context kind-kserve-demo
kubectl get nodes
```

The node should reach the `Ready` state.

## Check the Kubernetes version

KServe requires a compatible, sufficiently recent Kubernetes version. Check the version of the cluster:

```bash
kubectl version
```

Confirm compatibility with the KServe release you intend to install.

## Delete the cluster

When you have finished experimenting:

```bash
kind delete cluster --name kserve-demo
```

Documentation: https://kind.sigs.k8s.io/
