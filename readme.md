# Chaos Testing on a K3s (Kubernetes) Cluster

## What is chaos testing?

Chaos testing is the practice of deliberately injecting failures into a system to observe how it behaves under stress or partial outage. The goal is to identify weaknesses in the system and its recovery mechanisms — before real-world failures occur. Chaos testing helps surface hidden assumptions, brittle dependencies, and unmonitored failure modes.

<br>

## Key characteristics of chaos testing

### Controlled:
Failures are introduced in a known, observable way.

### Repeatable:
Scenarios can be replayed to verify fixes.

### Measured:
Metrics, logs, and alerts are used to assess system behaviour and overall impact.

### Incremental:
We can start with small faults, and then expans to compound failures.

<br>

## Examples of chaos experiments

### Pod failure:
In this case, we delete a pod mid-request. This is at the Kubernetes cluster level, caused as a result of some infrastructure problem. This tests the system's auto-healing property.

### Node unavailability:
A node is drained or shut down.

### Network delay/loss:
A time delay is injected, for example between the service writing data to a database (in this article we won't be dicussing this, since it requires sudo/root access on all the cluster nodes, which is something I'll do in a later series of articles.)

### Resource exhaustion:
A high CPU or memory load is simulated.

### Service crash:
This type of failure occurs inside the pod, and is application level. This type of failure tests the application's exception handling logic.

<br>

## Requirements to follow the guide

1. A working Kubernetes cluster with at least `3 nodes` (physical in my case, but can be virtual; I operate all my nodes in a headless manner.)
2. On the development machine, `kubectl` must be configured to access the Kubernetes cluster. I'm using a Windows machine as the development system, so `Git` is required to run the chaos testing scripts.
3. For this article, I've been using a set of microservices - a `gateway`, a `database writer` service, and an `user interface (UI)` service. There is no decoupling between the services, and they communicate with each other using `HTTP` (except the database connection.) The code and YAML files for them are uploaded in this repository.
4. To simulate the requests, I'm using `Locust`. The file is shared in this repository.
5. Since this is a Linux environment, the user needs to have knowledge of how to check CPU and memory usage, pod counts (all the basic Kubernetes commands,) and able to understand errors which they can troubleshoot.

<br>

## Brief introduction to auto scaling

In real world systems, application load is never constant - traffic spikes, sudden drops, and unpredictable behavior are common. Kubernetes handles this challenge by using the auto scaling property, which ensures applications scale up when there's a lot of requests, and scale down when the usage is idle. This optimizes both performance and resource costs.

Auto scaling in Kubernetes is driven by real time metrics such as CPU usage, memory consumption, or any other custom application metrics. When these metrics cross over the configured thresholds, Kubernetes adjusts the number of running pod replicas automatically. Our focus will be on one specific type of auto scaling, which is the `Horizontal Pod Autoscalar` (HPA.) The HPA scales the number of pod replicas depending on the CPU, memory, or custom metrics.

We used YAML files to run our application on the Kubernetes cluster. Along with this, we will create an additonal YAML file for HPA details. This contains the CPU or memory requests and limits for the deployment. Once this HPA policy is applied on the cluster, we can observe the auto scaling behavior based on load we would generate using Locust.

<br>

### How does it relate to chaos testing?



## Running different scenarios

## Conclusion

## Future work.