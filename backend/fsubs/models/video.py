"""Video models."""
from enum import Enum
from typing import List, Union

from pydantic import BaseModel, validator

from fsubs.models.misc import Metadata


class DiscType(str, Enum):
    """The kind of disc for the `VideoInstance`."""

    bd = 'BD'
    bd3d = 'BD3D'
    dvd = 'DVD'
    uhd = 'UHD'
    web_dl = 'WEB-DL'
    unknown = 'UNKNOWN'


class DVDRegion(str, Enum):
    """
    What region the DVD is encoded for.

    See https://en.wikipedia.org/wiki/DVD_region_code#Region_codes_and_countries for what countries
    each region consists of.
    """

    r0 = 'Region 0'
    r1 = 'Region 1'
    r2 = 'Region 2'
    r3 = 'Region 3'
    r4 = 'Region 4'
    r5 = 'Region 5'
    r6 = 'Region 6'
    r7 = 'Region 7'
    r8 = 'Region 8'
    all = 'ALL'
    unknown = 'UNKNOWN'


class BluRegion(str, Enum):
    """
    What region the Blu-Ray is encoded for.

    See https://en.wikipedia.org/wiki/DVD_region_code#Blu-ray_Disc_region_codes for what countries
    each region consists of. Most BD's are region 0 (region free).
    """

    a = 'A'
    b = 'B'
    c = 'C'
    abc = 'ALL'
    free = 'ALL'
    unknown = 'UNKNOWN'


class SubType(str, Enum):
    """
    What type the subtitles are.

    Separate means the subs are on a separate track. Hardocded means the subs are burned into the
    video. Forced means there is a separate track that has been flagged forced.
    """

    separate = 'Separate'
    hardcoded = 'Hardcoded'
    forced = 'Forced'
    unknown = 'Unknown'


class VideoInstance(BaseModel):
    """
    A single instance of a video.

    For example, the extended edition of a video may be different than the theatrical, even though
    they are the same movie.

    **disc_type** - What type of disc the instance is from (e.g. `DVD`)

    **region** - Which region the source is from (e.g. `Region 0` or `A`)

    **timestamps** - A list of timestamps as strings. A timestamp is of the form: `TODO`.

    **sub_type** - What type the subtitles are (e.g. `Hardcoded`).

    **description** - The description of the video instance.

    **track** - Which track (if applicable) the subtitle is.
    """

    disc_type: DiscType = DiscType['unknown']
    region: Union[DVDRegion, BluRegion] = BluRegion['unknown']
    timestamps: List[str]
    sub_type: SubType = SubType['unknown']
    description: str = None
    track: int = None

    @validator('timestamps')
    def valid_timestamps(cls, v):
        """Validate timestamps."""
        # TODO Validate timestamps for real...
        return v


class VideoInstanceInDB(VideoInstance):
    """
    The VideoInstance stored in the db.

    **id** - The id of the item in the database.

    **video_base_id** - The id of the `VideoBaseInDB` to associate the `VideoInstanceInDB` with.
    """

    id: str
    video_base_id: str
    metadata: Metadata = Metadata()


class VideoBase(BaseModel):
    """
    Base video class. Used to represent a movie or single TV episode.

    **title** - The title of the video.

    **imdb_id** - The IMDB id of the video.

    **description** - Description of the video.

    **no_subs** - Set to `True` if the video has been verified to have no subtitles.
    """

    title: str
    imdb_id: str
    description: str = None
    no_subs: bool = False


class VideoBaseInDB(VideoBase):
    """
    The VideoBase class stored in db.

    **id** - The id of the item in the database.

    **metadata** - The Metadata object to be associated with the item.
    """

    id: str
    metadata: Metadata = Metadata()
