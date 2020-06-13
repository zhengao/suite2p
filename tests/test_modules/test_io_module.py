"""
Tests for the Suite2p IO module
"""

import numpy as np
from pathlib import Path
from tifffile import imread
from suite2p import io


def get_binary_file_data(op):
    # Read in binary file's contents as int16 np array
    binary_file_data = np.fromfile(
        str(Path(op['save_path0']).joinpath('suite2p', 'plane0', 'data.bin')),
        np.int16
    )
    return np.reshape(binary_file_data, (-1, op['Ly'], op['Lx']))


def test_tiff_reconstruction_from_binary_file(default_ops):
    """
    Tests to see if tif generated by tiff_to_binary and write_tiff matches test tif.
    """
    op = io.tiff_to_binary(default_ops)[0]
    output_data = get_binary_file_data(op)
    # Make sure data in matrix is nonnegative
    assert np.all(output_data >= 0)
    io.write_tiff(output_data, op, 0, True)
    reconstructed_tiff_data = imread(
        str(Path(default_ops['save_path0']).joinpath('suite2p', 'plane0', 'reg_tif', 'file000_chan0.tif'))
    )
    # Compare to our test data
    prior_data = imread(
        str(Path(default_ops['data_path'][0]).joinpath('1plane1chan', 'suite2p', 'test_write_tiff.tif'))
    )
    assert np.array_equal(reconstructed_tiff_data, prior_data)


def test_h5_to_binary_nonnegative_output(default_ops):
    """
    Tests if the binary file produced by h5_to_binary contains nonnegative data.
    """
    default_ops['h5py'] = Path(default_ops['data_path'][0]).joinpath('input.h5')
    default_ops['data_path'] = []
    op = io.h5py_to_binary(default_ops)[0]
    output_data = get_binary_file_data(op)
    assert np.all(output_data >= 0)