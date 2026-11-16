# 🚀 KServe – MLOps Zero to Hero

A practical, beginner-friendly journey into **KServe and Kubernetes-based Machine Learning Model Serving**.

This repository accompanies my KServe YouTube tutorial series, where we explore KServe from its fundamentals and architecture to installation, model deployment, private model storage, and model serving.

The goal is to help beginners understand how modern ML models are deployed, served and managed using Kubernetes and KServe through practical demonstrations.

## 📚 Tutorial Series

| Video | Topic | Resources |
|---|---|---|
| 01 | Introduction to KServe | [Notes and resources](video-01-introduction/README.md) · [YouTube](https://www.youtube.com/watch?v=o9Gkx0TgkK4&t=160s) |
| 02 | KServe Architecture – How InferenceService Becomes a Running Model Endpoint | [Notes and resources](video-02-kserve-architecture/README.md) · [YouTube](https://www.youtube.com/watch?v=n4MHfPbcGEs&t=1s) |
| 03 | Installing KServe Locally on Kubernetes | [Notes and installation files](video-03-kserve-installation/README.md) |
| 04 | Deploying Your First ML Model Using KServe | [Notes, InferenceService YAML and sample input](video-04-first-model-deployment/README.md) |
| 05 | Deploy ML Models from Private S3 Storage with KServe and MinIO | [Notes, MinIO manifests, upload script and KServe YAML](video-05-private-model-storage-s3-minio/README.md) |

YouTube links for Episodes 3–5 will be added after publication.

## 🛠️ Technology Stack

- KServe
- Kubernetes
- kind
- Docker
- cert-manager
- Envoy Gateway
- MinIO and S3-compatible object storage
- Python, Boto3 and Scikit-learn
- Machine Learning and MLOps

## 🎯 Learning Objectives

By following this repository, you will learn how to:

- Understand KServe and its role in MLOps.
- Explore the KServe architecture.
- Install KServe on a local Kubernetes cluster.
- Understand and configure InferenceService resources.
- Deploy machine learning models and test inference endpoints.
- Understand how KServe retrieves model artifacts from object storage.
- Configure private S3-compatible model access using Kubernetes Secrets and ServiceAccounts.
- Use MinIO locally to practise S3 model storage without an AWS account.
- Explore model serving runtimes and scalable model serving on Kubernetes.

## 🏗️ Repository Structure

Each video has its own directory containing the relevant configurations, code, manifests and audience reference notes.

```text
video-01-introduction/
video-02-kserve-architecture/
video-03-kserve-installation/
video-04-first-model-deployment/
video-05-private-model-storage-s3-minio/
resources/
```

## 🚀 Getting Started

Start with Video 1 and follow the tutorials sequentially.

Each video directory contains its own README with prerequisites, explanations, commands, configuration files and implementation details. Use the files and instructions from the corresponding episode directory.

**Security note:** Some local demonstration manifests use sample credentials to make the MinIO walkthrough reproducible. They are for local learning only. Never commit real access keys or reuse demonstration credentials in production.

## 📖 Official Documentation

- KServe: https://kserve.github.io/website/
- Kubernetes: https://kubernetes.io/docs/
- kind: https://kind.sigs.k8s.io/
- cert-manager: https://cert-manager.io/
- MinIO: https://min.io/docs/

## 👨‍💻 Author

**Neelesh Ghanathey**

This repository is part of my *MLOps Zero to Hero* educational initiative.

If you find this repository useful, please ⭐ Star the repository and subscribe to the YouTube channel for upcoming tutorials.

Happy Learning! 🚀
