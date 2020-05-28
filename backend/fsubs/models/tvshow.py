"""TV show models."""

from fsubs.models.video import VideoBase
from fsubs.models.misc import Metadata


class TVShowInDB(VideoBase):
    """
    The TVShow stored in the db.

    **id** - The id of the item in the database.

    **metadata** - The Metadata object to be associated with the item.
    """
    id: str
    metadata: Metadata = Metadata()


class TVShowEpisode(VideoBase):
    """
    Representation of a single tv show episode.

    todo params
    """


class TVShowEpisodeInDB(TVShowEpisode):
    """
    The TVShowEpisode in the db.

    todo params
    """