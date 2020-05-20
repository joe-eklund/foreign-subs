"""Miscellaneous models."""
from datetime import datetime, timezone

import bson
from pydantic import BaseModel


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


class Metadata(BaseModel):
    """
    Metadata info.

    **date_created** - The date and time of creation of the item.

    **created_by** - Which user created the item.

    **last_modified** - The date and time the item was last modified.

    **modified_by** - Which user was the last to modify the item.
    """

    date_created: datetime = datetime.now(timezone.utc)
    created_by: str = None
    last_modified: datetime = None
    modified_by: str = None
