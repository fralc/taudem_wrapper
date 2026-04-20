import os, sys
from functools import wraps
import inspect
from dataclasses import dataclass
import xarray as xr
import rioxarray


@dataclass
class DataWrapper:
    fn: str
    _data: xr.DataArray = None

    @property
    def data(self):
        if self._data is None:
            self._data = rioxarray.open_rasterio(self.fn).squeeze()
        return self._data

    @data.setter
    def data(self, data: xr.DataArray):
        data.rio.to_raster(self.fn)




def taudify(funzione_parametro, n=4):
    @wraps(funzione_parametro)
    def wrapper(**kwargs):
        signature = inspect.signature(funzione_parametro)
        fname = signature.parameters['fname'].default
        command = f'mpiexec -n {n} --allow-run-as-root {fname}'.lower()
        for k, v in kwargs.items():
            command += f' -{k} {v}'
        os.system(command)
        return
    return wrapper

def take_fn(funzione_parametro):
    @wraps(funzione_parametro)
    def wrapper(**kwargs):
        new_kwargs = {}
        for k, v in kwargs.items():
            if isinstance(v, DataWrapper):
                new_kwargs[k] = v.fn
            else:
                new_kwargs[k] = v
        return funzione_parametro(**new_kwargs)
    return wrapper

@take_fn
@taudify
def pit_remove(z, fel, fname='PitRemove'):
    return

@take_fn
@taudify
def d8_flow_dir(fel, p, fname='D8FlowDir'):
    return

@take_fn
@taudify
def dinf_flow_dir(fel, slp, ang, fname='DinfFlowDir'):
    return

@take_fn
@taudify
def area_d8(p, ad8, fname='AreaD8'):
    return

@take_fn
@taudify
def area_dinf(ang, sca, fname='AreaDinf'):
    return

@take_fn
@taudify
def dinf_dist_down(ang, fel, slp, src, m, dd, fname='DinfDistDown'):
    return

@take_fn
@taudify
def stream_def_by_threshold(ssa, thresh, src, fname='Threshold'):
    return

@take_fn
@taudify
def stream_net(fel, p, ad8, src, ord, tree, coord, net, w, fname='StreamNet'):
    return







