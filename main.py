import os
import time

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


def apply(file_path):
    command = "kubectl apply -f " + file_path
    os.system(command)


def delete(file_path):
    command = "kubectl delete -f " + file_path
    os.system(command)


if __name__ == '__main__':
    apply(pods_map["basic-network-delay"])
    time.sleep(60)
    delete(pods_map["basic-network-delay"])