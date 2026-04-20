# Taudem Wrapper

A tool for calling Taudem executables by means of python functions.

Usage example:

```python
from taudem_functions import DataWrapper, pit_remove

dtm = DataWrapper('dtm.tif') # Input, it does exist
fel = DataWrapper('fel.tif') # Output, it does not exist, but it will be created by the function

pit_remove(z=dtm, fel=fel)
```

