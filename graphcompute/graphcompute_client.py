# -*- coding: utf-8 -*-

from gremlin_python.driver.client import Client
from utils.auth import Auth

class GraphCompute_Client(Client):
    def __init__(self, url, traversal_source, credential, protocol_factory=None,
                 transport_factory=None, pool_size=None, max_workers=None):
        maxgraph_auth = Auth(credential)
        Client.__init__(self, url, traversal_source, protocol_factory,
                        transport_factory, pool_size, max_workers,
                        username=maxgraph_auth.gen_user(), password=maxgraph_auth.gen_remote_credentials())


