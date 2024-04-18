from django.shortcuts import render, redirect
from category.models import Category
from category.forms import categoryForm

# Create your views here.
def createCategoryView(request, owner_name):
  if request.method == 'POST':
    form = categoryForm(request.POST)
    # print(request.POST.get['category_name'])
    print(form)
    if form.is_valid():
      print(form.cleaned_data)
      form.save()
      return redirect('dashboard', owner_name)
  else:
    form = categoryForm()
  return render(request, 'create_category.html', {'form':form})
    


