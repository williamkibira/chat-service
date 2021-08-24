import os
import socket
from typing import Dict, List

from decouple import config
from yaml import safe_load

from app.core.discovery.client import ServiceDiscoveryClient, ConsulClient, Credentials
from app.settings import RESOURCES_DIRECTORY


class BuildInformation(object):
    __instance__ = None

    def __init__(self, entries: Dict):
        self.__name: str = entries["name"]
        self.__version: str = entries["version"]
        self.__repository: str = entries["repository"]
        self.__environment: str = entries["environment"]
        self.__commit_hash: str = entries["commit_hash"]
        self.__build_date: str = entries["build_date"]
        self.__build_epoch: int = entries["build_epoch_sec"]

    def name(self):
        return self.__name

    def version(self):
        return self.__version

    def repository(self):
        return self.__repository

    def environment(self):
        return self.__environment

    def commit_hash(self):
        return self.__commit_hash

    def build_date(self):
        return self.__build_date

    def build_date_epoch(self):
        return self.__build_epoch

    @staticmethod
    def fetch():
        if BuildInformation.__instance__ is None:
            application_file_path = os.path.join(
                RESOURCES_DIRECTORY, "application.yml")
            with open(application_file_path) as f:
                content_map = safe_load(f)
                BuildInformation.__instance__ = BuildInformation(content_map)
        return BuildInformation.__instance__


class Configuration(object):
    __instance__ = None

    def __init__(
            self,
            build_information: BuildInformation,
            content_map: Dict,
            client: ServiceDiscoveryClient,
            test_mode: bool = False) -> None:
        self.__build_information = build_information
        self.__database_uri: str = content_map["database"]["uri"]
        self.__nats_configuration = content_map["nats"]
        self.__port: int = int(content_map["port"])
        self.__client: ServiceDiscoveryClient = client
        if self.__client is not None:
            self.__register_service()
        self.__test_mode = test_mode

    def __del__(self):
        if self.__client is not None:
            self.__deregister_service()

    def database_uri(self) -> str:
        return self.__database_uri

    def build_information(self) -> BuildInformation:
        return self.__build_information

    def nats_configuration(self) -> Dict:
        return self.__nats_configuration

    def port(self) -> int:
        return self.__port

    def is_in_test_mode(self):
        return self.__test_mode

    def __register_service(self):
        tags: List = [self.__build_information.environment()]
        hostname = socket.gethostname()
        host = socket.gethostbyname(hostname)
        self.__client.register(
            name=self.__build_information.name(),
            host=host,
            port=self.__port,
            health_check="http://{}:{}/health-check".format(host, self.__port),
            tags=tags
        )

    def __de_register_service(self):
        self.__client.de_register(service_id=self.__build_information.name())

    @staticmethod
    def local():
        build_information = BuildInformation.fetch()
        content_map = Configuration.read_settings()
        return Configuration(build_information=build_information, content_map=content_map, client=None)

    @staticmethod
    def test():
        build_information = BuildInformation.fetch()
        content_map = Configuration.read_settings(testing=True)
        return Configuration(build_information=build_information, content_map=content_map, client=None, test_mode=True)

    @staticmethod
    def remote():
        build_information = BuildInformation.fetch()
        client = ConsulClient(credentials=Credentials())
        tags: List = []
        # tags.append(build_information.environment())
        content = client.fetch(tag=tags, key=build_information.name())
        content_map = safe_load(content)
        print("FETCHING FROM CONSUL")
        return Configuration(
            build_information=build_information,
            content_map=content_map,
            client=client)

    @staticmethod
    def read_settings(testing: bool = False) -> Dict:
        settings_file = os.path.join(RESOURCES_DIRECTORY, "test-settings.yml" if testing else "settings.yml")
        with open(settings_file) as f:
            content_map = safe_load(f)
            return content_map
        return {}

    @staticmethod
    def get_instance(testing: bool = False):
        if Configuration.__instance__ is None:
            if config("CONSUL_ENABLED", default=False, cast=bool):
                Configuration.__instance__ = Configuration.remote()
            elif testing:
                Configuration.__instance__ = Configuration.test()
            else:
                Configuration.__instance__ = Configuration.local()
        return Configuration.__instance__
