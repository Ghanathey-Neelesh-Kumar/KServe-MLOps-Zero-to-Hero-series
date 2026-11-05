# Step 2 — Install cert-manager

KServe uses webhooks to validate and configure resources. Kubernetes communicates with these webhooks over a secure TLS connection, which requires certificates.

**cert-manager** creates and renews those certificates.

## Add the Helm repository

```bash
helm repo add jetstack https://charts.jetstack.io
helm repo update
```

## Install cert-manager

The episode uses cert-manager **v1.17.0**:

```bash
helm install cert-manager jetstack/cert-manager \
  --namespace cert-manager --create-namespace \
  --version v1.17.0 \
  --set crds.enabled=true
```

## Wait for the pods to become ready

```bash
kubectl wait --for=condition=Ready pods --all -n cert-manager --timeout=120s
kubectl get pods -n cert-manager
```

The episode expects three pods:
- `cert-manager`
- `cert-manager-cainjector` (shown as cainjector)
- `cert-manager-webhook` (shown as webhook)

Do not proceed until the cert-manager pods are ready. The episode highlights this as a common source of later installation problems.

Documentation: https://cert-manager.io/docs/
