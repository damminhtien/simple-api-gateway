class Limiter(object):
    r_counter = {}
    ip_counter = {}
    rule = {}

    @classmethod
    def set_rule(cls, route, limit=1000):
        """
        Set limit requests per second to one route, default 1000req/s
        params:
            route: sub-path of url
            limit: maximum number of requests per second
        """
        cls.rule[route] = limit

    @classmethod
    def add_r_counter(cls, route):
        if route in cls.r_counter:
            if route not in cls.rule or cls.r_counter[route] < cls.rule[route]:
                cls.r_counter[route] += 1
        else:
            cls.r_counter[route] = 0

    @classmethod
    def minus_r_counter(cls, route):
        if route in cls.r_counter:
            if cls.r_counter[route] > 0:
                cls.r_counter[route] -= 1
        else:
            cls.r_counter[route] = 0

    @classmethod
    def add_ip_counter(cls, route, ip):
        if ip in cls.ip_counter:
            if route in cls.ip_counter[ip]:
                if cls.r_counter[route] < cls.rule[route]:
                    cls.ip_counter[ip] += 1
            else:
                cls.ip_counter[ip] = 0
        else:
            cls.ip_counter[ip] = {}
            cls.ip_counter[ip][route] = 0

    @classmethod
    def is_limit(cls, route, ip):
        if route not in cls.rule or cls.r_counter[route] < cls.rule[route]:
            cls.add_r_counter(route)
            cls.add_ip_counter(route, ip)
            return True
        return False
