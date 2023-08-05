Cypress Common Modules
======================

This module is a common helper for all the other modules in cypress
project!

There are common\_helper, cypress\_base, cypress\_cache, kafka\_helper,
and logger\_helper.

1. How to install the latest cypress\_common package

   ::

       pip install cypress_common

2. How to install cypress\_common package with a sepcific version

   ::

       pip install cypress_common==<version_number>

3. How to import a class from cypress\_common module

   Ex) How to import the CypressCache from other projects:

   ::

       from cypress_common.cypress_cache import CypressCache
