import random
from typing import Callable

from main import *

import yaml
from kubernetes import client, config, utils


# kubectl apply -f yaml_file.yaml
def apply_from_single_file(yaml_file):
    config.load_kube_config()
    k8s_client = client.ApiClient()
    # yaml_file = 'examples/configmap-demo-pod.yml'
    utils.create_from_yaml(k8s_client, yaml_file, verbose=True)
    print("Create Pod ")


def apply_customer_object_from_file(yaml_file):
    config.load_kube_config()
    with open(yaml_file) as f:
        dep = yaml.safe_load(f)
        api = client.CustomObjectsApi()
        resp = api.create_namespaced_custom_object(
            group="Chaos", version="v1alpha1", plural="chaos", body=dep, namespace="ts")
        print("Deployment created. status='%s'" % resp.metadata.name)


def delete_customer_object_from_file(yaml_file):
    config.load_kube_config()
    with open(yaml_file) as f:
        dep = yaml.safe_load(f)
        api = client.CustomObjectsApi()
        resp = api.delete_namespaced_custom_object(
            group="Chaos", version="v1alpha1", plural="chaos", body=dep, namespace="ts")
        print("Deployment deleted. status='%s'" % resp.metadata.name)


# kubectl delete networkchaos network-delay
# kubectl delete -n ts name
def delete_by_kind_and_name(name):
    config.load_kube_config()
    k8s_core_v1 = client.CoreV1Api()
    resp = k8s_core_v1.delete_namespaced_pod(namespace="ts", name=name)
    print("delete Pod ", name)


pods_map = {'basic-network-delay': '../chaos/network_delay/basic_network_delay.yml',
              'order-network-delay': '../chaos/network_delay/order_network_delay.yml',
              'route-network-delay': '../chaos/network_delay/route_network_delay.yml',
              'station-network-delay': '../chaos/network_delay/station_network_delay.yml',
              'ticketinfo-network-delay': '../chaos/network_delay/ticketinfo_network_delay.yml',
              'travel-network-delay': '../chaos/network_delay/travel_network_delay.yml',
              'travel-plan-network-delay': '../chaos/network_delay/travel_plan_network_delay.yml',
              'user-network-delay': '../chaos/network_delay/user_network_delay.yml',

              'basic-cpu-stress': '../chaos/cpu_stress/basic_stress_cpu.yml',
              'order-cpu-stress': '../chaos/cpu_stress/order_stress_cpu.yml',
              'route-cpu-stress': '../chaos/cpu_stress/route_stress_cpu.yml',
              'station-cpu-stress': '../chaos/cpu_stress/station_stress_cpu.yml',
              'ticketinfo-cpu-stress': '../chaos/cpu_stress/ticketinfo_stress_cpu.yml',
              'travel-cpu-stress': '../chaos/cpu_stress/travel_stress_cpu.yml',
              'travel-plan-cpu-stress': '../chaos/cpu_stress/travel_plan_stress_cpu.yml',
              'user-cpu-stress': '../chaos/cpu_stress/user_stress_cpu.yml',

              'basic-http-outbound': '../chaos/http_outbound/basic_http_outbound.yml',
              'order-http-outbound': '../chaos/http_outbound/order_http_outbound.yml',
              'route-http-outbound': '../chaos/http_outbound/route_http_outbound.yml',
              'station-http-outbound': '../chaos/http_outbound/station_http_outbound.yml',
              'ticketinfo-http-outbound': '../chaos/http_outbound/ticketinfo_http_outbound.yml',
              'travel-http-outbound': '../chaos/http_outbound/travel_http_outbound.yml',
              'travel-plan-http-outbound': '../chaos/http_outbound/travel_plan_http_outbound.yml',
              'user-http-outbound': '../chaos/http_outbound/user_http_outbound.yml'}

def run(task: Callable):
    task(10)

def fun(a, b):
    print(a+b)

def test(inti):
    d = [inti]
    def tt(c):
        d[0] += c
        print(d[0])
    return tt

if __name__ == '__main__':
    task = test(0)
    run(task)
    run(task)
    exit(0)
    s = "a_b_c_d"
    print(time.strftime("%Y-%m-%d %H:%M:%S"))
    exit(0)
    print(random.sample(range(0, 24), 2))
    aa = [5, 4, 1, 7, 6, 0, 3, 2]
    b = [10, 13, 11, 9, 8, 12, 15, 14]
    c = [21, 16, 23, 17, 18, 19, 22, 20]
    last = -1
    res = []
    l = [a, b, c]
    ii = [0, 0, 0]
    for i in range(24):
        r = random.randint(0, 2)
        while r == last or ii[r] > 7:
            r = random.randint(0, 2)
        res.append(l[r][ii[r]])
        ii[r] += 1
        last = r
    print(res)

    apply_customer_object_from_file(pods_map["basic-network-delay"])
    delete_customer_object_from_file(pods_map["basic-network-delay"])
    time.sleep(200)
# apply_from_single_file(pods_map['basic-network-delay'])
# time.sleep(60)
# delete_by_kind_and_name("basic-network-delay")
