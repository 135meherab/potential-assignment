from core.models import *
from products.models import CategoryModel, SubCategoryModel
from authentications.models import User
class ProductModel(BaseModel):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.PositiveIntegerField()
    category = models.ForeignKey(CategoryModel, related_name='products', on_delete=models.CASCADE)
    subcategory = models.ForeignKey(SubCategoryModel, related_name='products', on_delete=models.CASCADE)
    vendor = models.ForeignKey(User, related_name='products', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=content_file_path, blank=True, null=True)

    def __str__(self):
        return self.name
