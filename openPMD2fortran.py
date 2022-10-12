"""
Copyright 2022, openPMD2fortran contributors
Authors: Jian Fuh Ong
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
from turtle import back
from openpmd_viewer import OpenPMDTimeSeries
import numpy as np
from scipy.io import FortranFile

def openPMD2fortran(run_directory,species,iteration,select=None,backend='h5py'):
    """
        Parameters
        ----------
        run_directory : string
            The path to the directory where the output of openPMD are.
            i.e. PIConGPU run_directory = "your_output_path/your_file/simOutput/h5/"
        
        species : string
            The particle species in PIC simulation
        
        iteration : integer
            The iteration of the file to convert
            i.e. iteration = 189600

        backend: string
            Backend to be used for data reading. Can be `openpmd-api`
            or `h5py`. Default is `h5py`
        
        example:
        select = {uy : [148:150]}
        openPMD2fortran('/media/ong/WORKDIR21/betatron0047_1/simOutput/h5/particles/','e_highGamma', 189600, select)
        """
    
    ts = OpenPMDTimeSeries(run_directory,backend=backend)

    x, y, z, ux, uy, uz, w= ts.get_particle(
        var_list=['x','y','z','ux','uy','uz','w'],
        iteration=iteration, 
        species=species,
        select=select,
    )
    dimensions = x.shape[-1]
    print("Writing fortran file for iteration:",iteration, "; having array shape of :", dimensions)
    f = FortranFile(rf'{run_directory}/restrt{iteration}.dat', 'w')
    f.write_record(iteration)
    f.write_record(dimensions)
    f.write_record(x)
    f.write_record(y)

if __name__ == "__main__":
    select = {'uy' : [148,150]}
    openPMD2fortran('/media/ong/WORKDIR21/betatron0047_1/simOutput/h5/particles/',species='e_highGamma', iteration=189600, select=select)


