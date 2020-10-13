## Openshift-Secret-Manager

# What is it?

This is a pip modular app that would watch an openshift namespace and 
check the namespace secrets across the ones stored in a hashicorp vault
server, if there are any updates on the hashicorp vault secret, it will 
push those updates into the openshift project. 

# How to run
```
 a) git clone this project
 b) pip install -e .
 c) openshift-secret-manager --namespace <your openshift project>
```


