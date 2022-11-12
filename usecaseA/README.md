# This is the First usecase
This describes use is to simulate the EHR use case with 2 clusters are connected and one isolated, as shown in the following figure.


![Implementation](https://github.com/epi-project/EPIF-Configurations/blob/main/usecaseA/download%20(1).png)


## CLusters' Requirements
- cluster 1: meduim resources with 1 master node (jk-01), and two worker nodes (jk-02 jk-05)
- cluster 2: small resources with 1 master node (jk-03), and one worker nodes (jk-04)
- cluster 3: large resources with 1 master node (lz-03), and three worker nodes

## CLuster 1 setup 
- There needs to be latency of 10 ms between 1 and 2, by running the following command on master node of the cluster 1
 ```shell
sudo tc qdisc add dev cilium_host root netem delay 10ms
```
- cluster 1 

