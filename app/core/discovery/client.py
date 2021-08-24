from typing import List
import consulate
from consulate import Session
from decouple import config
import abc


class Credentials(object):
    def __init__(self):
        self.__host: str = config('CONSUL_HOST', default='localhost')
        self.__port: int = config('CONSUL_PORT', default=8500, cast=int)
        self.__datacenter: str = config('CONSUL_DATACENTER', default='dc1')
        self.__token: str = config('CONSUL_TOKEN', default='')

    def host(self) -> str:
        return self.__host

    def port(self) -> int:
        return self.__port

    def datacenter(self) -> str:
        return self.__datacenter

    def token(self):
        return self.__token


class ServiceDiscoveryClient(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook(cls, subclass):
        return (hasattr(subclass, 'register') and
                callable(subclass.register) and
                hasattr(subclass, 'fetch') and
                callable(subclass.fetch) and
                hasattr(subclass, 'de_register') and
                callable(subclass, subclass.de_register) or
                NotImplemented)

    @abc.abstractmethod
    def register(
            self, name: str,
            host: str,
            port: int,
            health_check: str,
            tags: List[str],
            ttl_seconds: int = 10) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def fetch(self, tag: List[str], key: str) -> str:
        raise NotImplementedError

    @abc.abstractmethod
    def de_register(self, service_id: str) -> None:
        raise NotImplementedError


class ConsulClient(ServiceDiscoveryClient):
    def __init__(self, credentials: Credentials):
        self.__session: Session = consulate.Session(
            host=credentials.host(),
            port=credentials.port(),
            datacenter=credentials.datacenter(),
            token=credentials.token()
        )

    def register(
            self, name: str,
            host: str,
            port: int,
            health_check: str,
            tags: List[str],
            ttl_seconds: int = 10) -> None:

        if self.__session.agent.service.register(
                name=name,
                service_id=name,
                address=host,
                port=port,
                tags=tags,
                httpcheck=health_check,
                interval='{}s'.format(ttl_seconds)
        ):
            print("REGISTERED")
        else:
            print("FAILED TO REGISTER")

    def fetch(self, tag: List[str], key: str) -> str:
        if key in self.__session.kv:
            return self.__session.kv.get(item=key, raw=True)
        return ""

    def de_register(self, service_id: str) -> None:
        self.__session.agent.service.deregister(service_id=service_id)
