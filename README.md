# EPIF-Configurations
This describes the automatic and adaptive framework configurations to place, assign, and chain BF services' instances.

## Requirements
- You need to have at least two functional clusters with at least 1 worker, 1 master node each
- The clusterIP blocks should not overlap across clusters
- Swapoff -a
- Firewall rules allow traffic across pods
