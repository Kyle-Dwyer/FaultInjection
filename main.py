import os
import time

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