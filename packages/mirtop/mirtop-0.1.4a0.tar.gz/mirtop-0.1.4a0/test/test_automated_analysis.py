"""This directory is setup with configurations to run the main functional test.

Inspired in bcbio-nextgen code
"""
import os
import subprocess
import unittest
import shutil
import contextlib
import collections
import functools

from nose import SkipTest
from nose.plugins.attrib import attr
import yaml


@contextlib.contextmanager
def make_workdir():
    remove_old_dir = True
    dirname = os.path.join(os.path.dirname(__file__), "test_automated_output")
    if remove_old_dir:
        if os.path.exists(dirname):
            shutil.rmtree(dirname)
        os.makedirs(dirname)
    orig_dir = os.getcwd()
    try:
        os.chdir(dirname)
        yield dirname
    finally:
        os.chdir(orig_dir)

def expected_failure(test):
    """Small decorator to mark tests as expected failure.
    Useful for tests that are work-in-progress.
    """
    @functools.wraps(test)
    def inner(*args, **kwargs):
        try:
            test(*args, **kwargs)
        except Exception:
            raise SkipTest
        else:
            raise AssertionError('Failure expected')
    return inner

class AutomatedAnalysisTest(unittest.TestCase):
    """Setup a full automated analysis and run the pipeline.
    """
    def setUp(self):
        self.data_dir = os.path.join(os.path.dirname(__file__), "data", "automated")

    def _install_test_files(self, data_dir):
        """Download required sequence and reference files.
        """
        #       self._download_to_dir(url, dirname)

    def _download_to_dir(self, url, dirname):
        print dirname
        cl = ["wget", url]
        subprocess.check_call(cl)
        cl = ["tar", "-xzvpf", os.path.basename(url)]
        subprocess.check_call(cl)
        shutil.move(os.path.basename(dirname), dirname)
        os.remove(os.path.basename(url))

    @attr(complete=True)
    @attr(annotate=True)
    def test_srnaseq_annotation(self):
        """Run miraligner analysis
        """
        with make_workdir():
            clcode = ["mirtop",
                      "annotate",
                      "--sps", "hsa",
                      "--hairpin", "../../data/examples/annotate/hairpin.fa",
                      "--mirna", "../../data/examples/annotate/miRNA.str",
                      "-o", "test_out_mirs_fasta",
                      "../../data/examples/annotate/sim_isomir.sam"]
            print " ".join(clcode)
            subprocess.check_call(clcode)
