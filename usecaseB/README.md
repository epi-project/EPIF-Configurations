# This is the second usecase
This describes use is to simulate the streaming usecase with 3 isolated clusters, as shown in the following figure.


![Implementation](https://github.com/epi-project/EPIF-Configurations/blob/main/usecaseB/download%20(2).png)


## CLusters' Requirements
- cluster 1: meduim resources with 1 master node (jk-01), and two worker nodes (jk-02 jk-05)
- cluster 2: small resources with 1 master node (jk-03), and one worker nodes (jk-04)
- cluster 3: large resources with 1 master node (lz-03), and three worker nodes


## Edit $HOME/.kube/config to remove other clusters information as in the config file, and remove contexts if already there
 ```shell
sudo kubectl config get-contexts
sudo kubectl unset contexts.cluster2-cntx

export KUBECONFIG=~/.kube/config
```
## Client send rate
Copy/paste the client.py in the correct directory. The use case is a large load usecase with 1000 kb/s send rate. 
