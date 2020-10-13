import logging
import sys
import time
import itertools
from src.get import Get
from src.delete import Delete

class Requeue(object):
    def __init__(self, seclist=None, namespace=None):
        self.seclist = seclist
        self.namespace = namespace

    def syncObjects(self):
        logging.info('Getting list of all deployments in the namespace')
        namelist = Get('Deployment', namespace=self.namespace).getResourceNames()
        actionlist = []
        logging.info('Getting list of all deployments to sync in the namespace')
        if len(namelist) == 0:
            logging.error('No deployment objects found in namespace ' + self.namespace)
        else:
            for sec in self.seclist:
                for name in namelist:
                    if sec in str(Get('Deployment', namespace=self.namespace).getResourceYaml()):
                        actionlist.append(name)
                    else:
                        logging.info('Secret ' + sec + ' not referenced by deployment ' + name + ' so skipping this one..')
            actionlist = list(dict.fromkeys(actionlist))
        podlist = []
        if len(actionlist) == 0:
            logging.error('No deployment found that uses secret ' + sec)
        else:
            for action in actionlist:
                podlist.append(Get('Pod', namespace=self.namespace, name=action).getPodNamesFromSelectors())
                logging.info('Requeing deployment ' + action + ' to reflect the config change in ' + sec)
            flatpodlist = (list(itertools.chain.from_iterable(podlist)))
            if len(flatpodlist) == 0:
                logging.error('No pods found in pod list')
            else:
                for pod in flatpodlist:
                    resourcename = Get('Pod', name=pod, namespace=self.namespace).getResourceYaml()['metadata']['labels']['app']
                    print('Resource name is'+ resourcename)
                    currentpodlist = Get('Pod', name=resourcename, namespace=self.namespace).getPodNamesFromSelectors()
                    logging.info('Restarting pods')
                    Delete('Pod', self.namespace, name=pod).deleteResource()
                    time.sleep(3)
                    newpodlist = Get('Pod', name=resourcename, namespace=self.namespace).getPodNamesFromSelectors()
                    try:
                        spawnedpod = list(set(newpodlist) - set(currentpodlist))[0]
                    except IndexError:
                        spawnedpod = None
                        sys.exc_clear()
                    if spawnedpod != None:
                        logging.info('Watching pod to check if pod ' + str(spawnedpod) + ' is running')
                        Watch('Pod', self.namespace, name=spawnedpod).checkPodRunning()
                    else:
                        logging.info('It seems that no new pods have spawned, skipping the pod check')