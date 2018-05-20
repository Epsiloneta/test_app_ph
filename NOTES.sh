mkdir teixi
cd teixi/

# Create virtual env
mkvirtualenv test_app_1
workon test_app_1

# Get code
git clone https://teixi@bitbucket.org/epsilon1987/easy_ph.git
cd easy_ph
git checkout package

# Build wheel
pip install pybind11
pip wheel --no-deps .

# Install wheel
pip install --upgrade easy_ph-0.1-cp27-cp27mu-linux_x86_64.whl

# Launch tests
python setup.py test

# Launch app
app_easy_ph

# Destroy virtualenv
deactivate
rmvirtualenv test_app_1
