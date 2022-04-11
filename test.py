if __name__ == '__main__':
    s = ["basic", "order", "route", "station", "ticketinfo", "travel", "travel-plan", "user"]
    o = {}
    for i in s:
        key = i + "-network-delay"
        value = "./chaos/network_delay/" + i + "_network_delay.yml"
        o[key] = value
    for i in s:
        key = i + "-cpu-stress"
        value = "./chaos/cpu_stress/" + i + "_network_delay.yml"
        o[key] = value
    for i in s:
        key = i + "-http-outbound"
        value = "./chaos/http_outbound/" + i + "_network_delay.yml"
        o[key] = value
    print(o)