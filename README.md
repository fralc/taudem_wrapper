# Taudem Wrapper

A tool for calling Taudem executables by means of python functions.

Usage example:

```python
from taudem_functions import pit_remove

pit_remove(
    z=r"path_to/dem.tif",
    fel=r"path_to/filled_dem.tif"
)
```

Taudem path, MPI path, and number of processes to be used must be set in *taudem_settings.yaml*. 

