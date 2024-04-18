from django import forms
from category.models import Category

class categoryForm(forms.ModelForm):
  class Meta:
    model = Category
    fields = ['category_name', 'description', 'catgory_img']
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    for field in self.fields:
      if field == 'catgory_img':
        continue
      self.fields[field].widget.attrs.update({
            'class': (
                'form-control'
            )})
