# Troubleshooting

## Check cluster health

```bash
kubectl get nodes
kubectl get pods -A
kubectl get events -A --sort-by=.lastTimestamp
```

## Pod is Pending

```bash
kubectl describe pod <pod-name> -n <namespace>
```

Review scheduling events, available node resources, image availability, and storage requirements.

## Pod is not Ready

```bash
kubectl describe pod <pod-name> -n <namespace>
kubectl logs <pod-name> -n <namespace>
```

For multi-container pods, add `-c <container-name>`.

## GatewayClass is missing

Check that the gateway controller pods are ready and that the Gateway API resources required by the selected release are installed:

```bash
kubectl get pods -A
kubectl get gatewayclass
```

## InferenceService is not ready

```bash
kubectl get inferenceservice -A
kubectl describe inferenceservice <name> -n <namespace>
kubectl get pods -n <namespace>
```

Inspect the InferenceService conditions, model storage configuration, serving runtime, and pod events.

Never share credentials, tokens, private keys, or sensitive cluster configuration when posting logs.
