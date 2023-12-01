# Configuring Ingress in Kubernetes

**Objective:** Configure Ingress to handle HTTP traffic in Kubernetes.

**Real-world Scenario:** You have multiple services in Kubernetes and want to simplify access to these services through a single entry point.

**Example Code:**
```yaml
# ingress.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: sample-ingress
spec:
  rules:
    - host: your-ingress-hostname
      http:
        paths:
        - path: /
          pathType: Prefix
          backend:
            service:
              name: sample-app
              port:
                number: 3000
