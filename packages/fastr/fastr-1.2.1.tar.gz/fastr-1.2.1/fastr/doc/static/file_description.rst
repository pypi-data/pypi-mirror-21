Resource File Formats
=====================

This chapter describes the various files fastr uses. The function and format
of the files is described allowing the user to configure fastr and add
DataTypes and Tools.

.. _config-file:

Config file
-----------

Fastr reads the config files from the following locations by default (in order):

* ``$FASTRHOME/config.py``
* ``~/.fastr/config.py``

Reading a new config file change or override settings, making the last config
file read have the highest priority. All settings have a default value, making
config files and all settings within optional.

Example config file
^^^^^^^^^^^^^^^^^^^

Here is a minimal config file::

  # Enable debugging output
  debug = False

  # Define the path to the tool definitions
  tools_path = ['/path/to/tools',
                '/path/to/other/tools'] + tools_path
  types_path = ['/path/to/datatypes',
                '/path/to/other/datatypes'] + types_path


  # Specify what your preferred output types are.
  preferred_types += ["NiftiImageFileCompressed",
                      "NiftiImageFile"]

  # Set the tmp mount
  mounts['tmp'] = '/path/to/tmpdir'


Format
^^^^^^

The config file is actually a python source file. The next syntax applies to
setting configuration values::

    # Simple values
    float_value = 1.0
    int_value = 1
    str_value = "Some value"
    other_str_value = 'name'.capitalize()

    # List-like values
    list_value = ['over', 'ride', 'values']
    other_list_value.prepend('first')
    other_list_value.append('list')

    # Dict-like values
    dict_value = {'this': 1, 'is': 2, 'fixed': 3}
    other_dict_value['added'] = 'this key'

.. note:: Dictionaries and list always have a default, so you can always append
          or assign elements to them and do not have to create them in a config
          file. Best practice is to only edit them unless you really want to
          block out the earliers config files.

Most operations will be assigning values, but for list and dict values
a special wrapper object is used that allows manipulations from the default.
This limits the operations allowed.

List values in the ``config.py`` have the following supported operators/methods:

* ``+``, ``__add__`` and ``__radd__``
* ``+=`` or ``__iadd__``
* ``append``
* ``prepend``
* ``extend``

Mapping (dict-like) values in the ``config.py`` have the following supported operators/methods:

* ``update``
* ``[]`` or ``__getitem__``, ``__setitem__`` and ``__delitem__``

Configuration fields
^^^^^^^^^^^^^^^^^^^^

This is a table the known config fields on the system:

.. include:: ../fastr.config.rst


:py:class:`Tool <fastr.core.tool.Tool>` description
---------------------------------------------------

.. _tool-schema:

:py:class:`Tools <fastr.core.tool.Tool>` are the building blocks in the fastr network. To add new
:py:class:`Tools <fastr.core.tool.Tool>` to fastr, XML/json files containing a :py:class:`Tool <fastr.core.tool.Tool>`
definition can be added. These files have the following layout:

