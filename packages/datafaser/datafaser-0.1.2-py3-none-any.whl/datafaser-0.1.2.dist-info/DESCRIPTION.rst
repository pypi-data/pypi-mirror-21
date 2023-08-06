Datafaser
=========

Datafaser collects and generates data, then fills in templates to generate files.

Results of each phase are checked against data schemas and content descriptions.

Requirements
------------

 - Python 3.6

Setup
-----

    . setup

Testing
-------

    nosetests --with-coverage --cover-package=datafaser

Use
---

    . local/bin/activate
    python datafaser --help

For example, to output the schema of datafaser as yaml:

    python datafaser utilities/convert-json-to-yaml.yaml < datafaser/data/schema.json

Documentation
-------------

Ideas in doc folder are currently a bit out of date.



