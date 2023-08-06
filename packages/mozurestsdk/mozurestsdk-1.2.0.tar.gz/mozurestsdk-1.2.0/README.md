# Mozu Python SDK

Python SDK for the full v1.18 Mozu Api


## Usage:

### Install using Pip
```
	pip install mozurestsdk

	#update
	pip install mozurestsdk --update
```

### initialize client from using config file
```
from mozurestsdk import mozuclient
client = mozuclient.configure(config="<path to config file>");

#sample config
[MozuConfig]
applicationKey=[applicationKey]
sharedSecret=[sharedSecret]
#set to false if using proxy
verifySSLCert=False
#optional values
#set base authurl value for non-prod environments 
#baseAuthUrl=[auth url]
tenantId=[tenantId]
tenantUrl=[tenantUrl]
```

###Get Tenant Information
```
from mozurestsdk.platform.tenant import Tenant
from mozurestsdk.apiexception import ApiException;
tenant = Tenant().getTenant(1234);
```

###Get Products

```
from mozurestsdk.apicontext import ApiContext;
from mozurestsdk.commerce.catalog.admin.product import Product;
#apicontext values can be passed in config file or used with config file. code will merge values from config file and values passed in constructor
apiContext = ApiContext(catalogId=1,masterCatalogId=1);
product = Product(apiContext);
p = product.getProduct("test");
```

