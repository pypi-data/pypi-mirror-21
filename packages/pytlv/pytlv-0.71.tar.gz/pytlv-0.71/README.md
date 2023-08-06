TLV (tag length lavue) data parser, especially useful for [EMV](http://emvco.com) tags parsing

To import the pytlv module in your code:
```python
from pytlv.TLV import *

```

To parse data from a TLV string:
```python
tlv = TLV(['84', 'A5']) # provide the possible tag values
tlv.parse('840E315041592E5359532E4444463031A5088801025F2D02656E')
>>> {'84': '315041592E5359532E4444463031', 'A5': '8801025F2D02656E'}

```

To build a TLV string:
```python
tlv = TLV(['9F02', '9F04'])
tlv.build({'9f02': '000000001337'})
>>> '9F0206000000001337'

```