+-------------------------------------------------+--------------------------------------------------------------------------------+
| Attribute                                       | Description                                                                    |
+=================================================+================================================================================+
| ``id``                                          | The id of this Tool (used internally in fastr)                                 |
+---------------+---------------------------------+--------------------------------------------------------------------------------+
| ``name``      |                                 | The name of the Tool, for human readability                                    |
+---------------+---------------------------------+--------------------------------------------------------------------------------+
| ``version``   |                                 | The version of the Tool wrapper (not the binary)                               |
+---------------+---------------------------------+--------------------------------------------------------------------------------+
| ``url``       |                                 | The url of the Tool wrapper                                                    |
+---------------+---------------------------------+--------------------------------------------------------------------------------+
| ``authors[]`` |                                 | List of authors of the Tools wrapper                                           |
|               +---------------------------------+--------------------------------------------------------------------------------+
|               | ``name``                        | Name of the author                                                             |
|               +---------------------------------+--------------------------------------------------------------------------------+
|               | ``email``                       | Email address of the author                                                    |
|               +---------------------------------+--------------------------------------------------------------------------------+
|               | ``url``                         | URL of the website of the author                                               |
+---------------+---------------------------------+--------------------------------------------------------------------------------+
| ``tags``      | ``tag[]``                       | List of tags describing the Tool                                               |
+---------------+---------------------------------+--------------------------------------------------------------------------------+
| ``command``   |                                 | Description of the underlying command                                          |
|               +---------------------------------+--------------------------------------------------------------------------------+
|               | ``version``                     | Version of the tool that is wrapped                                            |
|               +---------------------------------+--------------------------------------------------------------------------------+
|               | ``url``                         | Website where the tools that is wrapped can be obtained                        |
|               +---------------+-----------------+--------------------------------------------------------------------------------+
|               | ``targets[]`` |                 | Description of the target binaries/script of this Tool                         |
|               |               +-----------------+--------------------------------------------------------------------------------+
|               |               | ``os``          | OS targetted (windows, linux, macos or * (for any)                             |
|               |               +-----------------+--------------------------------------------------------------------------------+
|               |               | ``arch``        | Architecture targetted 32, 64 or * (for any)                                   |
|               |               +-----------------+--------------------------------------------------------------------------------+
|               |               | ``module``      | Environment module giving access to the Tool                                   |
|               |               +-----------------+--------------------------------------------------------------------------------+
|               |               | ``location``    | If the module is not found, try using this location to find the Tool           |
|               |               +-----------------+--------------------------------------------------------------------------------+
|               |               | ``interpreter`` | Interpreter to use to call the ``bin`` with (e.g. bash, python, Rscript)       |
|               |               +-----------------+--------------------------------------------------------------------------------+
|               |               | ``bin``         | Name of the Tool binary (e.g. toolname, toolname.exe, toolname.py              |
|               +---------------+-----------------+--------------------------------------------------------------------------------+
|               | ``description``                 | Description of the Tool                                                        |
|               +---------------------------------+--------------------------------------------------------------------------------+
|               | ``license``                     | License of the Tool, either full license or a clear name (e.g. LGPL, GPL v2)   |
|               +---------------+-----------------+--------------------------------------------------------------------------------+
|               | ``authors[]`` |                 | List of authors of the Tool (not the wrapper!)                                 |
|               |               +-----------------+--------------------------------------------------------------------------------+
|               |               | ``name``        | Name of the authors                                                            |
|               |               +-----------------+--------------------------------------------------------------------------------+
|               |               | ``email``       | Email address of the author                                                    |
|               |               +-----------------+--------------------------------------------------------------------------------+
|               |               | ``url``         | URL of the website of the author                                               | 
+---------------+---------------+-----------------+--------------------------------------------------------------------------------+
| ``inputs[]``  |                                 | List of Inputs that can are accepted by the Tool                               |
|               +---------------------------------+--------------------------------------------------------------------------------+
|               | ``id``                          | ID of the Input                                                                |
|               +---------------------------------+--------------------------------------------------------------------------------+
|               | ``name``                        | Longer name of the Input (more human readable)                                 |
|               +---------------------------------+--------------------------------------------------------------------------------+
|               | ``datatype``                    | The ID of the DataType of the Input [#f1]_                                     |
|               +---------------------------------+--------------------------------------------------------------------------------+
|               | ``enum[]``                      | List of possible values for an EnumType (created on the fly by fastr) [#f1]_   |
|               +---------------------------------+--------------------------------------------------------------------------------+
|               | ``prefix``                      | Commandline prefix of the Input (e.g. --in, -i)                                |
|               +---------------------------------+--------------------------------------------------------------------------------+
|               | ``cardinality``                 | Cardinality of the Input                                                       |
|               +---------------------------------+--------------------------------------------------------------------------------+
|               | ``repeat_prefix``               | Flag indicating if for every value of the Input the prefix is repeated         |
|               +---------------------------------+--------------------------------------------------------------------------------+
|               | ``required``                    | Flag indicating if the input is required                                       |
|               +---------------------------------+--------------------------------------------------------------------------------+
|               | ``nospace``                     | Flag indicating if there is no space between prefix and value (e.g. --in=val)  |
|               +---------------------------------+--------------------------------------------------------------------------------+
|               | ``format``                      | For DataTypes that have multiple representations, indicate which one to use    |
|               +---------------------------------+--------------------------------------------------------------------------------+
|               | ``default``                     | Default value for the Input                                                    |
|               +---------------------------------+--------------------------------------------------------------------------------+
|               | ``description``                 | Long description for an input                                                  |
+---------------+---------------------------------+--------------------------------------------------------------------------------+
| ``outputs[]`` |                                 | List of Outputs that are generated by the Tool (and accessible to fastr)       |
|               +---------------------------------+--------------------------------------------------------------------------------+
|               | ``id``                          | ID of the Output                                                               |
|               +---------------------------------+--------------------------------------------------------------------------------+
|               | ``name``                        | Longer name of the Output (more human readable)                                |
|               +---------------------------------+--------------------------------------------------------------------------------+
|               | ``datatype``                    | The ID of the DataType of the Output [#f1]_                                    |
|               +---------------------------------+--------------------------------------------------------------------------------+
|               | ``enum[]``                      | List of possible values for an EnumType (created on the fly by fastr) [#f1]_   |
|               +---------------------------------+--------------------------------------------------------------------------------+
|               | ``prefix``                      | Commandline prefix of the Output (e.g. --out, -o)                              |
|               +---------------------------------+--------------------------------------------------------------------------------+
|               | ``cardinality``                 | Cardinality of the Output                                                      |
|               +---------------------------------+--------------------------------------------------------------------------------+
|               | ``repeat_prefix``               | Flag indicating if for every value of the Output the prefix is repeated        |
|               +---------------------------------+--------------------------------------------------------------------------------+
|               | ``required``                    | Flag indicating if the input is required                                       |
|               +---------------------------------+--------------------------------------------------------------------------------+
|               | ``nospace``                     | Flag indicating if there is no space between prefix and value (e.g. --out=val) |
|               +---------------------------------+--------------------------------------------------------------------------------+
|               | ``format``                      | For DataTypes that have multiple representations, indicate which one to use    |
|               +---------------------------------+--------------------------------------------------------------------------------+
|               | ``description``                 | Long description for an input                                                  |
|               +---------------------------------+--------------------------------------------------------------------------------+
|               | ``action``                      | Special action (defined per DataType) that needs to be performed before        |
|               |                                 | creating output value (e.g. 'ensure' will make sure an output directory exists)|
|               +---------------------------------+--------------------------------------------------------------------------------+
|               | ``automatic``                   | Indicate that output doesn't require commandline argument, but is created      |
|               |                                 | automatically by a Tool [#f2]_                                                 |
|               +---------------------------------+--------------------------------------------------------------------------------+
|               | ``method``                      | Method to acquire output value from the Tool can be 'path' or 'stdout' [#f2]_  |
|               +---------------------------------+--------------------------------------------------------------------------------+
|               | ``location``                    | Definition where to an automatically, usage depends on the ``method`` [#f2]_   |
+---------------+---------------------------------+--------------------------------------------------------------------------------+
| ``help``                                        | Help text explaining the use of the Tool                                       |
+-------------------------------------------------+--------------------------------------------------------------------------------+
| ``cite``                                        | Bibtext of the Citation(s) to reference when using this Tool for a publication |
+-------------------------------------------------+--------------------------------------------------------------------------------+

.. rubric:: Footnotes

.. [#f1] ``datatype`` and ``enum`` are conflicting entries, if both specified ``datatype`` has presedence
.. [#f2] More details on defining automatica output are given in [TODO]



