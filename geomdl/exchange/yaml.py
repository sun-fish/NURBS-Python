"""
.. module:: exchange.yaml
    :platform: Unix, Windows
    :synopsis: Provides exchange capabilities for YAML file format

.. moduleauthor:: Onur R. Bingol <contact@onurbingol.net>

"""

from io import StringIO
from ..base import export, GeomdlError, GeomdlFloat
from . import exc_helpers


@export
def import_yaml(file_name, **kwargs):
    """ Imports curves and surfaces from files in YAML format.

    .. note::

        Requires `ruamel.yaml <https://pypi.org/project/ruamel.yaml/>`_ package.

    Use ``jinja2=True`` to activate Jinja2 template processing. Please refer to the documentation for details.

    :param file_name: name of the input file
    :type file_name: str
    :return: a list of rational spline geometries
    :rtype: list
    :raises GeomdlException: an error occurred reading the file
    """
    def callback(data):
        yaml = YAML()
        return yaml.load(data)

    # Check if it is possible to import 'ruamel.yaml'
    try:
        from ruamel.yaml import YAML
    except ImportError:
        raise GeomdlError("Please install 'ruamel.yaml' package to use YAML format: pip install ruamel.yaml")

    # Get keyword arguments
    use_template = kwargs.get('jinja2', False)

    # Read file
    file_src = exc_helpers.read_file(file_name)

    # Import data
    return exc_helpers.import_dict_str(file_src=file_src, callback=callback, tmpl=use_template)


@export
def export_yaml_str(obj):
    """ Exports curves and surfaces in YAML format as a string.

    .. note::

        Requires `ruamel.yaml <https://pypi.org/project/ruamel.yaml/>`_ package.

    :param obj: input geometry
    :type obj: abstract.SplineGeometry
    :raises GeomdlException: an error occurred writing the file
    """
    def callback(data):
        # Ref: https://yaml.readthedocs.io/en/latest/example.html#output-of-dump-as-a-string
        stream = StringIO()
        yaml = YAML()
        yaml.register_class(GeomdlFloat)  # register GeomdlFloat
        yaml.dump(data, stream)
        return stream.getvalue()

    # Check if it is possible to import 'ruamel.yaml'
    try:
        from ruamel.yaml import YAML
    except ImportError:
        raise GeomdlError("Please install 'ruamel.yaml' package to use YAML format: pip install ruamel.yaml")

    # Export data
    return exc_helpers.export_dict_str(obj=obj, callback=callback)


@export
def export_yaml(obj, file_name):
    """ Exports curves and surfaces in YAML format as a file.

    .. note::

        Requires `ruamel.yaml <https://pypi.org/project/ruamel.yaml/>`_ package.

    :param obj: input geometry
    :type obj: abstract.SplineGeometry
    :param file_name: name of the output file
    :type file_name: str
    :raises GeomdlException: an error occurred writing the file
    """
    # Write to file
    return exc_helpers.write_file(file_name, export_yaml_str(obj))
