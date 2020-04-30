from datetime import datetime
from enum import Enum

from pydantic import List, Union, validator

from app.models.shared import BasicModel


class DiscType(Enum):
    """The kind of disc for the ``VideoInstance``."""
    bd = 'BD'
    bd3d = 'BD3D'
    dvd = 'DVD'
    uhd = 'UHD'
    web_dl = 'WEB-DL'
    unknown = 'UNKNOWN'


class DVDRegion(Enum):
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


class BluRegion(Enum):
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


class SubType(Enum):
    """
    What kind of type the subtitles are.
    Separate means the subs are on a separate track. Hardocded means the subs are burned into the
    video. Forced means there is a separate track that has been flagged forced.
    """
    separate = 'Separate'
    hardcoded = 'Hardcoded'
    forced = 'Forced'
    unknown = 'Unknown'


class VideoInstance(BasicModel):
    disc_type: List[DiscType] = DiscType['unknown']
    region: List[Union[DVDRegion, BluRegion]] = BluRegion['unknown']
    timestamps: List[str]
    sub_type: SubType = SubType['unknown']
    description: str = None
    track: int = None
    date_created: datetime = datetime.now()
    created_by: str = None
    last_modified: datetime = None
    last_modified_by: str = None

    @validator('timestamps')
    def valid_timestamps(cls, v):
        # TODO Validate timestamps for real...
        return v


class VideoInstanceInDB(VideoInstance):
    id: int


class VideoBase(BasicModel):
    title: str = None
    description: str = None
    imdb_id: str = None
    instances = List[VideoInstance]


class VideoBaseInDB(VideoBase):
    id: int