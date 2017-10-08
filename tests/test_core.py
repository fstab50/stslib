"""
Summary:
    Tests for stsAval core.py module

Test Framework: pytest

Args:
    :type
    :param

Useage:
    import json, sys
    sys.path.insert(0, '..')
    from stsAval import core

    source_a = './assets_core/awscli.reference'        # input file
    source_b = './assets_core/parsed.reference'        # ouput file
    def setup():
        r_obj = generate_reference_object(source_b)
        # create stsAval object, parse the test input file (awscli_reference)
        b = source_b.split('/')[2]
        sts_obj = core.StsCore(role_file=source_a, output_file=b)
        # set instance attribute for reuse
        target = json.dumps(sts_obj.profiles, indent=2, sort_keys=True)
        return r_obj, target
    r_obj_b, target_b = setup()
"""
import sys

sys.path.insert(0,'..')        # required to import modules

import json
import configparser
import pytest
import inspect
import logging
from stsAval import core
from stsAval.statics import __version__

__tracebackhide__ = False

# setup std logging
logger = logging.getLogger(__version__)
s_handler = logging.StreamHandler()
s_formatter = logging.Formatter('%(pathname)s - %(name)s - [%(levelname)s]: %(message)s')
s_handler.setFormatter(s_formatter)
logger.setLevel(logging.DEBUG)

source_a = './assets_core/awscli.reference'        # input file
source_b = './assets_core/parsed.reference'        # ouput file


class TestParsing():
    """
    validate core module for ability to accurately parse role credential files
    """
    def setup(self):
        r_obj, pp = self.generate_reference_object(source_b)
        # create stsAval object, parse the test input file (awscli_reference)
        b = source_b.split('/')[2]
        sts_obj = core.StsCore(role_file=source_a, output_file=b)
        # set instance attribute for reuse
        target = sts_obj.profiles
        target_pp = json.dumps(sts_obj.profiles, indent=2, sort_keys=True)
        return r_obj, target

    def ordered(self, dict_obj):
        if isinstance(dict_obj, dict):
            return sorted((k, self.ordered(v)) for k, v in dict_obj.items())
        if isinstance(dict_obj, list):
            return sorted(self.ordered(x) for x in dict_obj)
        else:
            return dict_obj

    @pytest.fixture(scope='session')
    def generate_reference_object(self, fname):
        """
        fixture to gen reference output file asset when a awscli local config
        file is parsed by stsAval
        """
        try:
            handle = open(fname, 'r')
            file_obj = handle.read()
            reference = json.loads(file_obj)
            reference_pp = json.dumps(reference, indent=2, sort_keys=True)
        except OSError as e:
            print('%s: Problem importing reference file object: %s' %
                (inspect.stack()[0][3], str(fname)))
            raise
        except TypeError:
            # fname is already json object, not file-type object
            reference = fname
            reference_pp = json.dumps(fname, indent=2, sort_keys=True)
        return reference, reference_pp

    def test_01_length(self):
        """
        validate awscli ini files are parsed correctly by benchmark to reference
        file asset
        """
        __tracebackhide__ = False
        # retrieve reference object
        r_object_b, pp = self.generate_reference_object(source_b)
        print('\nr_object_b is:\n')
        print(pp)
        # create stsAval object, parse the test input file (awscli_reference)
        b = source_b.split('/')[2]
        sts_obj = core.StsCore(role_file=source_a, output_file=b)
        self.target_object_b, pp = self.generate_reference_object(sts_obj.profiles)
        print('\nsts_obj is:\n')
        print(pp)
        # validate
        assert len(self.target_object_b) == len(r_object_b)

    def test_02_key_content(self):
        """ compares parsed content for accuracy against a reference set """
        __tracebackhide__ = False
        r_object_b, target_object_b = self.setup()
        #
        assert self.ordered(r_object_b) == self.ordered(target_object_b)


    """
    def test_N(self):
        #__tracebackhide__ = True
        pytest.fail("%s: not yet configured" % inspect.stack()[0][3])

    def test_stub(x):
        __tracebackhide__ = True
        if not hasattr(x, "config"):
            pytest.fail("not configured: %s" %(x,))
    """
