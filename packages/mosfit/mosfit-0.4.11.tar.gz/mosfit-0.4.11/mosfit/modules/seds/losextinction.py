"""Definitions for the `LOSExtinction` class."""
from collections import OrderedDict

import numpy as np
from mosfit.modules.seds.sed import SED

from extinction import apply as eapp
from extinction import odonnell94


# Important: Only define one ``Module`` class per file.


class LOSExtinction(SED):
    """Adds extinction to SED from both host galaxy and MW."""

    MW_RV = 3.1

    def process(self, **kwargs):
        """Process module."""
        kwargs = self.prepare_input(self.key('luminosities'), **kwargs)
        self.preprocess(**kwargs)
        zp1 = 1.0 + kwargs[self.key('redshift')]
        self._seds = kwargs[self.key('seds')]
        self._nh_host = kwargs[self.key('nhhost')]
        self._rv_host = kwargs[self.key('rvhost')]
        self._bands = kwargs['all_bands']
        self._band_indices = kwargs['all_band_indices']
        self._frequencies = kwargs['all_frequencies']
        self._band_rest_wavelengths = self._sample_wavelengths / zp1

        av_host = self._nh_host / 1.8e21

        extinct_cache = OrderedDict()
        for si, cur_band in enumerate(self._bands):
            bi = self._band_indices[si]
            # Extinct out host gal (using rest wavelengths)
            if bi >= 0:
                if bi not in extinct_cache:
                    extinct_cache[bi] = odonnell94(
                        self._band_rest_wavelengths[bi], av_host,
                        self._rv_host)
                # Add host and MW contributions
                eapp(
                    self._mw_extinct[bi] + extinct_cache[bi],
                    self._seds[si],
                    inplace=True)
            else:
                # wavelengths = np.array(
                #   [c.c.cgs.value / self._frequencies[si]])
                # Need extinction function for radio
                pass

        return {
            'sample_wavelengths': self._sample_wavelengths,
            self.key('seds'): self._seds,
            self.key('avhost'): av_host
        }

    def preprocess(self, **kwargs):
        """Preprocess module."""
        if self._preprocessed:
            return
        self._ebv = kwargs[self.key('ebv')]
        self._av_mw = self.MW_RV * self._ebv
        # Pre-calculate LOS dust from MW for all bands
        self._mw_extinct = np.zeros_like(self._sample_wavelengths)
        for si, sw in enumerate(self._sample_wavelengths):
            self._mw_extinct[si] = odonnell94(self._sample_wavelengths[si],
                                              self._av_mw, self.MW_RV)
        self._preprocessed = True
