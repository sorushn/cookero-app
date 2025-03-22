from pydantic import BaseModel, Field

class RecipeBase(BaseModel):
    name: str = Field(..., json_schema_extra={"example": "Recipe Name"}, min_length=3, max_length=100)
    instructions: str = Field(..., json_schema_extra={"example": "Recipe Instructions"}, max_length=10000)

class RecipeCreate(RecipeBase):
    user_id: str = Field(..., json_schema_extra={"example": "28f24e1a-f56a-431d-8155-195948bf32b1"})

class RecipeUpdate(RecipeBase):
    id: str = Field(..., json_schema_extra={"example": "28f24e1a-f56a-431d-8155-195948bf32b1"})