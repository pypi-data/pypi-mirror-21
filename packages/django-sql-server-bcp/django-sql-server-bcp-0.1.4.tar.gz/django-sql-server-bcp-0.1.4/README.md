# django-sql-server-bcp
A utility for using mssql-tools BCP command with Django models.

## Installation

`pip install django-sql-server-bcp`

## Requirements

If on Linux or Mac, install mssql-tools

- For Mac: https://blogs.technet.microsoft.com/dataplatforminsider/2017/04/03/sql-server-command-line-tools-for-mac-preview-now-available/
- For Linux: https://docs.microsoft.com/en-us/sql/linux/sql-server-linux-setup-tools


On Linux, you must use Microsoft's driver in your odbc.ini. Otherwise, you'll get error `The DSN specified an unsupported driver.`. 
If you're using pyodbc, your driver might look like:

```
[my_dsn_name]
Driver = /usr/local/lib/libtdsodbc.so

```

Change it to (e.g. on Ubuntu):

```
[my_dsn_name]
Driver = /opt/microsoft/msodbcsql/lib64/libmsodbcsql-13.1.so.6.0
```

## Usage

Example Django model:


```python
from django.db import models

class StockPrice(models.Model):

    id = models.AutoField(primary_key=True)
    symbol = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=15, decimal_places=4)
    timestamp = models.DateTimeField()


```

**Example BCP usage with `StockPrice` Model.** 

Create a dict with the properties of your model. Then save via BCP:

```python
from random import random

rows = []
for i in range(1, row_count):
    rows.append(dict(
        symbol='GOOG',
        price='%.2f' % (100 * random()),
        timestamp=str(datetime.datetime.now())
    ))

bcp = BCP(StockPrice)
bcp.save(rows)
print cp.save(rows)


```

You should output similar to the following:

```
Starting copy...

499 rows copied.
Network packet size (bytes): 4096
Clock Time (ms.) Total     : 10     Average : (49900.0 rows per sec.)
```

## Caveats

- String data cannot contain commas or newlines because bulk data file format is flimsy CSV.
- Untested with long strings, dates, binary data.

