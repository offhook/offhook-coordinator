# coding: utf-8

from __future__ import absolute_import
from .base_model_ import Model
from . import util


class SearchResult(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    def __init__(self, name=None, full_name=None):  # noqa: E501
        """SearchResult - a model defined in Swagger

        :param name: The name of this SearchResult.  # noqa: E501
        :type name: str
        :param full_name: The full_name of this SearchResult.  # noqa: E501
        :type full_name: str
        """
        self.swagger_types = {
            'name': str,
            'full_name': str
        }

        self.attribute_map = {
            'name': 'name',
            'full_name': 'fullName'
        }

        self._name = name
        self._full_name = full_name

    @classmethod
    def from_dict(cls, dikt):
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The SearchResult of this SearchResult.  # noqa: E501
        :rtype: SearchResult
        """
        return util.deserialize_model(dikt, cls)

    @property
    def name(self):
        """Gets the name of this SearchResult.


        :return: The name of this SearchResult.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this SearchResult.


        :param name: The name of this SearchResult.
        :type name: str
        """
        if name is None:
            raise ValueError("Invalid value for `name`, must not be `None`")  # noqa: E501

        self._name = name

    @property
    def full_name(self):
        """Gets the full_name of this SearchResult.

        A fully-describing name of the package  # noqa: E501

        :return: The full_name of this SearchResult.
        :rtype: str
        """
        return self._full_name

    @full_name.setter
    def full_name(self, full_name):
        """Sets the full_name of this SearchResult.

        A fully-describing name of the package  # noqa: E501

        :param full_name: The full_name of this SearchResult.
        :type full_name: str
        """
        if full_name is None:
            raise ValueError("Invalid value for `full_name`, must not be `None`")  # noqa: E501

        self._full_name = full_name
