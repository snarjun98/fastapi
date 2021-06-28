from pydantic import BaseModel
class model_data(BaseModel):
    id:str
    x: float
    y:float
    z:float
    lat:str
    lon:str
    pulse:str
    temp:str
     