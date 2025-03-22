from pydantic import BaseModel, Field

class RecipeBase(BaseModel):
    user_id: str = Field(..., example="28f24e1a-f56a-431d-8155-195948bf32b1")
    name: str = Field(..., example="Recipe Name", min_length=3, max_length=100)
    instructions: str = Field(..., example="Recipe Instructions", max_length=10000)

class RecipeCreate(RecipeBase):
    pass