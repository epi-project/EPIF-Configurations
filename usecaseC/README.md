# This is the third usecase
This describes use is to simulate the algorithm(ML) sharing use case with 2 clusters are connected and third clusters, as shown in the following figure.


![Implementation](https://github.com/epi-project/EPIF-Configurations/blob/main/usecaseC/download%20(3).png)


## Clusters' Requirements
- cluster 1: meduim resources with 1 master node (jk-01), and two worker nodes (jk-02 jk-05)
- cluster 2: small resources with 1 master node (jk-03), and one worker nodes (jk-04)
- cluster 3: large resources with 1 master node (lz-03), and three worker nodes

## Cluster 1 setup 
- There needs to be latency of 10 ms between 1 and 3, by running the following command on master node of the cluster 1
 ```shell
sudo tc qdisc add dev cilium_host root netem delay 10ms
```
- cluster 1: has cluster 1 and cluster 3 as contexts
 ```shell
CLUSTER1="cluster1-cntx"
CLUSTER3="cluster3-cntx"
```
## Cluster 2 setup 
- There needs to be latency of 20 ms between 2 and 3, by running the following command on master node of the cluster 2
 ```shell
sudo tc qdisc add dev cilium_host root netem delay 20ms
```
- cluster 2: has cluster 2 and cluster 3 as contexts
 ```shell
CLUSTER2="cluster1-cntx"
CLUSTER3="cluster3-cntx"
```
## Edit $HOME/.kube/config to add cluster 3 on both clusters 1 and 2 as in the config file
 ```shell
sudo kubectl config --kubeconfig=config set-context cluster3-cntx --cluster=cluster3 --user=cluster3-admin
```
 ```shell
kubectl config --kubeconfig=config use-context cluster3-cntx
sudo kubectl config get-contexts
export KUBECONFIG=~/.kube/config
```
## Client send rate
Copy/paste the client.py in the correct directory. The use case is a small load usecase with 100 kb/s send rate. 
