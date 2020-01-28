from pydantic import BaseModel, BaseConfig


class BasicModel(BaseModel):
    class Config(BaseConfig):
        orm_mode = True
