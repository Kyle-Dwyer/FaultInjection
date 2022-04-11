import time

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
            group="Chaos",version="v1alpha1",plural="chaos",body=dep, namespace="ts")
        print("Deployment created. status='%s'" % resp.metadata.name)


def delete_customer_object_from_file(yaml_file):
    config.load_kube_config()
    with open(yaml_file) as f:
        dep = yaml.safe_load(f)
        api = client.CustomObjectsApi()
        resp = api.delete_namespaced_custom_object(
            group="Chaos",version="v1alpha1",plural="chaos",body=dep, namespace="ts")
        print("Deployment deleted. status='%s'" % resp.metadata.name)


# kubectl delete networkchaos network-delay
# kubectl delete -n ts name
def delete_by_kind_and_name(name):
    config.load_kube_config()
    k8s_core_v1 = client.CoreV1Api()
    resp = k8s_core_v1.delete_namespaced_pod(namespace="ts", name=name)
    print("delete Pod ", name)


pods_map = {'basic-network-delay': './chaos/network_delay/basic_network_delay.yml',
            'order-network-delay': './chaos/network_delay/order_network_delay.yml',
            'route-network-delay': './chaos/network_delay/route_network_delay.yml',
            'station-network-delay': './chaos/network_delay/station_network_delay.yml',
            'ticketinfo-network-delay': './chaos/network_delay/ticketinfo_network_delay.yml',
            'travel-network-delay': './chaos/network_delay/travel_network_delay.yml',
            'travel-plan-network-delay': './chaos/network_delay/travel_plan_network_delay.yml',
            'user-network-delay': './chaos/network_delay/user_network_delay.yml',

            'basic-cpu-stress': './chaos/cpu_stress/basic_network_delay.yml',
            'order-cpu-stress': './chaos/cpu_stress/order_network_delay.yml',
            'route-cpu-stress': './chaos/cpu_stress/route_network_delay.yml',
            'station-cpu-stress': './chaos/cpu_stress/station_network_delay.yml',
            'ticketinfo-cpu-stress': './chaos/cpu_stress/ticketinfo_network_delay.yml',
            'travel-cpu-stress': './chaos/cpu_stress/travel_network_delay.yml',
            'travel-plan-cpu-stress': './chaos/cpu_stress/travel_plan_network_delay.yml',
            'user-cpu-stress': './chaos/cpu_stress/user_network_delay.yml',

            'basic-http-outbound': './chaos/http_outbound/basic_network_delay.yml',
            'order-http-outbound': './chaos/http_outbound/order_network_delay.yml',
            'route-http-outbound': './chaos/http_outbound/route_network_delay.yml',
            'station-http-outbound': './chaos/http_outbound/station_network_delay.yml',
            'ticketinfo-http-outbound': './chaos/http_outbound/ticketinfo_network_delay.yml',
            'travel-http-outbound': './chaos/http_outbound/travel_network_delay.yml',
            'travel-plan-http-outbound': './chaos/http_outbound/travel_plan_network_delay.yml',
            'user-http-outbound': './chaos/http_outbound/user_network_delay.yml'}

if __name__ == '__main__':
    apply_customer_object_from_file(pods_map["basic-network-delay"])
    delete_customer_object_from_file(pods_map["basic-network-delay"])
# apply_from_single_file(pods_map['basic-network-delay'])
# time.sleep(60)
# delete_by_kind_and_name("basic-network-delay")
