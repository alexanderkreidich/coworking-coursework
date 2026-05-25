"""Представления для каталога ресурсов и CRUD-операций."""
from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from accounts.permissions import admin_required

from .forms import ResourceFilterForm, ResourceForm
from .models import Resource


def catalog(request):
    """Каталог ресурсов с фильтрацией и поиском."""
    filter_form = ResourceFilterForm(request.GET or None)
    resources = Resource.objects.filter(is_active=True)

    if filter_form.is_valid():
        search = filter_form.cleaned_data.get("search")
        type_ = filter_form.cleaned_data.get("type")
        capacity_min = filter_form.cleaned_data.get("capacity_min")
        price_max = filter_form.cleaned_data.get("price_max")

        if search:
            resources = resources.filter(name__icontains=search) | resources.filter(
                description__icontains=search
            )
        if type_:
            resources = resources.filter(type=type_)
        if capacity_min:
            resources = resources.filter(capacity__gte=capacity_min)
        if price_max is not None:
            resources = resources.filter(price_per_hour__lte=price_max)

    resources = resources.order_by("type", "name")
    paginator = Paginator(resources, 9)
    page = paginator.get_page(request.GET.get("page"))

    return render(
        request,
        "resources/catalog.html",
        {"page": page, "filter_form": filter_form},
    )


def detail(request, pk):
    resource = get_object_or_404(Resource, pk=pk)
    return render(request, "resources/detail.html", {"resource": resource})


@admin_required
def admin_list(request):
    resources = Resource.objects.all().order_by("type", "name")
    return render(request, "resources/admin_list.html", {"resources": resources})


@admin_required
def create(request):
    if request.method == "POST":
        form = ResourceForm(request.POST, request.FILES)
        if form.is_valid():
            resource = form.save()
            messages.success(request, f"Ресурс «{resource.name}» создан.")
            return redirect("resources:admin_list")
    else:
        form = ResourceForm()
    return render(
        request,
        "resources/form.html",
        {"form": form, "title": "Создание ресурса"},
    )


@admin_required
def edit(request, pk):
    resource = get_object_or_404(Resource, pk=pk)
    if request.method == "POST":
        form = ResourceForm(request.POST, request.FILES, instance=resource)
        if form.is_valid():
            form.save()
            messages.success(request, "Ресурс обновлён.")
            return redirect("resources:admin_list")
    else:
        form = ResourceForm(instance=resource)
    return render(
        request,
        "resources/form.html",
        {"form": form, "title": f"Редактирование: {resource.name}"},
    )


@admin_required
def delete(request, pk):
    resource = get_object_or_404(Resource, pk=pk)
    if request.method == "POST":
        resource.delete()
        messages.success(request, "Ресурс удалён.")
        return redirect("resources:admin_list")
    return render(request, "resources/delete.html", {"resource": resource})
