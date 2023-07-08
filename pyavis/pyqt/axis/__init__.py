from .sample_axis import SampleAxisItem
from .time_axis import TimeAxisItem

def createAxis(type="sample", *args, **kwargs):
    if type == "sample":
        return SampleAxisItem(*args, **kwargs)
    elif type == "time":
        return TimeAxisItem(*args, **kwargs)
    else:
        raise ValueError("Invalid axis type")
