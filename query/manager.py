import os
from typing import Callable
from autoquery.queries import Query
from autoquery.scenarios import *
from autoquery.utils import random_from_weighted
import logging
import random
import time
import argparse
from multiprocessing import Process, Pool

logging.basicConfig(
    format='%(asctime)s.%(msecs)03d [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.INFO
)
logger = logging.getLogger("autoquery-manager")

url = 'http://175.27.169.178:32677'
minute = 60
hour = 60 * minute

# 记录异常情况下函数执行时间
fun_dic = {}


def constant_query(target: str, timeout: int = 24 * hour):
    q = Query(url)

    def preserve_scenario():
        query_and_preserve(q)

    def payment_scenario():
        query_and_pay(q)

    def cancel_scenario():
        query_and_cancel(q)

    def collect_scenario():
        query_and_collect(q)

    def execute_scenario():
        query_and_execute(q)

    if not q.login():
        return

    count = random.randint(3, 5)
    interval = random.randint(10, 20)

    query_weights = {
        q.query_cheapest: 20,
        q.query_orders: 30,
        q.query_food: 5,
        q.query_high_speed_ticket: 50,
        q.query_contacts: 10,
        q.query_min_station: 20,
        q.query_quickest: 20,
        q.query_high_speed_ticket_parallel: 10,
        preserve_scenario: 30,
        payment_scenario: 20,
        cancel_scenario: 20,
        collect_scenario: 20,
        execute_scenario: 20,
    }

    forbid_query = {
        "travel": [q.query_high_speed_ticket,
                   q.query_high_speed_ticket_parallel,
                   q.query_min_station,
                   q.query_cheapest,
                   q.query_quickest,
                   preserve_scenario],
        "ticketinfo": [q.query_high_speed_ticket,
                       q.query_high_speed_ticket_parallel,
                       q.query_min_station,
                       q.query_cheapest,
                       q.query_quickest,
                       preserve_scenario],
        "route": [q.query_high_speed_ticket,
                  q.query_min_station,
                  q.query_cheapest,
                  q.query_quickest,
                  preserve_scenario],
        "order": [q.query_high_speed_ticket,
                  q.query_min_station,
                  q.query_cheapest,
                  q.query_quickest,
                  q.query_orders,
                  payment_scenario,
                  cancel_scenario,
                  collect_scenario],
        "basic": [q.query_high_speed_ticket,
                  q.query_min_station,
                  q.query_cheapest,
                  q.query_quickest],
        "user": [cancel_scenario],
        "travel_plan": [q.query_min_station,
                        q.query_cheapest,
                        q.query_quickest],
        "station": [q.query_high_speed_ticket,
                    q.query_high_speed_ticket_parallel,
                    q.query_min_station,
                    q.query_cheapest,
                    q.query_quickest,
                    q.query_orders,
                    q.query_other_orders],

    }

    for fun in forbid_query[target]:
        del query_weights[fun]

    for _ in range(0, count):
        func = random_from_weighted(query_weights)
        logger.info(f'constant execute query: {func.__name__}')
        try:
            func()
        except Exception:
            logger.exception(f'constant query {func.__name__} got an exception')

        time.sleep(interval)

    return


# 随机次数随机场景进行查询
def random_query(q: Query, weights: dict, count: int = random.randint(3, 5), interval: int = random.randint(10, 20)):
    """
    登陆一个用户并按权重随机发起请求
    :param weights: 权重dict
    :param count: 请求次数
    :param interval: 请求间隔
    """
    if not q.login():
        return

    for _ in range(0, count):
        func = random_from_weighted(weights)
        logger.info(f'execute query: {func.__name__}')
        try:
            execute_time = time.strftime("%Y-%m-%d %H:%M:%S")
            func()
            fun_dic[execute_time] = func.__name__
        except Exception:
            logger.exception(f'query {func.__name__} got an exception')

        time.sleep(interval)

    return


def run(task: Callable, timeout: int):
    task()
    # start = time.time()
    # while time.time() - start < timeout:
    #     task()
    #     time.sleep(1)
    return


def query_travel(timeout: int = 5 * minute):
    q = Query(url)

    def preserve_scenario():
        query_and_preserve(q)

    query_weights = {
        q.query_high_speed_ticket: 10,
        q.query_high_speed_ticket_parallel: 10,
        q.query_min_station: 10,
        q.query_cheapest: 10,
        q.query_quickest: 10,
        preserve_scenario: 50,
    }

    def task():
        random_query(q, query_weights)

    run(task, timeout)
    return


def query_ticketinfo(timeout: int = 5 * minute):
    q = Query(url)

    def preserve_scenario():
        query_and_preserve(q)

    query_weights = {
        q.query_high_speed_ticket: 10,
        q.query_high_speed_ticket_parallel: 10,
        q.query_min_station: 10,
        q.query_cheapest: 10,
        q.query_quickest: 10,
        preserve_scenario: 50,
    }

    def task():
        random_query(q, query_weights)

    run(task, timeout)
    return


def query_route(timeout: int = 5 * minute):
    q = Query(url)

    def preserve_scenario():
        query_and_preserve(q)

    query_weights = {
        q.query_high_speed_ticket: 10,
        q.query_min_station: 10,
        q.query_cheapest: 10,
        q.query_quickest: 10,
        preserve_scenario: 50,
    }

    def task():
        random_query(q, query_weights)

    run(task, timeout)
    return


