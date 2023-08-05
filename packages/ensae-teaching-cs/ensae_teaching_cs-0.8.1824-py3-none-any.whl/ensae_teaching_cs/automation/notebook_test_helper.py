#-*- coding: utf-8 -*-
"""
@file
@brief Some automation helpers to test notebooks and check they are still working fine.
"""
import os
import sys
import shutil
from pyquickhelper.loghelper import noLOG
from pyquickhelper.ipythonhelper.notebook_helper import install_python_kernel_for_unittest
from pyquickhelper.ipythonhelper import run_notebook


def ls_notebooks(subfolder):
    """
    list the notebooks in a particular subfolder

    @param      subfolder   subfolder (related to this module)
    @return                 list of files
    """
    this = os.path.abspath(os.path.dirname(__file__))
    docnote = os.path.join(
        this,
        "..",
        "..",
        "..",
        "_doc",
        "notebooks",
        subfolder)
    notes = [
        os.path.normpath(
            os.path.join(
                docnote,
                _)) for _ in os.listdir(docnote)]

    keepnote = []
    for i, note in enumerate(notes):
        ext = os.path.splitext(note)[-1]
        if ext != ".ipynb":
            continue
        keepnote.append(note)
    return keepnote


def get_additional_paths():
    """
    returns a list of paths to add before running the notebooks,
    paths to pyquickhelper, pyensae, pymmails

    @return             list of paths
    """
    import pyquickhelper
    import pyensae
    import pymmails
    import pymyinstall
    import jyquickhelper
    addpath = [os.path.dirname(pyquickhelper.__file__),
               os.path.dirname(pyensae.__file__),
               os.path.dirname(pymmails.__file__),
               os.path.dirname(pymyinstall.__file__),
               os.path.dirname(jyquickhelper.__file__),
               os.path.join(os.path.abspath(os.path.dirname(__file__)), ".."),
               ]
    addpath = [os.path.normpath(os.path.join(_, "..")) for _ in addpath]
    return addpath


def clean_function_1a(code):
    """
    function which clean cells when unittesting notebooks 1A

    @param      code        cell content
    @return                 modified code
    """
    code = code.replace(
        'run_cmd("exemple.xlsx"',
        'skip_run_cmd("exemple.xlsx"')

    skip = ["faire une chose avec la probabilité 0.7",
            "# déclenche une exception",
            "# pour lancer Excel",
            "for k in list_exercice_1 :",
            "return ....",
            "return [ .... ]",
            "def __init__(self, ...) :",
            "if random.random() <= 0.7 :",
            "dictionnaire_depart.items() [0]",
            "iterateur(0,10) [0]",
            "# ...... à remplir",
            'String.Join(",", a.Select(c=>c.ToString()).ToArray())',
            "# elle n'existe pas encore",
            "from ggplot import *",
            "print(tab[i] + tab[i+1])",
            "if n = 1:",
            "clenche une exception",
            'y = "a" * 3 + 1',
            # ggplot calls method show and it opens window blocking the offline
            # execution
            ]
    rep = [("# ...", "pass # "),
           ("%timeit", "#%timeit"),
           ]
    spl = ["# ......",
           "# elle n'existe pas encore",
           ]

    for s in skip:
        if s in code:
            return ""

    for s in spl:
        if s in code:
            code = code.split(s)[0]

    for s in rep:
        code = code.replace(s[0], s[1])

    return code


def execute_notebooks(folder, notebooks, filter, clean_function=None,
                      fLOG=noLOG, deepfLOG=noLOG, replacements=None):
    """
    execute a list of notebooks

    @param      folder          folder
    @param      notebooks       list of notebooks
    @param      filter          function which validates the notebooks to test (True means will be tested)
    @param      clean_function  cleaning function to apply to the code before running it
    @param      fLOG            logging function
    @param      deepfLOG        logging function used to run the notebook
    @param      replacements    replacements
    @return                     dictionary { notebook_file: (isSuccess, outout) }

    The signature of function ``filter`` is::

        def filter( i, filename) : return True or False

    """

    def valid_cell(cell):
        if "%system" in cell:
            return False
        if "df.plot(...)" in cell:
            return False
        if 'df["difference"] = ...' in cell:
            return False
        if 'remote_open' in cell:
            return None
        if 'blobpassword' in cell:
            return None
        return True

    addpath = get_additional_paths()
    kernel_name = None if "travis" in sys.executable else install_python_kernel_for_unittest(
        "ensae_teaching_cs")
    results = {}
    tested = []
    for i, note in enumerate(notebooks):
        if filter(i, note):
            fLOG("******", i, os.path.split(note)[-1])
            tested.append(note)
            outfile = os.path.join(folder, "out_" + os.path.split(note)[-1])
            try:
                stat, out = run_notebook(note, working_dir=folder, outfilename=outfile,
                                         additional_path=addpath, valid=valid_cell,
                                         clean_function=clean_function, fLOG=deepfLOG,
                                         kernel_name=kernel_name, replacements=replacements)
                if not os.path.exists(outfile):
                    raise FileNotFoundError(outfile)
                results[note] = (True, stat, out)
            except Exception as e:
                results[note] = (False, None, e)
    if len(tested) == 0:
        raise Exception("no notebook were tested with '{0}'".format(filter))
    return results


def unittest_raise_exception_notebook(res, fLOG):
    """
    same code for all unit tests

    @param      res     output of @see fn execute_notebooks
    """
    assert len(res) > 0
    fails = [(os.path.split(k)[-1], ) + v
             for k, v in sorted(res.items()) if not v[0]]
    for f in fails:
        fLOG(f)
    if len(fails) > 0:
        raise fails[0][-1]
    for k, v in sorted(res.items()):
        fLOG("final", os.path.split(k)[-1], v[0], v[1])


def copy_data_file(notebook_folder, filename, dest, fLOG=noLOG):
    """
    copy a data file from a notebook folder to the current folder

    @param      notebook_folder     notebook_folder
    @param      filename            filename or list of file names
    @param      destination         destination folder
    @parm       fLOG                logging function
    @return                         copied files
    """
    if isinstance(filename, list):
        return [copy_data_file(notebook_folder, f, dest) for f in filename]
    else:
        src = os.path.abspath(os.path.join(os.path.dirname(
            __file__), "..", "..", "..", "_doc", "notebooks", notebook_folder, filename))
        if not os.path.exists(src):
            raise FileNotFoundError(src)
        if not os.path.exists(dest):
            raise FileNotFoundError(dest)
        shutil.copy(src, dest)
        res = os.path.join(dest, os.path.split(src)[-1])
        fLOG("copy", res)
        return res
