# Step 5 — Verify the KServe installation

Run the following checks after completing the installation:

```bash
kubectl get nodes
kubectl get pods -A
kubectl get crd | grep -i serving
kubectl get gatewayclass
kubectl get gateway -A
```

## Ready to proceed when
- The Kubernetes node is `Ready`.
- cert-manager components are healthy.
- KServe controller components are ready.
- The gateway controller is ready.
- The expected GatewayClass and Gateway resources have been accepted and programmed, where applicable.

For a resource that is not ready, inspect its status and events:

```bash
kubectl describe <resource-type> <resource-name> -n <namespace>
kubectl get events -A --sort-by=.lastTimestamp
```

Resolve installation issues before moving on to model deployment.
