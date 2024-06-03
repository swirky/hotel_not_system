# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
import os
import sys
sys.path.insert(0, os.path.abspath('../src'))


html_theme_path = ['sphinx_rtd_theme.get_html_theme_path()']
html_theme = 'sphinx_rtd_theme'

project = 'System zgloszen hotelowych'
copyright = '2024, Marek Świerk, Dominik Kozioł, Patryk Grębosz'
author = 'Marek Świerk, Dominik Kozioł, Patryk Grębosz'
release = '1'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['sphinx.ext.todo','sphinx.ext.viewcode','sphinx.ext.autodoc']
todo_include_todos= True

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_static_path = ['_static']
