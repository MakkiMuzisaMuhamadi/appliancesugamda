from django import forms
from mainApp.models import Brand, Category, Product


class ProductForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all())
    brand = forms.ModelChoiceField(queryset=Brand.objects.none())

    class Meta:
        model = Product
        fields = ['category', 'brand', 'name', 'price', 'description', 'image']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['brand'].queryset = Brand.objects.none()

        if 'category' in self.data:
            try:
                category_id = int(self.data.get('category'))
                self.fields['brand'].queryset = Brand.objects.filter(category_id=category_id)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['brand'].queryset = self.instance.category.brand_set
            


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'image']

class BrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = ['name', 'category']


