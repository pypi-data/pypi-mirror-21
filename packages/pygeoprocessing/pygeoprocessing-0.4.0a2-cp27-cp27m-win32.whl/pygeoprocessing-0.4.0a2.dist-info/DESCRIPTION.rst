under the following conditions and terms:

Copyright (c) 2014, The Natural Capital Project

All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are
met:

 * Redistributions of source code must retain the above copyright
   notice, this list of conditions and the following disclaimer.

 * Redistributions in binary form must reproduce the above copyright
   notice, this list of conditions and the following disclaimer in the
   documentation and/or other materials provided with the
   distribution.

 * Neither the name of the Natural Capital Project nor the names of
   its contributors may be used to endorse or promote products derived
   from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
"AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

Description: .. default-role:: code
        
        About PyGeoprocessing
        =====================
        
        |test_coverage_badge|
        
        .. |test_coverage_badge| image:: http://builds.naturalcapitalproject.org:9931/jenkins/c/http/builds.naturalcapitalproject.org/job/test-pygeoprocessing/label=GCE-windows-1/
          :target: http://builds.naturalcapitalproject.org/job/test-pygeoprocessing/label=GCE-windows-1
        
        
        PyGeoprocessing is a Python/Cython based library that provides a set of commonly
        used raster, vector, and hydrological operations for GIS processing.  Similar
        functionality can be found in ArcGIS/QGIS raster algebra, ArcGIS zonal
        statistics, and ArcGIS/GRASS/TauDEM hydrological routing routines.
        
        PyGeoprocessing was developed at the Natural Capital Project to create a
        programmable, open source, and free GIS processing library to support the
        ecosystem service software InVEST.  PyGeoprocessing's design prioritizes
        computation and memory efficient runtimes, easy installation and cross
        compatibility with other open source and proprietary software licenses, and a
        simplified set of orthogonal GIS processing routines that interact with GIS data
        via filename. Specifically the functionally provided by PyGeoprocessing includes
        
        * programmable raster algebra routine (vectorize_datasets)
        * routines for simplified raster creation and statistics
        * integration with vector based geometry in many of the routines
        * a simplified hydrological routing library including,
           + d-infinity flow direction
           + support for plateau drainage
           + weighted and unweighted flow accumulation
           + and weighted and unweighted flow distance
        
        Dependencies include
        
        * cython>=0.20.2
        * numpy>=1.8.2
        * scipy>=0.13.3
        * shapely>=1.3.3
        * gdal>=1.10.1
        
        Installing PyGeoprocessing
        ==========================
        
        .. code-block:: console
        
            $ pip install pygeoprocessing
        
        
        If you `import pygeoprocessing` and see a `ValueError: numpy.dtype has the
        wrong size, try recompiling`, this is the result of a version compatibility
        issue with the numpy ABI in the precompiled pygeoprocessing binaries.
        The solution is to recompile pygeoprocessing on your computer:
        
        .. code-block:: console
        
            $ pip uninstall -y pygeoprocessing
            $ pip install pygeoprocessing --no-deps --no-binary :all:
        
        
Keywords: gis pygeoprocessing
Platform: UNKNOWN
Classifier: Intended Audience :: Developers
Classifier: Development Status :: 5 - Production/Stable
Classifier: Intended Audience :: Science/Research
Classifier: Natural Language :: English
Classifier: Operating System :: MacOS :: MacOS X
Classifier: Operating System :: Microsoft
Classifier: Operating System :: POSIX
Classifier: Programming Language :: Python :: 2 :: Only
Classifier: Topic :: Scientific/Engineering :: GIS
