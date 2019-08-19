# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# http://www.sphinx-doc.org/en/master/config

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#

import sys

sys.path.append('..')

import jinete as jit

# -- Project information -----------------------------------------------------


project = jit.__name__
copyright = '2019, Sergio García Prado'
author = 'Sergio García Prado'
release = jit.__version__

# -- General configuration ---------------------------------------------------

master_doc = 'index'

extensions = [
    'sphinxcontrib.apidoc',
    'sphinx.ext.autodoc',
    'sphinx.ext.coverage',
    'sphinx.ext.mathjax',
    'sphinx.ext.viewcode',
    'sphinx.ext.intersphinx',
    'sphinx.ext.todo',
    'sphinx.ext.doctest',
    'sphinx_rtd_theme',
]

templates_path = ['_templates']

exclude_patterns = []

# -- Options for HTML output -------------------------------------------------

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

# -- Extension configuration -------------------------------------------------

## "intersphinx" extension
intersphinx_mapping = {'https://docs.python.org/': None}

## "todo" extension
todo_include_todos = True

## "apidoc" extension
apidoc_module_dir = '../../{}'.format(jit.__name__)
apidoc_output_dir = 'api_reference'
apidoc_separate_modules = True
autoclass_content = 'both'
apidoc_toc_file = False
apidoc_module_first = True
apidoc_extra_args = ['--force', '--implicit-namespaces']
