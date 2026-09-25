"""Fronteira de conectividade para publicação futura de telemetria."""


class Connectivity:
    def publish(self, topic, payload):
        raise NotImplementedError
