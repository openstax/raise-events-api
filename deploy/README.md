# RAISE Events API deployment

## Overview

This application is deployed using Kubernetes. The deployment is automated via [CodePipeline](https://docs.aws.amazon.com/codepipeline). This directory includes all deployment related configuration files used for the application, with the exception of the AWS infrastructure resource definitions which live with the rest of the K12 IaC code. The subdirectories include:

* `buildspec/` - [CodeBuild](https://docs.aws.amazon.com/codebuild) buildspec files used in pipeline stages
* `chart/` - A Helm chart used to deploy to Kubernetes
* `k8s/` - Kubernetes configurations for deployed resources

The pipeline is configured to automatically update the staging environment when PRs are merged to `main`. An operator must manually approve the promotion to production.

## Deploying Redpanda Console

Currently we do not leave a longstanding instance of Redpanda Console running in our clusters. If a developer wants to deploy an instance to inspect a Kafka cluster, they can utilize the configuration files in the `k8s/` directory (staging or production):

1. Modify the YAML file with appropriate values for `KAFKA_BROKERS`
2. Deploy the pod and setup a port forward (note that the example below uses port 8081 to avoid conflicts with the use of port 8080 by the `docker-compose.yml` in this repo):

```bash
$ kubectl apply -f deploy/k8s/redpanda-po-{prod/staging}.yaml
$ kubectl port-forward redpanda 8081:8080
```

3. Navigate to `http://localhost:8081` to view the console
4. Cleanup after you're done:

```bash
$ kubectl delete -f deploy/k8s/redpanda-po-{prod/staging}.yaml
```

## References

* [Build specification reference for CodeBuild](https://docs.aws.amazon.com/codebuild/latest/userguide/build-spec-ref.html)
* [Kubernetes API](https://kubernetes.io/docs/reference/kubernetes-api/)
