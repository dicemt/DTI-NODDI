# DTI-NODDI
Daisuke Matsuyoshi (National Institute for Radiological Sciences ([QST-NIRS](https://www.qst.go.jp/site/qst-english/)) and [Araya, Inc.](https://www.araya.org/))

Implementation of diffusion tensor image based neurite orientation dispersion and density imaging (DTI-NODDI) written in Python.


# Installation
## Python
- Python 3.7 or higher

## Package dependencies
- numpy (>=1.16.5)
- scipy (>=1.3.1)
- nibabel (>=3.1.0)


# Usage

## Basic usage
```bash
dti_noddi_fit.py <b-value> --L1 <L1 file> --L2 <L2 file> --L3 <L3 file> [options]
dti_noddi_fit.py <b-value> --FA <FA file> --MD <MD file> [options]
```

## Output
Output parameter maps in NIfTI-1 format (`*.nii.gz`), including:
1. Orientation dispersion index ( `DTINODDI_ODI` )
1. Intracellular volume fraction, aka neurite density index ( `DTINODDI_ICVF` )
1. Fractinoal anisotropy ( `DTINODDI_FA` ) *Using standard DTI.*
1. Mean diffusivity ( `DTINODDI_MD` ) *Using standard DTI, but correct for b-value.*

## Examples
- Using eigenvalue files (if b-value is 2000 s/mm-2)
    - Will output DTINODDI_ODI, DTINODDI_ICVF, DTINODDI_FA, and DTINODDI_MD files.
    
```bash
$ python dti_noddi_fit.py 2000 --L1 L1.nii.gz --L2 L2.nii.gz --L3 L3.nii.gz
```

- Using FA and MD files (if b-value is 1000 s/mm-2)
    - Will output DTINODDI_ODI, and DTINODDI_ICVF files.
    
```bash
$ python dti_noddi_fit.py 1000 --FA FA.nii.gz --MD MD.nii.gz
```

- [options] `--mask`
  - Applying a binary mask image
  
```bash
$ python dti_noddi_fit.py 2000 --L1 L1.nii.gz --L2 L2.nii.gz --L3 L3.nii.gz --mask DWI_nodif_brain_mask.nii.gz
```

- [options] `--MK`
  - Heuristic correction for diffusional kurtosis (using mean kurtosis)
  
```bash
$ python dti_noddi_fit.py 2000 --L1 L1.nii.gz --L2 L2.nii.gz --L3 L3.nii.gz --MK MK.nii.gz
```

# License
The DTI-NODDI is free but copyright software, distributed under the terms of the [GNU Affero General Public License v3.0](https://choosealicense.com/licenses/agpl-3.0/).

Copyright (C) 2020 Daisuke Matsuyoshi

This program is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License along with this program.  If not, see <https://www.gnu.org/licenses/>.
