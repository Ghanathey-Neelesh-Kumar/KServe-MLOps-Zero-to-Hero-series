# Step 2 — Install cert-manager

cert-manager automates certificate management in Kubernetes and is part of the installation sequence used in this walkthrough.

First confirm the cluster is healthy:

```bash
kubectl get nodes
```

Install the release and manifests demonstrated in the video. Check the official documentation for compatibility with your Kubernetes version.

Verify the components:

```bash
kubectl get pods -n cert-manager
```

Wait until the cert-manager pods are ready before installing KServe.

Documentation: https://cert-manager.io/docs/installation/
