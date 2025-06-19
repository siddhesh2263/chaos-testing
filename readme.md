# Chaos Testing on a K3s (Kubernetes) Cluster

## What is chaos testing?

Chaos testing is the practice of deliberately injecting failures into a system to observe how it behaves under stress or partial outage. The goal is to identify weaknesses in the system and its recovery mechanisms — before real-world failures occur. Chaos testing helps surface hidden assumptions, brittle dependencies, and unmonitored failure modes.

<br>

### Key characteristics of chaos testing:

Controlled:
* Failures are introduced in a known, observable way.

Repeatable:
* Scenarios can be replayed to verify fixes.

Measured:
* Metrics, logs, and alerts are used to assess system behaviour and overall impact.

Incremental:
* We can start with small faults, and then expans to compound failures.

<br>

### Examples of chaos experiments:

Pod failure:
* In this case, we delete a pod mid-request. This is at the Kubernetes cluster level, caused as a result of some infrastructure problem. This tests the system's auto-healing property.

Node unavailability:
* A node is drained or shut down.

Network delay/loss:
* A time delay is injected, for example between the service writing data to a database. 

Resource exhaustion:
* A high CPU or memory load is simulated.

Service crash:
* This type of failure occurs inside the pod, and is application level. This type of failure tests the application's exception handling logic.

<br>

## Requirements to follow the guide

## Brief introduction to auto scaling

## Running different scenarios

## Conclusion

## Future work.