def query_order(timeout: int = 5 * minute):
    q = Query(url)

    def payment_scenario():
        query_and_pay(q)

    def cancel_scenario():
        query_and_cancel(q)

    def collect_scenario():
        query_and_collect(q)

    query_weights = {
        q.query_high_speed_ticket: 10,
        q.query_min_station: 10,
        q.query_cheapest: 10,
        q.query_quickest: 10,
        q.query_orders: 20,
        payment_scenario: 50,
        cancel_scenario: 50,
        collect_scenario: 50,
    }

    def task():
        random_query(q, query_weights)

    run(task, timeout)
    return


def query_basic(timeout: int = 5 * minute):
    q = Query(url)

    query_weights = {
        q.query_high_speed_ticket: 10,
        q.query_min_station: 10,
        q.query_cheapest: 10,
        q.query_quickest: 10,
    }

    def task():
        random_query(q, query_weights)

    run(task, timeout)
    return


def query_travel_plan(timeout: int = 5 * minute):
    q = Query(url)

    query_weights = {
        q.query_min_station: 10,
        q.query_cheapest: 10,
        q.query_quickest: 10,
    }

    def task():
        random_query(q, query_weights)

    run(task, timeout)
    return


def query_station(timeout: int = 5 * minute):
    q = Query(url)

    query_weights = {
        q.query_high_speed_ticket: 10,
        q.query_high_speed_ticket_parallel: 10,
        q.query_min_station: 10,
        q.query_cheapest: 10,
        q.query_quickest: 10,
        q.query_orders: 20,
        q.query_other_orders: 20,
    }

    def task():
        random_query(q, query_weights)

    run(task, timeout)
    return


def query_user(timeout: int = 5 * minute):
    q = Query(url)

    def cancel_scenario():
        query_and_cancel(q)

    query_weights = {
        cancel_scenario: 100,
    }

    def task():
        random_query(q, query_weights)

    run(task, timeout)
    return


chaos_path = {'basic-network-delay': '../chaos/network_delay/basic_network_delay.yml',
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


def select_fault(idx: int) -> str:
    # All fault
    fault = [
        # 0-7
        'basic-network-delay', 'order-network-delay', 'route-network-delay', 'station-network-delay',
        'ticketinfo-network-delay', 'travel-network-delay', 'travel-plan-network-delay', 'user-network-delay',
        # 8-15
        'basic-cpu-stress', 'order-cpu-stress', 'route-cpu-stress', 'station-cpu-stress', 'ticketinfo-cpu-stress',
        'travel-cpu-stress', 'travel-plan-cpu-stress', 'user-cpu-stress', 'basic-http-outbound',
        # 16-23
        'order-http-outbound', 'route-http-outbound', 'station-http-outbound', 'ticketinfo-http-outbound',
        'travel-http-outbound', 'travel-plan-http-outbound', 'user-http-outbound']
    random_fault = [10, 5, 13, 21, 11, 16, 4, 23, 1, 9, 17, 8, 18, 7, 19, 12, 6, 22, 15, 0, 20, 3, 14, 2,
                    21, 10, 16, 5, 23, 4, 13, 1, 11, 7, 9, 6, 17, 8, 0, 18, 3, 12, 19, 2, 22, 15, 20, 14,
                    1, 21]
    if idx < 0 or idx > 49:
        return ""
    return fault[random_fault[idx]]


def workflow(times: int = 50, task_timeout: int = 5 * minute):
    # task for each query
    tasks = {
        "travel": query_travel,
        "ticketinfo": query_ticketinfo,
        "route": query_route,
        "order": query_order,
        "basic": query_basic,
        "user": query_user,
        "travel_plan": query_travel_plan,
        "station": query_station,
    }
    p = Pool(4)
    # # 持续进行正常query
    # logger.info('start constant query')
    # p.apply_async(constant_query)

    for current in range(times):
        # 选择故障
        fault = select_fault(current)
        if fault == "":
            logger.info("no task, waiting for 1 minute")
            time.sleep(1 * minute)
            continue
        fault_split = fault.split("-")
        # 选择task
        target = fault_split[0]
        if fault_split[0] == "travel" and fault_split[1] == "plan":
            target = "travel_plan"
        task = tasks[target]
        # 注入故障
        logger.info(f'fault inject: {fault}')
        apply(chaos_path[fault])
        time.sleep(10)
        # 异常
        logger.info(f'execute task: {task.__name__}')
        p.apply_async(task, args=(task_timeout,))
        # 正常
        p.apply_async(constant_query, args=(target, task_timeout))
        # 恢复故障
        time.sleep(5 * minute)
        logger.info(f'fault recover: {fault}')
        delete(chaos_path[fault])
        # 间隔3min
        time.sleep(3 * minute)

    p.close()
    logger.info('waiting for constant query end...')
    p.join()
    return


def arguments():
    parser = argparse.ArgumentParser(description="query manager arguments")
    parser.add_argument(
        '--duration', help='query constant duration (times)', default=50)
    parser.add_argument('--url', help='train ticket server url',
                        default='http://175.27.169.178:32677')
    return parser.parse_args()


def main():
    args = arguments()
    global url
    url = args.url
    duration = int(args.duration)
    logger.info(f'start auto-query manager for {duration} times')

    logger.info('start query workflow')
    workflow(duration)
    logger.info('workflow ended')
    logger.info('auto-query manager ended')
    logger.info(f'execute_func_dict: {fun_dic}')


if __name__ == '__main__':
    main()
