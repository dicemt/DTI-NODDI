#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2020 Daisuke Matsuyoshi
# Released under the GNU AGPLv3 
# https://opensource.org/licenses/AGPL-3.0

"""
Run DTI-NODDI
"""

__author__ = "Daisuke Matsuyoshi @dicemt"

import argparse
import dti_noddi_api
import sys
from dti_noddi import isnumber

parser = argparse.ArgumentParser(description="""

usage:

$ noddi_dti_fit.py 2000 --L1 DWI_L1.nii.gz --L2 DWI_L2.nii.gz --L3 DWI_L3.nii.gz
$ noddi_dti_fit.py 1000 --FA DWI_FA.nii.gz --MD DWI_MD.nii.gz

""",
                                 formatter_class=argparse.RawDescriptionHelpFormatter)

parser.add_argument("bval", help="b value", metavar="b_value")
parser.add_argument("--L1", help="DTI L1 file", metavar="L1_file", default=None)
parser.add_argument("--L2", help="DTI L2 file", metavar="L2_file", default=None)
parser.add_argument("--L3", help="DTI L3 file", metavar="L3_file", default=None)
parser.add_argument("--FA", help="DTI FA file", metavar="FA_file", default=None)
parser.add_argument("--MD", help="DTI MD file", metavar="MD_file", default=None)
parser.add_argument("--MK", help="DTI MK file", metavar="MK_file", default=1)
parser.add_argument("-m", "--mask", help="mask_file", default=None)


args = parser.parse_args()
bval = args.bval
mask = args.mask
MK = args.MK

import time
startTime = time.time()

if args.L1:
    print("Using eigenvalues")
    if isnumber(str(MK)):
        MK = float(MK)
    dti_noddi_api.dti_noddi_eigenvalue(float(bval), args.L1, args.L2, args.L3, MK=MK, mask = mask)
elif args.FA:
    print("Using FA and MD")
    dti_noddi_api.dti_noddi_famd(float(bval), FA=args.FA, MD=args.MD, mask = mask)
    
print("----- %s seconds -----" % (time.time() - startTime))
