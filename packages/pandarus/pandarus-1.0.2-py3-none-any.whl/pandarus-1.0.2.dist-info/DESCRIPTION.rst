Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

Redistributions of source code must retain the above copyright notice, this
list of conditions and the following disclaimer. 

Redistributions in binary form must reproduce the above copyright notice, 
this list of conditions and the following disclaimer in the documentation 
and/or other materials provided with the distribution.

Neither the name of ETH Zürich nor the names of its contributors may be used
to endorse or promote products derived from this software without specific
prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

Description: # Pandarus
        
        [![Build Status](https://travis-ci.org/cmutel/pandarus.svg?branch=master)](https://travis-ci.org/cmutel/pandarus) [![codecov](https://codecov.io/gh/cmutel/pandarus/branch/master/graph/badge.svg)](https://codecov.io/gh/cmutel/pandarus)
         [![Docs](https://readthedocs.org/projects/pandarus/badge/?version=latest)](http://pandarus.readthedocs.io/?badge=latest)
        
        Pandarus is a GIS software toolkit for regionalized life cycle assessment. It is designed to work with [brightway LCA framework](https://brightwaylca.org), [brightway2-regional](https://bitbucket.org/cmutel/brightway2-regional), and [Constructive Geometries](https://bitbucket.org/cmutel/constructive-geometries).
        
        For more information, see the [online documentation](https://pandarus.readthedocs.io/).
        
        Pandarus provides the following functionality:
        
        * Match two vector datasets, calculating the areas of each combination of features using the Mollweide projection.
        * Calculate the areas left out (present in one input file but not the other) from the aforementioned intersections calculation.
        * Calculate statistics such as min, mean, and max when overlaying a raster dataset with a vector dataset.
        * Normalize raster datasets, including use of compatible `nodata` values
        * Vectorization of raster datasets
        
        ## Requirements
        
        * [appdirs](https://pypi.python.org/pypi/appdirs)
        * [fiona](https://pypi.python.org/pypi/Fiona)
        * [numpy](http://www.numpy.org/)
        * [pyproj](https://pypi.python.org/pypi/pyproj)
        * [rasterio](https://github.com/mapbox/rasterio)
        * [rasterstats](https://pypi.python.org/pypi/rasterstats)
        * [Rtree](https://pypi.python.org/pypi/Rtree/)
        * [shapely](https://pypi.python.org/pypi/Shapely)
        
        ## Development
        
        Pandarus is developed by [Chris Mutel](https://chris.mutel.org/) as part of his work at the [Technology Assessment Group](https://www.psi.ch/ta/technology-assessment) at the Paul Scherrer Institut and previously at the [Ecological Systems Design group](http://www.ifu.ethz.ch/ESD/index_EN) at ETH Zürich.
        
        Source code is available on [GitHub](https://github.com/cmutel/pandarus).
        
Platform: UNKNOWN
Classifier: Development Status :: 5 - Production/Stable
Classifier: Intended Audience :: End Users/Desktop
Classifier: Intended Audience :: Developers
Classifier: Intended Audience :: Science/Research
Classifier: License :: OSI Approved :: BSD License
Classifier: Operating System :: MacOS :: MacOS X
Classifier: Operating System :: Microsoft :: Windows
Classifier: Operating System :: POSIX
Classifier: Programming Language :: Python
Classifier: Programming Language :: Python :: 3.5
Classifier: Programming Language :: Python :: 3 :: Only
Classifier: Topic :: Scientific/Engineering :: Mathematics
