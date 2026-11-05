# Video 03 — Install KServe Locally (Standard Mode)

This guide accompanies the local installation walkthrough. The objective is to run KServe on a local Kubernetes cluster without requiring a cloud account.

## Installation sequence
1. Create a local Kubernetes cluster with kind.
2. Install cert-manager.
3. Install KServe in Standard mode.
4. Install and configure Envoy Gateway.
5. Verify the installation.

## Prerequisites
- Docker installed and running
- kind and kubectl installed
- A terminal with permission to run the commands
- Sufficient CPU, memory, and disk space for a local cluster

## Step-by-step guides
- [Create the kind cluster](kind/README.md)
- [Install cert-manager](cert-manager/README.md)
- [Install KServe](kserve/README.md)
- [Install Envoy Gateway](gateway/README.md)
- [Verify the installation](verification/README.md)

**Important:** This series uses KServe Standard mode (called RawDeployment in some older documentation). Check version compatibility and use the release-specific commands shown in the video. Do not mix manifests from different releases.
