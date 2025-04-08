from pydantic import BaseModel

class Result(BaseModel):
	role_name: str
	role_description: str