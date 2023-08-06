import os

from collections import OrderedDict
from subprocess import check_output, CalledProcessError, STDOUT

import yaml

from hokusai.config import HokusaiConfig
from hokusai.common import print_red, print_green, verbose, select_context, HokusaiCommandError

def pull_config(context):
  config = HokusaiConfig().check()

  try:
    select_context(context)
  except HokusaiCommandError, e:
    print_red(repr(e))
    return -1

  try:
    existing_configmap = check_output(verbose("kubectl get configmap %s-config -o yaml"
                                                % config.project_name), stderr=STDOUT, shell=True)
    configmap_data = yaml.load(existing_configmap)['data']
  except CalledProcessError, e:
    if 'Error from server: configmaps "%s-config" not found' % config.project_name in e.output:
      print("ConfigMap %s-config not found. Creating..." % config.project_name)
      configmap_data = {}
    else:
      print_red("Failed to pull configmap hokusai/%s-config.yml" % context)
      return -1

  configmap_yaml = OrderedDict([
    ('apiVersion', 'v1'),
    ('kind', 'ConfigMap'),
    ('metadata', {
      'labels': {'app': config.project_name},
      'name': "%s-config" % config.project_name
    }),
    ('data', configmap_data)
  ])

  with open(os.path.join(os.getcwd(), 'hokusai', "%s-config.yml" % context), 'w') as f:
    f.write(yaml.safe_dump(configmap_yaml, default_flow_style=False))

  print_green("Pulled configmap hokusai/%s-config.yml" % context)
  return 0

def push_config(context):
  HokusaiConfig().check()

  if not os.path.isfile(os.path.join(os.getcwd(), 'hokusai', "%s-config.yml" % context)):
    print_red("Secrets file hokusai/%s-config.yml does not exist" % context)
    return -1

  try:
    select_context(context)
  except HokusaiCommandError, e:
    print_red(repr(e))
    return -1

  try:
    check_output(verbose("kubectl apply -f %s" % os.path.join(os.getcwd(), 'hokusai', "%s-config.yml" % context)), stderr=STDOUT, shell=True)
  except CalledProcessError:
    print_red("Failed to push configmap hokusai/%s-config.yml" % context)
    return -1

  print_green("Pushed configmap hokusai/%s-config.yml" % context)
  return 0
