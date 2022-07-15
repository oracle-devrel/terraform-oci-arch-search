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
