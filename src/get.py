from kubernetes.client import ApiClient
from openshift.dynamic import DynamicClient
from typing import List, Any

from src.apiclient import ApiClient
import os
import logger
import logging

class Get(object):
    def __init__(self, resource_type, name=None, namespace=None, url=None):
        self.resource_type = resource_type
        self.name = name
        self.namespace = namespace
        self.url = url

    def getResourceNames(self):
        logger.setLevel()
        k8s_client = ApiClient().apiclient() # type: ApiClient
        dyn_client = DynamicClient(k8s_client)
        v1_resources = dyn_client.resources.get(api_version='v1', kind=self.resource_type)
        resource_list = v1_resources.get(namespace=self.namespace)
        resdict = []  # type: List[Any]
        for resource in resource_list.items:
            resdict.append(resource.metadata.name)
        return resdict

    @property
    def getPodNamesFromSelectors(self):
        logger.setLevel()
        k8s_client = ApiClient().apiclient() # type: ApiClient
        dyn_client = DynamicClient(k8s_client)
        v1_resources = dyn_client.resources.get(api_version='v1', kind='Pod')
        resource_list = v1_resources.get(namespace=self.namespace, label_selector='app=' + self.name)
        listitem = [] # type: List[Any]
        for resource in resource_list.items:
            listitem.append(resource.metadata.name)
        return listitem

    def getResourceName(self):
        logger.setLevel()
        k8s_client = ApiClient().apiclient() # type: ApiClient
        dyn_client = DynamicClient(k8s_client)
        v1_resources = dyn_client.resources.get(api_version='v1', kind=self.resource_type)
        resource = v1_resources.get(namespace=self.namespace, name=self.name)
        logging.info('Resource name is ' + resource.metadata.name)
        return resource.metadata.name

    def getResourceYaml(self):
        logger.setLevel()
        k8s_client = ApiClient().apiclient()  # type: ApiClient
        dyn_client = DynamicClient(k8s_client)
        v1_resources = dyn_client.resources.get(api_version='v1', kind=self.resource_type)
        resource = v1_resources.get(namespace=self.namespace, name=self.name)
        return resource





