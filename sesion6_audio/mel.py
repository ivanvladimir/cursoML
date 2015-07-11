#!/usr/bin/env python
# -*- coding: utf-8
# ----------------------------------------------------------------------
# Module for MEL scale
# ----------------------------------------------------------------------
# Ivan Vladimir Meza-Ruiz/ ivanvladimir at turing.iimas.unam.mx
# 2013/IIMAS/UNAM
# ----------------------------------------------------------------------
# mel.py is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
# -------------------------------------------------------------------------

""" 
.. module:: mel
    :platform: Unix
    :synopsis: Module for MEL scale operations

.. moduleauthor:: Ivan Meza-Ruiz <ivanvladimir@turing.iimas.unam.mx>

"""

import numpy as np

def mel(fs):
    """
    Transform hertz frecuencies the mel scale frecuencies

    Args:
        fs (numpy dtype): The hertz frecuencies to transform

    Returns:
        numpy dtype with the frecuencies in the mel scale


    Example:

    >>> mel(np.arange(0,10000,1000))


    """
    return 2595.0 * np.log10(1+fs/700.0) 

def mel_(ms):
    """
    Transform mel frecuencies to hertz scale

    Args:
        ms (numpy dtype): The mel frecuencis to transform

    Returns:
        numpy dtype with the frecuencies in the hertz scale

    Example:

    >>> mel_(mel(np.arange(0,10000,1000))) 

    """

    return 700.0 * (np.power(10.,ms/2595.0) -1.)
 
    
def melfilters(nfilters,upfreq=7500.0,lowfreq=300.0,k=512,sr=16000):
    """
    Creates a bank of mel filters
    BASED on http://sphinx-am2wfst.googlecode.com/hg-history/c08d2c86a25c491116bb70b729fb7f2cda7bda2e/t3sphinx/mfcc.py

    Args:
        nfilters int: Number of filters to create

    Kwargs:
        upfreq  (float): upper bound frequency [7500 based on speech]
        lowfreq (float): lower bound frequency [300 based on speech]
        k       (int)  : Number of coeficients to filter
        sr      (int)  : Sample Rate

    Returns:
        numpy dtype with filters

    Example:

    >>> melfilters(26)

    """

    # Space for filters
    filters=np.zeros((k/2+1,nfilters),'d')

    dfreq=float(sr/k)
    upmel=mel(upfreq)
    lowmel=mel(lowfreq)
    dmelbw = (upmel - lowmel) / (nfilters + 1)
    filt_edge = mel_(lowmel + dmelbw * np.arange(nfilters + 2, dtype='d'))
    for filt in range(nfilters):
        # Filter triangles, in DFT points
        leftfr   = round(filt_edge[filt] / dfreq)
        centerfr = round(filt_edge[filt + 1] / dfreq)
        rightfr  = round(filt_edge[filt + 2] / dfreq)
        fwidth   = (rightfr - leftfr) * dfreq
        height   = 2. / fwidth

        if centerfr != leftfr:
            leftslope = height / (centerfr - leftfr)
        else:
            leftslope = 0
        freq = leftfr + 1
        while freq < centerfr:
            filters[freq,filt] = (freq - leftfr) * leftslope
            freq +=  1
        if freq == centerfr: 
            filters[freq,filt] = height
            freq += 1
        if centerfr != rightfr:
            rightslope = height / (centerfr - rightfr)
        while freq < rightfr:
            filters[freq,filt] = (freq - rightfr) * rightslope
            freq +=  1
    return filters 

# Specific MEL filters
#: Typical MEL filter for birds
MELfilterbank_birds=melfilters(40,upfreq=4000,
                                lowfreq=0,
                                k=512,
                                sr=16000)

#: MEL filter based on sphinx speech
MELfilterbank_sphinx=melfilters(40,upfreq=6855.4976,
                                lowfreq=133.3333,
                                k=512,
                                sr=16000)

#: Typical MEL filter for speech
MELfilterbank_speech=melfilters(26)
