# django-sql-server-bcp
A utility for using mssql-tools BCP command with Django models.

## Installation

`pip install django-sql-server-bcp`

## Requirements

If on Linux or Mac, install mssql-tools

- For Mac: https://blogs.technet.microsoft.com/dataplatforminsider/2017/04/03/sql-server-command-line-tools-for-mac-preview-now-available/
- For Linux: https://docs.microsoft.com/en-us/sql/linux/sql-server-linux-setup-tools


1. On Linux, you must use Microsoft's driver in your odbc.ini. Otherwise, you'll get error `The DSN specified an unsupported driver.`.
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

2. Make sure `bcp` is is accessible to execute

   `sudo ln -s /opt/mssql-tools/bin/bcp /usr/local/bin/bcp`

3. On Windows, using BCP via ODBC DNS name has proven to be painful or straight up broken. *django-sql-server-bcp* will prefer to connect via server HOST if available. So please set `HOST` in your django DATABSAES settings if you're having problems with getting BCP to work on Windows. You can leave `dsn` name in your django settings.


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
from models import StockPrice


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

You should see output similar to the following:

```
Starting copy...

499 rows copied.
Network packet size (bytes): 4096
Clock Time (ms.) Total     : 10     Average : (49900.0 rows per sec.)
```

## Caveats

- String data cannot contain commas or newlines because bulk data file format is flimsy CSV.
- Untested with long strings, dates, binary data.
- Can't be used in a django transaction involving the same table that BCP is accessing - you'll end up locking the table and BCP won't be able to get a lock on it and BCP will wait indefinitely.

## Troublehooting


### The DSN specified an unsupported driver

- On Linux, see Requirements above
- On Windows, when you setup your ODBC data source in Windows, select "SQL Server Native Client XX". Not "SQL Server" or "ODBC Driver XX for SQL Server". For more info: https://docs.microsoft.com/en-us/sql/relational-databases/native-client-odbc-bulk-copy-operations/performing-bulk-copy-operations-odbc

### The specified DSN contains an architecture mismatch between the Driver and Application

In Windows, This usually means BCP is 32-bit and you've trying to use a 64-bit ODBC connection. Add your ODBC connection under both 32-bit and 64-bit ODBC managers.

### Could not find stored procedure 'sp_describe_first_result_set'.

https://connect.microsoft.com/SQLServer/feedback/details/2777154/attempt-to-use-bcp-2016-to-export-from-sql-2008-or-earlier-fails-with-obscure-error-message

> This error is due to the version of ODBC driver you are using: version 13. You can resolve this issue buy uninstalling the version from Program and features, and install the version 13.1 you can find: https://www.microsoft.com/en-us/download/details.aspx?id=53339

### Unable to open BCP host data-file
On Linux, if www-data can't create a format file, it's a real pain to troubleshoot. `bcp` wants to access a few files covertly and fails without telling you why.
    - To turn on file access auditing, you may discover that `bcp` is trying to create a `/var/www/.odbc.ini` or access `/etc/localtime`

```bash
    # install auditd
    sudo apt install auditd
    # Turn on file access auditing for all files where success=0
    sudo auditctl -w / -k bcp_debug
    # Run bcp commend as www-data
    # Then search audit log for failures
    sudo ausearch --interpret --exit -13
```

Search the log for `success=no` and try to see what files bcp is being denied access to

- For some reason, bcp tries to create `.odbc.ini` in www-data's home folder (e.g. /var/www/.odbc.ini). Make sure www-data's home folder is writeable by www-data
- Another problem was that Microsoft docs say to pass `nul` to format command which, on Windows is a nul file but on Linux, bcp will try to open file named `nul` and fails with permission error. On Linux, pass `/dev/null` instead of `nul`.

### BCP is hanging, stuck at "Starting copy..."

- Make sure you are not calling BCP from within a django transaction that accessing the same table as BCP
- Make sure you do not have any active transactions locking the table or hung transactions locking the table

Check for transaction:

```sql
SELECT S.*
FROM sys.dm_exec_requests R
INNER JOIN sys.dm_exec_sessions S
ON S.session_id = R.blocking_session_id;
```