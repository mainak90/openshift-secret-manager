import yaml
import logger
import logging
from openshift.dynamic import DynamicClient
import sys
from src.apiclient import ApiClient

class Delete(object):
    def __init__(self, resource_type, namespace, name=None, url=None):
        self.resource_type = resource_type
        self.namespace = namespace
        self.name = name
        self.url = url

    def deleteResource(self):
        k8s_client = ApiClient.apiclient()
        dyn_client = DynamicClient(k8s_client)
        logging.info('Requested to delete resource ' + self.name + ' via API version v1')
        try:
            v1_resources = dyn_client.resources.get(api_version='v1', kind=self.resource_type)
            v1_resources.delete(namespace=self.namespace, name=self.name)
            logging.info('Deleted resource ' + self.resource_type + ' ' + self.name)
        except Exception as ex:
            logging.error(str(ex))
            sys.exc_clear()

    def deleteResourceType(self):
        k8s_client = ApiClient.apiclient()
        dyn_client = DynamicClient(k8s_client)
        v1_resources = dyn_client.resources.get(api_version='v1', kind=self.resource_type)
        logging.info('Requested to delete resources of type ' + self.resource_type)
        try:
            v1_resources.delete(namespace=self.namespace, field_selector='metadata.namespace=' + self.namespace)
            logging.info('Deleted all resources of type ' + self.resource_type)
        except Exception as ex:
            logging.error(str(ex))
            sys.exc_clear()


