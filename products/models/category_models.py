from core.models import *


class CategoryModel(BaseModel):
    name = models.CharField(max_length=100)


class SubCategoryModel(BaseModel):
    category = models.ForeignKey(CategoryModel, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
