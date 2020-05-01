"""Miscellaneous models."""

import bson


class ObjectIdStr(str):
    """Model for a MongoDB ObjectId (that validates)."""

    @classmethod
    def __get_validators__(cls):
        """Implement get_validators dunder method."""
        yield cls.validate

    @classmethod
    def validate(cls, v):
        """Validate input against a bson ObjectId."""
        try:
            bson.ObjectId(v)
        except bson.objectid.InvalidId as e:
            raise ValueError(str(e))
        return str(v)
