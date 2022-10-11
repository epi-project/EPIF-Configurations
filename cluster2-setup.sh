#!/bin/bash

CLUSTER1="cluster1-cntx"
CLUSTER2="cluster2-cntx"


####### This section must be run only on the Master node#########################################################################################

#Initialize the cluster
sudo kubeadm init 

mkdir -p $HOME/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config
#*******************************************************************************************************************************************************

#************************************************************Join worker nodes***************************************************************************

#sudo kubeadm join
  
#******************************************************************************************************************************************************

#******************************************************************Install Cilium**********************************************************************
#Downlad cilium CLI
curl -L --remote-name-all https://github.com/cilium/cilium-cli/releases/latest/download/cilium-linux-amd64.tar.gz{,.sha256sum}
sha256sum --check cilium-linux-amd64.tar.gz.sha256sum
sudo tar xzvfC cilium-linux-amd64.tar.gz /usr/local/bin
rm cilium-linux-amd64.tar.gz{,.sha256sum}

#*******************************************************************************************************************************************************

#*********************************************************Add cluster contexts**********************************************************

# Edit $HOME/.kube/config to add both clusters information as in the example config file
sudo kubectl config --kubeconfig=config set-context cluster2-cntx --cluster=cluster2 --user=cluster2-admin
#To switch cluster context
kubectl config --kubeconfig=config use-context cluster2-cntx
sudo kubectl config get-contexts
export KUBECONFIG=~/.kube/config

cilium install   --cluster-id=2 --cluster-name="cluster2"  --inherit-ca $CLUSTER1
    #cilium uninstall

#****************************************************************Verify Cluster Installation and install "Hubble"******************************************
#Veriy thal all PODS and nodes are ready. You may need to reboot if things are not healthy after a few minutes.
kubectl -n kube-system get pods -l k8s-app=cilium -o wide
kubectl get pods -n kube-system -o wide
kubectl get nodes -o wide

cilium status --wait


#***************************************************Setup Hubble******************************************************************
#Enabling Hubble requires the TCP port 4245 to be open on all nodes running Cilium. This is required for Relay to operate correctly.
cilium hubble enable

cilium status

#In order to access the observability data collected by Hubble, install the Hubble CL
export HUBBLE_VERSION=$(curl -s https://raw.githubusercontent.com/cilium/hubble/master/stable.txt)
curl -L --remote-name-all https://github.com/cilium/hubble/releases/download/$HUBBLE_VERSION/hubble-linux-amd64.tar.gz{,.sha256sum}
sha256sum --check hubble-linux-amd64.tar.gz.sha256sum
sudo tar xzvfC hubble-linux-amd64.tar.gz /usr/local/bin
rm hubble-linux-amd64.tar.gz{,.sha256sum}

#In order to access the Hubble API, create a port forward to the Hubble service from your local machine
cilium hubble port-forward&

hubble status 

hubble observe

