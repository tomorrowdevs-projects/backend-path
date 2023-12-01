# Horizontal Scaling in Kubernetes

**Objective:** Modify the application deployed in the fourth exercise to enable horizontal scaling.

**Real-world Scenario:** You want to learn how Kubernetes can handle horizontal scaling in response to workload changes.

**Example Code:**
```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: sample-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: sample-app
  template:
    metadata:
      labels:
        app: sample-app
    spec:
      containers:
        - name: sample-app
          # Container configuration
          ports:
            - containerPort: 3000
