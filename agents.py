import json
import os
import copy


AGENTS_FILE_PATH = os.path.join(os.path.dirname(__file__), 'agents.json')


def __load_supported_environments(agents):
    supported = copy.deepcopy(agents)

    del supported['agents']

    for source in supported['sources'].values():
        for os in source['operatingSystems'].values():
            for arch in os['architectures'].values():
                del arch['agent']

    return supported


with open(AGENTS_FILE_PATH, 'r') as f:
    agents = json.load(f)

supported = __load_supported_environments(agents)
