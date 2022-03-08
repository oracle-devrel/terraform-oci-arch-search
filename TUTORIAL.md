# OCI Search Service with OpenSearch - Tutorial

## **Pre-requisites**  

### 1. Create the required service policies in the OCI Console, tailoring them to your needs
(e.g. change *any-user* to the desired group, provide the path to the compartment if required)  
  
Working policies:  

```
Allow any-user to manage search-insights-family in compartment opensearch
Allow service search-insights to manage vnics in compartment opensearch
Allow service search-insights to use subnets in compartment opensearch
Allow service search-insights to use network-security-groups in compartment opensearch
```

### 2. Create a VCN with a public subnet and a private subnet

Simplified process:  

Console menu &rarr; Networking &rarr; Virtual Cloud Networks &rarr; Start VCN Wizard &rarr; Create VCN with Internet Connectivity  

Custom process:  

“Create VCN” instead of “Start VCN Wizard”, providing your own desired details.  
<br>
### 3. Create a VM Instance in the public subnet of the VCN
 
Console menu &rarr; Compute &rarr; Instances &rarr; Create instance  
Choose the instance name, compartment and select the public subnet.  
For the other options we will use the default values (Oracle Linux 8, VM.Standard.E4.Flex, assign a public IP).  
Decide whether you wish to use an existing SSH key, or have a new one generated. If choosing to generate, remember to download the keys.

<br>

## **Note** 
For the exercise contained in this tutorial, a Mac was used. Windows command line instructions may differ.  

<br>

## **Tutorial - Steps**  

### 1. Create an OCI Search Service cluster

Console menu &rarr; Databases &rarr; OCI Search Service &rarr; Clusters  
Choose the cluster name and compartment where to create the cluster

<img src=".//media/image1.png" style="width:6.26806in;height:3.10347in"
alt="Graphical user interface, text, application, email Description automatically generated" />

Choose the cluster sizing.

<img src=".//media/image2.png" style="width:6.26806in;height:3.06181in"
alt="Graphical user interface, text, application, email Description automatically generated" />

Select the VCN you created. Select the private subnet.

<img src=".//media/image3.png" style="width:6.26806in;height:3.07847in"
alt="Graphical user interface, text, application, email Description automatically generated" />

After the cluster creation, take note of the API endpoints and the IP
addresses which you can alternatively use. These are present in the OCI
Search Service cluster details page.

<img src=".//media/image4.png" style="width:6.26806in;height:1.97708in"
alt="Graphical user interface, text, application Description automatically generated" />

### 2.  Create security rules in the VCN Security List
  
In the VCN, create a Security List with the following security rules. Alternatively, they can be added to the VCN Default Security List.  
Within your VCN details page &rarr; Security Lists &rarr; chosen Security
List &rarr; Add Ingress Rules

Add a rule for port 9200 (OpenSearch), and a rule for 5601 (OpenSearch Dashboards).

<img src=".//media/image5.png" style="width:6.26806in;height:2.37292in" />

<img src=".//media/image6.png" style="width:6.26806in;height:2.39722in" />

<img src=".//media/image0.png" style="width:7.50806in;height:3.10347in" />

### 3.  Download the required certificate

Run the following command, replacing 'us-ashburn-1' (in both places) with the region name if required: 
```
openssl s_client -CAfile opensearch-us-ashburn-1-oci-oracleiaas-com-chain.pem -showcerts -connect amaaaaaanlc5nbya44qen6foty3gyu7ihpo22mzmtjw5ixtcjgetjcqwipuq.opensearch.us-ashburn-1.oci.oracleiaas.com:9200 >> cert.pem
```  
The certificate will be downloaded and saved in cert.pem, in your current directory.  
  
### 4.  Test the connection to OCI Search Service – OpenSearch endpoint

### 4.1. From inside the created VM instance  
  
a.  Connect to the instance via SSH:  
```
ssh -i ~/.ssh/id_rsa_opensearch.key opc@<your_VM_instance_public_IP>
```
b.  Run one of the following commands:
```
curl https://amaaaaaanlc5nbya44qen6foty3gyu7ihpo22mzmtjw5ixtcjgetjcqwipuq.opensearch.us-ashburn-1.oci.oracleiaas.com:9200 --cacert cert.pem
# OpenSearch API endpoint example, with certificate

curl https://10.1.1.190:9200 --insecure 
# OpenSearch private IP example
```
### 4.2.  From your local machine, through port forwarding

a. Run the following port forwarding SSH command in the Terminal. Do not
close the Terminal afterwards, for the connection to remain in place.

``` 
ssh -C -v -t -L 127.0.0.1:5601:<your_opensearch_dashboards_private_IP>:5601 -L 127.0.0.1:9200<your_opensearch_private_IP>:9200 opc@<your_VM_instance_public_IP> -i <path_to_your_private_key>
```

b. Open a new Terminal window and run the following command:
```
curl https://localhost:9200 --insecure
```

If all the steps were performed correctly you should see a response as
follows, regardless of what option was chosen:  

