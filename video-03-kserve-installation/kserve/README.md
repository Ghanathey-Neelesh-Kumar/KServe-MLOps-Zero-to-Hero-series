# Step 3 — Install KServe in Standard mode

This series installs KServe in **Standard mode** on the local kind cluster.

## Before installation
- Confirm the kind cluster is healthy.
- Confirm cert-manager is installed and ready.
- Check the KServe release notes for Kubernetes compatibility.

Run the installation commands from the video using the same pinned release. Avoid combining manifests from different KServe versions.

## Verify

```bash
kubectl get pods -A
kubectl get crd | grep -i serving
```

The KServe controller and required components should become ready. Namespaces and resource names may vary by release.

Documentation: https://kserve.github.io/website/
