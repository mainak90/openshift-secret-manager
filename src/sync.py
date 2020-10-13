from src.hvclient import HvClient
from src.apiclient import ApiClient
from openshift.dynamic import DynamicClient
from src.actions import Actions
import os
import sys
import logging
import yaml
import base64

class Sync(object):
    def __init__(self, namespace):
        self.namespace = namespace

    def checkForSync(self):
        k8s_client = ApiClient.apiclient()
        dyn_client = DynamicClient(k8s_client)
        v1_resources = dyn_client.resources.get(api_version='v1', kind='Secret')
        try:
            resources_list = v1_resources.get(namespace=self.namespace)
            logging.info('Retrived list of secrets from project ' + self.namespace)
        except Exception as e:
            logging.error('Error encountered ' + str(e))
            sys.exit(1)
        secdict = []
        secact = []
        for resource in resources_list.items:
            secdict.append(resource.metadata.name)
        logging.info('Secret list is ' + str(secdict))
        for secret in secdict:
            try:
                fullyaml = v1_resources.get(name=secret, namespace=self.namespace)
                yaml_response = yaml.safe_load(str(fullyaml))
                yamldata = yaml_response['ResourceInstance[Secret]']['data']
                for key, value in yamldata.iteritems():
                    try:
                        val = Actions(key=key, mount_point='secret', secret_path=self.namespace + '/' + secret).fromVault()
                        encodedbytes = base64.b64encode(val.encode("utf-8"))
                        if encodedbytes and value == encodedbytes:
                            logging.info('The current value of the secret-key ' + key + ' in secret ' + secret  +  ' is unchanged, skipping this one...')
                        elif encodedbytes and value != encodedbytes:
                            fullyaml = yaml.safe_load(str(fullyaml))
                            fullyaml['ResourceInstance[Secret]']['data'][key] = encodedbytes
                            logging.info('Updating key-value for key ' + key + ' in secret ' + secret)
                            try:
                                print fullyaml['ResourceInstance[Secret]']
                                v1_resources.patch(body=fullyaml['ResourceInstance[Secret]'], namespace=self.namespace, name=secret)
                                logging.info('Secret ' + secret + ' updated with a new value in namespace ' + self.namespace)
                                secact.append(secret)
                                logging.info('Updating the list with secrets that has been modified')
                            except Exception as e:
                                logging.error('Error encountered ' + str(e))
                        else:
                            logging.error('The value for key ' + key + ' does not exist in Vault')
                            break
                    except Exception as e:
                        logging.error('Error getting/setting secret key ' + key + ' for secret ' + secret + ' from Hashicorp Vault. See ERROR: ' + str(e))
            except Exception as e:
                logging.error('Error encountered while getting secret ' + secret + ' Error: ' + str(e))
        return secact
