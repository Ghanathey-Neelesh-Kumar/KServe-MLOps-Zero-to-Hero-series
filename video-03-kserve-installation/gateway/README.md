# Step 4 — Install and configure Envoy Gateway

Envoy Gateway provides the gateway layer used in this local walkthrough to expose the inference service.

## Verify the controller

```bash
kubectl get pods -A
kubectl get gatewayclass
kubectl get gateway -A
```

Confirm the Envoy Gateway controller is ready, then apply the Gateway configuration demonstrated in the video.

If GatewayClass is missing, check that the controller installed successfully, inspect its logs, and confirm that the required Gateway API resources are present.

Documentation: https://gateway.envoyproxy.io/
