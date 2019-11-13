GraphCompute SDK for Python
===========================================


The GraphCompute SDK for Python allows user to access `GraphCompute Service <https://www.aliyun.com/product/graphcompute>`_ on Alibaba Cloud. You can access Graph Compute service without the need to generate accesskey-related signature manually. This README document introduces how to obtain and call GraphCompute SDK for Python. If you have any problem while using GraphCompute SDK for Python, please `submit an issue <https://github.com/aliyun/alibabacloud-graphcompute-python-sdk/issues/new>`_.

Requirements
------------


* To use GraphCompute SDK for Python, you must have an Alibaba Cloud account as well as an ``AccessKey ID`` and an ``AccessKey Secret``. Create and view your AccessKey on the `RAM console` or contact your system administrator.
* To use  GraphCompute SDK for Python to access the APIs of a product, you must first activate the product on the `Alibaba Cloud console <https://homenew.console.aliyun.com/>`_ if required.
* Python 2.7 is strongly recommended

Installation
------------

Install the official release version through PIP:

.. code-block:: bash

   $ pip install graphcompute

You can also install the unzipped installer package directly:

.. code-block::

   $ python setup.py install

Getting Started
---------------

.. code-block:: python

   # -*- coding: utf-8 -*-

   from graphcompute import GraphCompute_Client
   from graphcompute.utils.auth import Credentials

   access_key_id = "your access_key_id"
   access_key_secret = "your access_key_secret"
   cred = Credentials(access_key_id, access_key_secret)

   instance_domain = "your instance domain with port"
   remote_endpoint = "ws://%s/gremlin" % str(instance_domain)
   client = GraphCompute_Client(remote_endpoint, 'g', cred)

   query="g.V()"
   result = client.submit(query).one()

   client.close()

More examples can be referred in ``basic_func_examples.py`` under "examples" directory.

License
-------

`Apache-2.0 <http://www.apache.org/licenses/LICENSE-2.0>`_
