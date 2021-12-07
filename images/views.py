from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ImageCreateForm
from django.shortcuts import get_object_or_404
from .models import Image
# Create your views here.

@login_required
def image_create(request):
    form = ImageCreateForm(data=request.GET)
    if request.method == 'POST':
        form = ImageCreateForm(data=request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            image = form.save(commit=False)
            image.user = request.user
            image.save()
            messages.success(request, 'Image added successfully')
            return redirect(image.get_absolute_url())
    return render(request,
                  'images/image/create.html',
                  {'form': form})

@login_required
def image_detail(request, id, slug):
    image = get_object_or_404(Image, id=id, slug=slug)
    return render(request, 'images/image/detail.html',
                            {'section': 'images',
                            'image': image})

