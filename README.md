<p align="center">
<a href="https://www.aliyun.com/product/graphcompute"><img src="https://raw.githubusercontent.com/aliyun/alibabacloud-graphcompute-java-sdk/master/src/resources/GraphCompute-blue.png"></a>
</p>

<h1 align="center">GraphCompute SDK for Python</h1>
<p align="center">




The GraphCompute SDK for Python allows user to access [GraphCompute Service](https://www.aliyun.com/product/graphcompute) on Alibaba Cloud. You can access Graph Compute service without the need to generate accesskey-related signature manually. This README document introduces how to obtain and call GraphCompute SDK for Python. If you have any problem while using GraphCompute SDK for Python, please [submit an issue](https://github.com/aliyun/alibabacloud-graphcompute-python-sdk/issues/new).

## Requirements

- To use GraphCompute SDK for Python, you must have an Alibaba Cloud account as well as an `AccessKey ID` and an `AccessKey Secret`. Create and view your AccessKey on the [RAM console](https://ram.console.aliyun.com "RAM console") or contact your system administrator.
- To use  GraphCompute SDK for Python to access the APIs of a product, you must first activate the product on the [Alibaba Cloud console](https://homenew.console.aliyun.com/) if required.
- Python 2.7 is strongly recommended


## Installation

Install the official release version through PIP:

```bash
$ pip install graphcompute
```

You can also install the unzipped installer package directly:

```
$ python setup.py install
```



## Getting Started

```python
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
```



More examples can be referred in `basic_func_examples.py` under "examples" directory.



## License

[Apache-2.0](http://www.apache.org/licenses/LICENSE-2.0)

