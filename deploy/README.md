# RAISE Events API deployment

## Overview

This application is deployed using Kubernetes. The deployment is automated via [CodePipeline](https://docs.aws.amazon.com/codepipeline). This directory includes all deployment related configuration files used for the application, with the exception of the AWS infrastructure resource definitions which live with the rest of the K12 IaC code. The subdirectories include:

* `buildspec/` - [CodeBuild](https://docs.aws.amazon.com/codebuild) buildspec files used in pipeline stages
* `chart/` - A Helm chart used to deploy to Kubernetes

The pipeline is configured to automatically updating the staging environment when PRs are merged to `main`. An operator must manually approve the promotion to production.

## References

* [Build specification reference for CodeBuild](https://docs.aws.amazon.com/codebuild/latest/userguide/build-spec-ref.html)
* [Kubernetes API](https://kubernetes.io/docs/reference/kubernetes-api/)
