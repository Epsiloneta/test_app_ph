EasyPH
--------

To install it in "debug mode" so that changes within this folder are automatically broadcasted to python use

    pip install -e .

To launch the GUI, just issue the command

    app_easy_ph

To build a source distribution use

    python setup.py sdist
    
to build a wheel use

    pip wheel --no-dist .

To build a universal wheel use 
  
     docker run -i -t -v `pwd`:/io quay.io/pypa/manylinux1_x86_64 /bin/bash

and inside the docker machine we can execute

    for PYBIN in /opt/python/*/bin; do
      echo ${PYBIN}
      if [[ "${PYBIN}" =~ ".*27.*" ]]; then
      echo "working";
      "${PYBIN}/pip" install pybind11
      "${PYBIN}/pip" wheel --no-deps /io/ -w wheelhouse/
      echo "Finished ${PYBIN}"
      else
      echo "ignored";
      fi
    done

    # Bundle external shared libraries into the wheels
    for whl in wheelhouse/*.whl; do
      auditwheel repair "$whl" -w /io/wheelhouse/
    done

Installing
---------------

Download .tar.gz

	pip install --upgrade easy_ph-0.1.tar.gz
    
Or
    pip install --upgrade easy_ph_long_file_name.whl
    
Running
---------------

Run app (from a Terminal):

	app_easy_ph 

Testing
-----------------

to test it in any system we can use

    nosetests easy_ph
    
provided that the python package nose is installed.

Inside the docker envirovment we can use

    PYBIN=/opt/python/cp27-cp27mu/bin/
    ${PYBIN}/pip install http://wheels.scipy.org/subprocess32-3.5.0-cp27-cp27mu-manylinux1_x86_64.whl
    ${PYBIN}/pip install matplotlib pandas networkx numpy scipy seaborn pybind11
    ${PYBIN}/pip install /io/

    ${PYBIN}/pip install nose
    ${PYBIN}nosetests easy_ph

