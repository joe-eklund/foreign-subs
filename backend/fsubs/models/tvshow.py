"""TV show models."""

from pydantic import validator

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

    **season** - The season number the episode belongs to.

    **episode** - The episode number in the season.
    """

    season: int
    episode: int

    @validator('season')
    def valid_season(cls, v):
        """Validate season."""
        assert v >= 0, "Season cannot be negative."
        return v

    @validator('episode')
    def valid_episode(cls, v):
        """Validate episode."""
        assert v >= 0, "Episode cannot be negative."
        return v


class TVShowEpisodeInDB(TVShowEpisode):
    """
    The TVShowEpisode in the db.

    **id** - The id of the item in the database.

    **metadata** - The Metadata object to be associated with the item.
    """

    id: str
    metadata: Metadata = Metadata()
