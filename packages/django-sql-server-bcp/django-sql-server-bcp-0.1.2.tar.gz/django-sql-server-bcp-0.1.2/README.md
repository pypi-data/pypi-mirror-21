# django-sql-server-bcp
A utility for using mssql-tools BCP command with Django models.

#Usage

Example Django model:


```python
from django.db import models

class StockPrice(models.Model):

    id = models.AutoField(primary_key=True)
    symbol = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=15, decimal_places=4)
    timestamp = models.DateTimeField()


```

Example BCP usage with `StockPrice` Model:

```python
from random import radom


rows = []
for i in range(1, row_count):
    rows.append(dict(
        symbol='GOOG',
        price='%.2f' % (100 * random()),
        timestamp=str(datetime.datetime.now())
    ))

bcp = BCP(StockPrice)
bcp.save(rows)
cp.save(rows)


```
#Caveats

- String data cannot contain commas or newlines because bulk data file format is flimsy CSV.
- Untested with long strings, dates, binary data.

