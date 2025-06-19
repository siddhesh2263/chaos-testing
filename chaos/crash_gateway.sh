#!/bin/bash
echo "[*] Injecting crash into Gateway deployment..."
kubectl patch deployment gateway -n default --patch '{
  "spec": {
    "template": {
      "spec": {
        "containers": [{
          "name": "gateway",
          "command": ["sh", "-c", "exit 1"]
        }]
      }
    }
  }
}'

sleep 15
kubectl get pods -l app=gateway