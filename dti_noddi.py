#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2020 Daisuke Matsuyoshi
# Released under the GNU AGPLv3 
# https://opensource.org/licenses/AGPL-3.0

"""
Calculate DTI-NODDI parameters
"""

__author__ = "Daisuke Matsuyoshi @dicemt"

import numpy as np
from scipy import sqrt
from scipy import special
from scipy import optimize as opt

def correct_md(bval, L1, L2, L3, MK = 1.0):
    MD = (L1 + L2 + L3) / 3.0
    # Eq.B11
    MD2 = (np.power(L1,2) + np.power(L2,2) + np.power(L3,2)) / 5.0 + 2.0 * (L1*L2 + L1*L3 + L2*L3) / 15.0
    # Eq.B12, Eq.5
    corrMD = MD + bval / 6.0 * MD2 * MK
    return(corrMD)


def dti_fit(L1,L2,L3):
    MD = (L1+L2+L3)/3
    denom = np.sqrt( np.power((L1-MD),2) + np.power((L2-MD),2) + np.power((L3-MD),2) )
    numer = np.sqrt( np.power(L1,2) + np.power(L2,2) + np.power(L3,2) )
    FA = np.sqrt(1.5) * ( np.divide(denom, numer, out=np.zeros_like(denom), where=numer!=0) )
    return(FA,MD)


def md2icvf(MD):
    dwm,dgm,_ = diff_parameters()
    # Eq.2; Lampinen (2017) Eq.27 icvf = 1.0 - sqrt(1 - 1.5 * (1 - MD/dwm))
    icvf = 1.0 - sqrt(0.5 * (3 * MD / dwm - 1.0))
    # Errorneous voxels
    erricvf = np.logical_or( icvf.real < 0.0 , np.isnan(icvf) )
    overicvf = (icvf.real >= 1.0)
    icvf[erricvf] = 0.0
    icvf[overicvf] = 1.0
    mask = np.logical_or( MD.real <= 0.0, np.isnan(MD) )
    icvf[mask] = 0.0
    return(icvf.real)

def famd2tau(FA,MD):
    dwm,dgm,_ = diff_parameters()
    # Eq.3
    #tau = 1.0/3.0 * (1.0 + (4.0 / np.abs(dwm - MD))) * (FA * MD) / np.sqrt(3.0 - 2.0 * np.power(FA,2))
    tau = 1.0/3.0 * (1.0 + 4.0 * FA *(MD / np.abs(dwm-MD)) / np.sqrt(3.0 - 2.0 * np.power(FA,2)))
    # Errorneous voxels
    errtau = np.logical_or(tau.real <= 1.0/3.0, np.isnan(tau))
    overtau = np.logical_or(tau.real >= 1.0, np.abs(tau.imag) > 1e-10 )
    tau[errtau] = 0.0
    tau[overtau] = 1.0
    mask = np.logical_or(MD.real <= 0.0, np.isnan(MD))
    tau[mask] = 0.0
    return(tau.real)


def tau2odi(tau):
    dwm,dgm,_ = diff_parameters()
    odi = np.zeros_like(tau)
    # Errorneous voxels
    errtau = np.logical_or(tau <(1.0/3.0), tau > 1.0)
    odi[errtau] = -1.0
    maintau = tau[~errtau]
    mainodi = np.zeros_like(maintau)
    for i in range(maintau.size):
        f = lambda x : kappa2tau(odi2kappa(x)) - maintau[i]
        try:
            mainodi[i] = opt.brentq(f, dwm, 1.0)
        except:
            mainodi[i] = 0
    odi[~errtau]=mainodi
    odi[errtau]=0 # Exclude again with zero
    print(tau.shape)
    odi = odi.reshape(tau.shape)
    return(odi)


def kappa2tau(kappa):
    tau = np.zeros_like(kappa)
    outkappa = np.abs(kappa) < 1e-12
    # Eq.8 Zhang
    tau[~outkappa] = 0.5 * ( -1.0 / kappa[~outkappa] + 1.0 / (np.sqrt(kappa[~outkappa]) * dawson(np.sqrt(kappa[~outkappa]))) )
    tau[outkappa] = 1.0/3.0 # Lower limit
    return(tau)


def dawson(x):
    # Abramowitz and Stegun (1972)
    a = 0.5 * np.sqrt(np.pi) * np.exp(-np.power(x,2)) * special.erfi(x)
    return(a)


def odi2kappa(odi):
    kappa = np.max(1.0 / np.tan((odi*np.pi)/2.0),0)
    return(kappa)


def kappa2odi(kappa):
    odi = 2.0 / np.pi * np.arctan(1.0/kappa)
    return(odi)


def diff_parameters():
    dwm = 1.7e-3
    dgm = 1.1e-3
    diso = 3.0e-3
    return(dwm,dgm,diso)

def isnumber(string):
    try:
        float(string)
        return True
    except ValueError:
        return False

