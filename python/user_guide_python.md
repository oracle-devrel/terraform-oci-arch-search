# terraform-oci-arch-search

[![License: UPL](https://img.shields.io/badge/license-UPL-green)](https://img.shields.io/badge/license-UPL-green) [![Quality gate](https://sonarcloud.io/api/project_badges/quality_gate?project=oracle-devrel_terraform-oci-arch-search)](https://sonarcloud.io/dashboard?id=oracle-devrel_terraform-oci-arch-search)

## The OCI Search Service with OpenSearch tutorial can be found [HERE](TUTORIAL.md).

## Contributing
This project is open source.  Please submit your contributions by forking this repository and submitting a pull request!  Oracle appreciates any contributions that are made by the open source community.

# Search data using OCI Search Service with OpenSearch DSL Python Client

## User Guide

This user guide specifies how to include and use the dsl-py client in your application.

## Setup

To add the client to your project, install it using [pip](https://pip.pypa.io/en/stable/)
  
```
pip install opensearch-dsl

```
Then import it like any other module:

```
from opensearchpy import OpenSearch
from opensearch_dsl import Search

```
## Sample Code

```
#!python

from opensearchpy import OpenSearch
from opensearch_dsl import Search
host = 'amaaaaaanlc5nbyai2nlgcqrvovh5sxmfqkyeadbyyfphtszmjpqhbao54va.opensearch.us-ashburn-1.oci.oracleiaas.com'
port = 9200
auth = ('admin', 'admin') # For testing only. Don't store credentials in code.
ca_certs_path = '/home/opc/cert.pem' # Provide a CA bundle if you use intermediate CAs with your root CA.

# Optional client certificates if you don't want to use HTTP basic authentication.
client_cert_path = '/home/opc/cert.pem'
# client_key_path = '/full/path/to/client-key.pem'

# Create the client with SSL/TLS enabled, but hostname verification disabled.
client = OpenSearch(
        hosts = [{'host': host, 'port': port}],
        http_compress = True, # enables gzip compression for request bodies
       #http_auth = auth,
        client_cert = client_cert_path,
        # client_key = client_key_path,
        use_ssl = True,
        verify_certs = False,
        ssl_assert_hostname = False,
        ssl_show_warn = False,
       #ca_certs = ca_certs_path
)


index_name = 'my-dsl-index'

response = client.indices.create(index_name)
print('\nCreating index:')
print(response)

# Add a document to the index.
document = {
  'title': 'python',
  'description': 'beta',
  'category': 'search'
}
id = '1'

response = client.index(
    index = index_name,
    body = document,
    id = id,
    refresh = True
    )

print('\nAdding document:')
print(response)

# Search for the document.
s = Search(using=client, index=index_name) \
    .filter("term", category="search") \
    .query("match", title="python")

response = s.execute()

print('\nSearch results:')
for hit in response:
    print(hit.meta.score, hit.title)

# Delete the document.
print('\nDeleting document:')
print('Index deleted', response)

# Delete the index.
response = client.indices.delete(
    index = index_name
)

print('\nDeleting index:')
print(response)

```

## License
Copyright (c) 2022 Oracle and/or its affiliates.

Licensed under the Universal Permissive License (UPL), Version 1.0.

See [LICENSE](LICENSE) for more details.

ORACLE AND ITS AFFILIATES DO NOT PROVIDE ANY WARRANTY WHATSOEVER, EXPRESS OR IMPLIED, FOR ANY SOFTWARE, MATERIAL OR CONTENT OF ANY KIND CONTAINED OR PRODUCED WITHIN THIS REPOSITORY, AND IN PARTICULAR SPECIFICALLY DISCLAIM ANY AND ALL IMPLIED WARRANTIES OF TITLE, NON-INFRINGEMENT, MERCHANTABILITY, AND FITNESS FOR A PARTICULAR PURPOSE.  FURTHERMORE, ORACLE AND ITS AFFILIATES DO NOT REPRESENT THAT ANY CUSTOMARY SECURITY REVIEW HAS BEEN PERFORMED WITH RESPECT TO ANY SOFTWARE, MATERIAL OR CONTENT CONTAINED OR PRODUCED WITHIN THIS REPOSITORY. IN ADDITION, AND WITHOUT LIMITING THE FOREGOING, THIRD PARTIES MAY HAVE POSTED SOFTWARE, MATERIAL OR CONTENT TO THIS REPOSITORY WITHOUT ANY REVIEW. USE AT YOUR OWN RISK. 