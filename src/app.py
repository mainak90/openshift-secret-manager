from src.sync import Sync
from src.apiclient import ApiClient
from src.requeue import Requeue
from openshift.dynamic import DynamicClient
import src.logger
import logging, os, sys, time, argparse

def main():
    src.logger.setLevel()
    parser = argparse.ArgumentParser(description='Listed arguments --namespace')
    parser.add_argument("-n", "--namespace", help="The namespace of the openshift project to watch")
    args = parser.parse_args()
    namespace = args.namespace
    k8s_client = ApiClient.apiclient()
    dyn_client = DynamicClient(k8s_client)
    v1_resources = dyn_client.resources.get(api_version='v1', kind='Secret')
    while True:
        secdict = Sync(namespace).checkForSync()
        if len(secdict) == 0:
            logging.info('No secrets have changed in the meantime...')
        else:
            logging.info('We have secrets that were modified, requeing the deployments now...')
            Requeue(seclist=secdict, namespace=namespace).syncObjects()
        logging.info('Sleeping 3 minutes before scheduling next check')
        time.sleep(180)

if __name__ == '__main__':
    sys.exit(main())