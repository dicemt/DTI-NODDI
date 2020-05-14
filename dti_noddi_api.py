#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2020 Daisuke Matsuyoshi
# Released under the GNU AGPLv3 
# https://opensource.org/licenses/AGPL-3.0

"""
API for DTI-NODDI
"""

__author__ = "Daisuke Matsuyoshi @dicemt"

import os
import os.path
import re
import numpy as np
import nibabel as nib
from dti_noddi import correct_md, dti_fit, md2icvf, famd2tau, tau2odi, kappa2tau, dawson, odi2kappa, diff_parameters, isnumber

def dti_noddi_eigenvalue(bval, L1, L2, L3, MK = 1, mask = None):
    # Files paths
    L1 = os.path.abspath(os.path.expanduser(L1))
    L2 = os.path.abspath(os.path.expanduser(L2))
    L3 = os.path.abspath(os.path.expanduser(L3))
    nam,ext = os.path.basename(L1).split(os.extsep, 1)
    nam = re.sub('_\S+','',nam)
    pth = os.path.dirname(L1)
    newdir = pth + "/DTINODDI/"
    try:
        os.mkdir(newdir)
    except FileExistsError:
        pass
    
    # Load data
    L1data,header,affine = load_nifti(L1)
    print("b-value = %g" % bval)
    print(L1data.shape)
    L2data,_,_ = load_nifti(L2)
    L3data,_,_ = load_nifti(L3)
        
    # DTI fit
    print("-> FA")
    FA,_ = dti_fit(L1data,L2data,L3data)

    # MD correction
    print("-> corrected MD")
    if isnumber(str(MK)):
        print('MK = %g' % MK)
        MD = correct_md(bval,L1data,L2data,L3data,MK)
    elif os.path.isfile(str(MK)):
        print('Using MK: %s' % MK)
        MKdata,_,_ = load_nifti(MK)
        MD = correct_md(bval,L1data,L2data,L3data,MKdata)
        
    # ICVF
    print("-> ICVF")
    ICVF=md2icvf(MD)

    # ODI
    print("-> ODI")
    tauV = famd2tau(FA,MD)
    ODI = tau2odi(tauV)
    
    # Save
    save_nifti(FA, header, affine, mask, nam = "FA", pth = newdir)
    save_nifti(MD, header, affine, mask, nam = "MD", pth = newdir)
    save_nifti(ODI, header, affine, mask, nam = "ODI", pth = newdir)
    save_nifti(ICVF, header, affine, mask, nam = "ICVF", pth = newdir)

def dti_noddi_famd(bval, FA, MD, mask = None):
    # Files paths
    FA = os.path.abspath(os.path.expanduser(FA))
    MD = os.path.abspath(os.path.expanduser(MD))
    nam,ext = os.path.basename(FA).split(os.extsep, 1)
    nam = re.sub('_\S+','',nam)
    pth = os.path.dirname(FA)
    newdir = pth + "/DTINODDI/"
    try:
        os.mkdir(newdir)
    except FileExistsError:
        pass

    # Load data
    FAdata,header,affine = load_nifti(FA)
    print("b-value = %g" % bval)
    print(FAdata.shape)
    MDdata,_,_ = load_nifti(MD)

    # ICVF
    print("-> ICVF")
    ICVF=md2icvf(MDdata)

    # ODI
    print("-> ODI")
    tauV = famd2tau(FAdata,MDdata)
    ODI = tau2odi(tauV)

    # Save
    save_nifti(ODI, header, affine, mask, nam="ODI", pth = newdir)
    save_nifti(ICVF, header, affine, mask, nam="ICVF", pth = newdir)
    

def load_nifti(mrifile):
    img = nib.load(mrifile)
    try:
        imgdata = img.get_fdata()
    except:
        imgdata = img.get_data()
    header = img.header.copy()
    return(imgdata,header,img.affine)

def save_nifti(imgdata, header, affine, mask=None, nam=None, pth=None):
    # Apply mask
    from dipy.segment.mask import applymask
    if not mask:
        data = imgdata
        print('Not found mask image. Using implicit mask instead.')
    elif os.path.isfile(mask):
        mask = nib.load(mask)
        try:
            maskdata = mask.get_fdata()
        except:
            maskdata = mask.get_data()
        print('Applying mask to %s' % nam)
        data = applymask(imgdata,maskdata)
    else:
        data = imgdata
        print('Not found mask image. Using implicit mask instead.')
        
    # Modify header
    header['descrip'] = "DTI-NODDI " + nam
    # Save nifti
    newImg = nib.Nifti1Image(data.astype(np.float64), affine, header=header)
    nib.save(newImg, pth + "DTINODDI_" + nam + '.nii.gz')
