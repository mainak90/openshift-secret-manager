from kubernetes import client, config
import os
import logging

class ApiClient(object):
    def apiclient(self):

        homedir = os.path.expanduser("˜")

        if os.path.exists('/var/run/secrets/kubernetes.io/serviceaccount/token'):
            with open('/var/run/secrets/kubernetes.io/serviceaccount/token') as tokenfile:
                token = tokenfile.read()
            aConfiguration = client.Configuration()
            aConfiguration.host = "https://kubernetes.default.svc"
            if os.path.exists('/var/run/secrets/kubernetes.io/serviceaccount/ca.crt'):
                aConfiguration.verify_ssl = True
                aConfiguration.ssl_ca_cert = '/var/run/secrets/kubernetes.io/serviceaccount/ca.crt'
            else:
                aConfiguration.verify_ssl = False

            aConfiguration.api_key = {"authorization": "Bearer " + token}
            logging.info('Initiating kubeapi session with auth token...')
            apiclient = client.ApiClient(aConfiguration)
            return apiclient
        elif os.path.exists(homedir + '/.kube/config'):
            config.verify_ssl = False
            k8sclient = config.new_client_from_config()
            logging.info('Found kubeconfig file on ' + homedir + '/.kube/config')
            return k8sclient
        else:
            raise Exception('Unauthorized: No kubeconfig file or bearer token found so cannot instantiate client instance')