"""High dynamic range imaging via tone-mapping.

See: Recovering High Dynamic Range Radiance Maps from Photographs
     Paul E. Debevec and Jitendra Malik
     http://www.debevec.org/Research/HDR/
"""

import numpy as N

class PhotometrySampler(object):
    def __init__(self,image_collection):
        pass

class DeviceResponse(object):
    def __init__(self,pm_sampler):
        pass

class HDRMapperNaive(object):
    def __init__(self,device_response):
        pass

    def __call__(self,image_collection,
                 std_dev=16,log_scale=0.25):
        """
        Stack images, using (value/exposure) as the radiance
        value. Input values around 128 are favored, with values closer
        to the extremes 0 and 255 weighing much less.

        Input:
        ------
        std_dev : float
            Width of Gaussian used in weighing input values.
        log_scale : float
            Scale of the log intensity transform.  Decrease for darker
            output image.

        """
        ic = image_collection
        out = N.zeros(ic[0].shape)
        outweight = N.zeros(ic[0].shape)
        for img in ic:
            weight = N.exp(-((img - 128.)**2/(2*std_dev**2)))
            out += img / img.exposure * weight
            outweight += weight

        out /= outweight
        out = N.log(log_scale*out)
        out -= out.min()
        out /= out.max()

        return out