```
{
  "name" : "opensearch-master-0",
  "cluster_name" : "opensearch",
  "cluster_uuid" : "M6gclrE3QLGEBlkdme8JkQ",
  "version" : {
    "distribution" : "opensearch",
    "number" : "1.2.4-SNAPSHOT",
    "build_type" : "tar",
    "build_hash" : "e505b10357c03ae8d26d675172402f2f2144ef0f",
    "build_date" : "2022-02-08T16:44:39.596468Z",
    "build_snapshot" : true,
    "lucene_version" : "8.10.1",
    "minimum_wire_compatibility_version" : "6.8.0",
    "minimum_index_compatibility_version" : "6.0.0-beta1"
  },
  "tagline" : "The OpenSearch Project: https://opensearch.org/"
}
```

### 5. Ingest data

Run the following commands from within your VM instance: 
```
# download data set

curl -O https://raw.githubusercontent.com/oracle-devrel/terraform-oci-arch-search/main/shakespeare.json

# create mapping

curl
-XPUT "https://<your_opensearch_private_IP>:9200/shakespeare" -H 'Content-Type: application/json' -d' --insecure
{
  "mappings": {
    "properties": {
    "speaker": {"type": "keyword"},
    "play_name": {"type": "keyword"},
    "line_id": {"type": "integer"},
    "speech_number": {"type": "integer"}
    }
  }
}
'

# push the dataset

curl -H 'Content-Type:
application/x-ndjson' -XPOST "https://<your_opensearch_private_IP>:9200/shakespeare/_bulk?pretty" --data-binary @shakespeare.json
--insecure

# check your indices

curl "https://amaaaaaanlc5nbya44qen6foty3gyu7ihpo22mzmtjw5ixtcjgetjcqwipuq.opensearch.us-ashburn-1.oci.oracleiaas.com:9200/_cat/indices" --cacert cert.pem

curl "https://amaaaaaanlc5nbya44qen6foty3gyu7ihpo22mzmtjw5ixtcjgetjcqwipuq.opensearch.us-ashburn-1.oci.oracleiaas.com:9200/oci_metrics/_search?from=40&size=1000&pretty" --cacert cert.pem

OR 

curl -X GET "https://<your_opensearch_private_IP>:9200/_cat/indices" --insecure

curl -X GET "https://<your_opensearch_private_IP>:9200/oci_metrics/_search?from=40&size=1000&pretty" --insecure

```

### 6. Query the OCI Search Service – Sample search query

### 6.1. From the VM instance shell:
```
curl -X GET "https://amaaaaaanlc5nbya44qen6foty3gyu7ihpo22mzmtjw5ixtcjgetjcqwipuq.opensearch.us-ashburn-1.oci.oracleiaas.com:9200/shakespeare/_search?q=speaker:WESTMORELAND&pretty" --cacert cert.pem
# OpenSearch API endpoint example, with certificate

curl -X GET
"https://10.0.1.190:9200/shakespeare/_search?q=speaker:WESTMORELAND&pretty" --insecure
# OpenSearch private IP example
```
### 6.2. From your local terminal, after port forwarding:  
```
curl -X GET "https://localhost:9200/shakespeare/_search?q=speaker:WESTMORELAND&pretty" --insecure
```
### 6.3. From your local browser, after port forwarding:  
```
https://localhost:9200/shakespeare/_search?q=speaker:WESTMORELAND&size=10&pretty
```

Refer to ElasticSearch tutorials for more on query syntax.  


### 7.  Connect to OCI Search Service – OpenSearch Dashboards

From your local machine, through port forwarding
(Ignore this step if you’ve executed it above and the connection is still open):
```
ssh -C -v -t -L 127.0.0.1:5601:<your_opensearch_dashboards_private_IP>:5601 -L 127.0.0.1:9200:<your_opensearch_private_IP>:9200 opc@<your_instance_public_ip> -i <path_to_your_private_key>
```
Access <https://localhost:5601> in a browser of your choice.  
Currently, there will be a warning of the kind "your connection is not private", depending on the browser. Choose the option which allows you to proceed anyway. After that, you should see the screen below.  

<img src=".//media/image7.png" style="width:6.26806in;height:2.85278in" />
  

### 8.  Search and visualize data in OCI Search Service - OpenSearch Dashboards

With the port forwarding connection in place, access https://localhost:5601 in your browser.

<img src=".//media/image8.png" style="width:6.26806in;height:3.20903in" />

Go to Menu &rarr; Management &rarr; Stack Management &rarr; Index Patterns
and create an index pattern, with name = `shakespeare*`

<img src=".//media/image9.png" style="width:6.26806in;height:3.17014in" />

Go to Menu &rarr; Discover to use the Dashboards UI to search your data.  
  
<img src=".//media/image10.png" style="width:6.26806in;height:3.52639in" />

Go to Menu &rarr; Dashboards and follow the steps below to create a sample
pie chart.

a.  Create new &rarr; New Visualization &rarr; Pie

<img src=".//media/image11.png" style="width:6.26806in;height:3.19444in" />

b.  Choose `shakespeare*` as source

c.  In Buckets, click ‘Add’ &rarr; Split slices, provide the parameters
    as below and click ‘Update’

<img src=".//media/image12.png" style="width:6.26806in;height:3.52778in"/>
