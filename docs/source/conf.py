# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html


import os
import sys

sys.path.append(os.path.abspath("../../src/main/python/"))
sys.path.append(os.path.abspath("../../gust_packages/radio_manager/src/"))
sys.path.append(os.path.abspath("../../gust_packages/cmr_manager/src/"))
sys.path.append(os.path.abspath("../../gust_packages/zed_manager/src/"))
sys.path.append(os.path.abspath("../../gust_packages/wsgi_apps/src/"))
sys.path.append(os.path.abspath("../../utilities/src/"))

sys.path.append(os.path.abspath("./packages_api/"))

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'GUST'
copyright = '2023, LAGER'
author = 'LAGER'
release = '2022'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.autosummary",
    "sphinx.ext.mathjax",
    "sphinx.ext.todo",
    "sphinx.ext.viewcode",
    "sphinxcontrib.apidoc",
]

templates_path = ['_templates']
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_logo = "images/gust_logo.svg"
html_show_sourcelink = False
html_baseurl = "https://github.com/drjdlarson/gust"