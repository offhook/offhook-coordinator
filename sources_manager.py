import json
import os
import copy
from models import DownloadSpec


DEFAULT_SOURCES_FILE_PATH = os.path.join(os.path.dirname(__file__), 'sources.json')
DEFAULT_ROUTING_FILE_PATH = os.path.join(os.path.dirname(__file__), 'agents_routing.json')


class SourcesManager:

    def __init__(self, sources_file_path=DEFAULT_SOURCES_FILE_PATH, routing_file_path=DEFAULT_ROUTING_FILE_PATH):
        with open(sources_file_path, 'r') as f:
            self.__sources = json.load(f)

        with open(routing_file_path, 'r') as f:
            self.__routing = json.load(f)

        self.__supported_sources = copy.deepcopy(self.__sources)
        for source in self.__supported_sources.values():
            for operating_system in source['operatingSystems'].values():
                for arch in operating_system['architectures'].values():
                    del arch['agent']

    def get_host_port_for_agent(self, agent_key):
        agent = self.__routing[agent_key]
        return agent['host'], agent['port']

    def get_supported_sources(self):
        return copy.deepcopy(self.__supported_sources)

    def get_agent_key_for_spec(self, spec: DownloadSpec):
        if spec.source not in self.__sources:
            raise ValueError(f'Source "{spec.source}" is not supported')

        operating_systems = self.__sources[spec.source]['operatingSystems']
        if spec.os not in operating_systems:
            raise ValueError(f'Operating system "{spec.os}" is not supported')

        architectures = operating_systems[spec.os]['architectures']
        if spec.architecture not in architectures:
            raise ValueError(f'Architecture "{spec.architecture}" is not supported')

        agent_key = architectures[spec.architecture]['agent']

        return agent_key
