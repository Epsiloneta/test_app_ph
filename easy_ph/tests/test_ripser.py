from unittest import TestCase

import easy_ph.ripser_wrapper_lib as ripser_lib
import os

import tempfile

# computation of the folder in which we are located
base_dir = os.path.normpath(os.path.join(
        os.path.dirname(__file__),
        '../..'))

class TestRipser(TestCase):
    def test_ripser_is_callable(self):
        # creation of a temporary file  name
        f = tempfile.NamedTemporaryFile(delete=False)
        f.close()
        tmp_file_path = f.name

        # creation of example input file
        in_f = tempfile.NamedTemporaryFile(delete=False)
        in_f.write('\n1\n1,2\n,1,2,2\n')
        in_f.close()
        in_tmp_file_path = in_f.name

        # actual call to ripser
        ripser_lib.ripser_call(['ripser',
            in_tmp_file_path],
            tmp_file_path)

        # read the output file
        x = open(tmp_file_path,'r').read()

        # check if the file is not empty
        self.assertTrue('[0,' in x) 

        # we remove the temporal file
        os.remove(tmp_file_path)

        