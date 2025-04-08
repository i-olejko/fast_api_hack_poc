from pydantic import BaseModel

class TableExtruction(BaseModel):
	first_extracted_role_name: str
	first_extracted_role_description: str