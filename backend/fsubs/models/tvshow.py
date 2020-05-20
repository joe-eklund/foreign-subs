"""TV show models."""

from pydantic import BaseModel

from fsubs.models.video import VideoBase


class TVShow(BaseModel):
    """
    Representation of a single tv show.

    todo params
    """


class TVShowInDB(TVShow):
    """
    The TVShow stored in the db.

    todo params
    """


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
