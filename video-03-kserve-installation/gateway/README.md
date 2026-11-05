# Gateway and networking in this installation

This episode deliberately keeps the initial installation focused on KServe Standard mode. It sets:

```bash
--set kserve.controller.gateway.disableIngressCreation=true
```

This tells KServe not to create ingress resources as part of this setup.

The episode explains that KServe recommends the Kubernetes Gateway API for networking, but using it requires a gateway controller. Gateway networking will be covered in later networking-focused videos.

For the current installation walkthrough, the plan is to access the model using `kubectl port-forward`.

This folder is reserved for the gateway configuration and practical steps when that part of the series is covered. Do not install an additional gateway solely on the basis of this episode's script.
