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
import matplotlib.pyplot as plt

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
    iteration=189600
    select = {'uy' : [148,150]}
    openPMD2fortran('/media/ong/WORKDIR21/betatron0047_1/simOutput/h5/particles/',species='e_highGamma', iteration=iteration, select=select)

    # The openPMD file is converted to fortran binary restrt{iteration}.dat. Fortran read this binary file then write the file pospic{iteration}.dat. The lines below plot this file.

    #x, y = np.loadtxt(rf"pospic{iteration}.dat",unpack=True,usecols=[0,1],dtype=np.float)

    #fig, ax = plt.subplots()

    #ax.plot(y*1e6, x*1e6, '.', color="black")
    
    #ax.set_ylabel(r"$x \,(\mathrm{\mu m})$")
    #ax.set_xlabel(r"$y \,(\mathrm{\mu m})$")

    # add watermark
    #ax.text(0.5, 0.5, 'LGED preliminary', transform=ax.transAxes,
    #    fontsize=20, color='gray', alpha=0.5,
    #    ha='center', va='center', rotation='30')
        
    #ax.set_ylim(ymin=0, ymax=78)
    #ax.set_xlim(xmin=5940,xmax=6005)
    #fig = plt.gcf()
    #fig.set_size_inches(3.4, 3.4/1.618)
    #plt.tight_layout()
    #fig.savefig(rf"particles{iteration}.png", dpi=300)



