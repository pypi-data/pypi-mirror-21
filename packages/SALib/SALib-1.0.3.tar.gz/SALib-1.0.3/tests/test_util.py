from __future__ import division

import os

from nose.tools import raises, with_setup
from numpy.testing import assert_equal, assert_allclose

import numpy as np
import tempfile
import pytest

from SALib.util import read_param_file, scale_samples, unscale_samples, \
                   compute_groups_matrix

def make_temporary_file():
    """ Returns a temporary file name

    Returns
    =========
    openfile.name : str
        Name of the temporary file
    """
    with tempfile.NamedTemporaryFile() as openfile:
        return openfile.name

@pytest.fixture(scope='function')
def setup_function():
    filename = make_temporary_file()
    with open(filename, "w+") as ofile:
        ofile.write("Test1 0.0 100.0\n")
        ofile.write("Test2 5.0 51.0\n")
    return filename

@pytest.fixture(scope='function')
def setup_param_file_group_dist():
    filename = make_temporary_file()
    with open(filename, "w") as ofile:
        ofile.write("Test1 0.0 100.0 Group1 unif\n")
        ofile.write("Test2 5.0 51.0 Group1 triang\n")
        ofile.write("Test3 10.0 1.0 Group2 norm\n")
    return filename

@pytest.fixture(scope='function')
def setup_csv_param_file_with_whitespace_in_names():
    filename = make_temporary_file()
    with open(filename, "w") as ofile:
        ofile.write("Test 1,0.0,100.0\n")
        ofile.write("Test 2,5.0,51.0\n")
    return filename

@pytest.fixture(scope='function')
def setup_tab_param_file_with_whitespace_in_names():
    filename = make_temporary_file()
    with open(filename, "w") as ofile:
        ofile.write("Test 1\t0.0\t100.0\n")
        ofile.write("Test 2\t5.0\t51.0\n")
    return filename

@pytest.fixture(scope='function')
def setup_csv_param_file_with_whitespace_in_names_comments():
    filename = make_temporary_file()
    with open(filename, "w") as ofile:
        ofile.write("# Here is a comment\n")
        ofile.write("'Test 1',0.0,100.0\n")
        ofile.write("'Test 2',5.0,51.0\n")
    return filename

@with_setup(setup_function)
def test_readfile():
    '''
    Tests a standard parameter file is read correctly
    '''

    filename = setup_function()
    pf = read_param_file(filename)

    assert_equal(pf['bounds'], [[0, 100], [5, 51]])
    assert_equal(pf['num_vars'], 2)
    assert_equal(pf['names'], ['Test1', 'Test2'])


@with_setup(setup_param_file_group_dist)
def test_readfile_group_dist():
    '''
    Tests a parameter file with groups and distributions is read correctly
    '''
    filename = setup_param_file_group_dist()
    pf = read_param_file(filename)
    assert_equal(pf['bounds'], [[0, 100], [5, 51], [10, 1]])
    assert_equal(pf['num_vars'], 3)
    assert_equal(pf['names'], ['Test1', 'Test2', 'Test3'])
    assert_equal(pf['groups'], ['Group1', 'Group1', 'Group2'])
    assert_equal(pf['dists'], ['unif', 'triang', 'norm'])


@with_setup(setup_csv_param_file_with_whitespace_in_names)
def test_csv_readfile_with_whitespace():
    '''
    A comma delimited parameter file with whitespace in the names
    '''

    filename = setup_csv_param_file_with_whitespace_in_names()
    pf = read_param_file(filename)

    assert_equal(pf['bounds'], [[0, 100], [5, 51]])
    assert_equal(pf['num_vars'], 2)
    assert_equal(pf['names'], ['Test 1', 'Test 2'])


@with_setup(setup_tab_param_file_with_whitespace_in_names)
def test_tab_readfile_with_whitespace():
    '''
    A tab delimited parameter file with whitespace in the names
    '''

    filename = setup_tab_param_file_with_whitespace_in_names()
    pf = read_param_file(filename)

    assert_equal(pf['bounds'], [[0, 100], [5, 51]])
    assert_equal(pf['num_vars'], 2)
    assert_equal(pf['names'], ['Test 1', 'Test 2'])


@with_setup(setup_csv_param_file_with_whitespace_in_names_comments)
def test_csv_readfile_with_comments():
    '''
    '''

    filename = setup_csv_param_file_with_whitespace_in_names_comments()

    pf = read_param_file(filename)

    print(pf['bounds'], pf['num_vars'], pf['names'])

    assert_equal(pf['bounds'], [[0, 100], [5, 51]])
    assert_equal(pf['num_vars'], 2)
    assert_equal(pf['names'], ['Test 1', 'Test 2'])


# Test scale samples
def test_scale_samples():
    '''
    Simple test to ensure that samples are correctly scaled
    '''

    params = np.arange(0, 1.1, 0.1).repeat(2).reshape((11, 2))

    bounds = [[10, 20], [-10, 10]]

    desired = np.array([np.arange(10, 21, 1), np.arange(-10, 12, 2)], dtype=np.float).T
    scale_samples(params, bounds)
    assert_allclose(params, desired, atol=1e-03, rtol=1e-03)

def test_unscale_samples():
    '''
    Simple test to unscale samples back to [0,1] range
    '''
    params = np.array([np.arange(10, 21, 1), np.arange(-10, 12, 2)], dtype=np.float).T
    bounds = [[10, 20], [-10, 10]]

    desired = np.arange(0, 1.1, 0.1).repeat(2).reshape((11, 2))
    unscale_samples(params, bounds)
    assert_allclose(params, desired, atol=1e-03, rtol=1e-03)


@raises(ValueError)
def test_scale_samples_upper_lt_lower():
    '''
    Raise ValueError if upper bound lower than lower bound
    '''
    params = np.array([[0, 0], [0.1, 0.1], [0.2, 0.2]])
    bounds = [[10, 9], [-10, 10]]
    scale_samples(params, bounds)


@raises(ValueError)
def test_scale_samples_upper_eq_lower():
    '''
    Raise ValueError if upper bound lower equal to lower bound
    '''
    params = np.array([[0, 0], [0.1, 0.1], [0.2, 0.2]])
    bounds = [[10, 10], [-10, 10]]
    scale_samples(params, bounds)


def test_compute_groups_from_parameter_file():
    '''
    Tests that a group file is read correctly
    '''
    actual_matrix, actual_unique_names = \
        compute_groups_matrix(['Group 1', 'Group 2', 'Group 2'], 3)

    assert_equal(actual_matrix, np.matrix('1,0;0,1;0,1', dtype=np.int))
    assert_equal(actual_unique_names, ['Group 1', 'Group 2'])
