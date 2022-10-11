# EPIF-Configurations
This describes the automatic and adaptive framework configurations to place, assign, and chain BF services' instances.  This setup is running over kubernetes/Cilium network configurations.

## Requirements
- You need to have at least two functional clusters with at least 1 worker, 1 master node each
- The clusterIP blocks should not overlap across clusters
- Swapoff -a
- Firewall rules allow traffic across pods

##After cluster setups:
You can now choose to deploy the proxy service on any cluster and you can reconfigure the proxy to assign BF services to requests and chain services as follows:

$ sudo kubectl patch deployment proxy --namespace default --type='json' -p='[{"op": "replace", "path": "/spec/template/spec/containers/0/args", "value": ["-c", "socks6://<BF-IP:PORT"]}]'
