#!/usr/bin/env python3
"""
Script to create remaining custom admin templates for the school website
"""

import os

templates = {
    "gallery_category_confirm_delete.html": """{% extends 'main/custom_admin/base.html' %}

{% block title %}Delete Gallery Category - Custom Admin{% endblock %}

{% block content %}
<div class="container-fluid">
    <div class="row justify-content-center">
        <div class="col-md-6">
            <div class="card">
                <div class="card-header bg-danger text-white">
                    <h4 class="mb-0">Confirm Delete</h4>
                </div>
                <div class="card-body">
                    <p class="text-center">
                        <i class="fas fa-exclamation-triangle fa-3x text-warning mb-3"></i>
                    </p>
                    <h5 class="text-center">Are you sure you want to delete this category?</h5>
                    <p class="text-center"><strong>{{ category.name }}</strong></p>
                    
                    <form method="post">
                        {% csrf_token %}
                        <div class="d-flex justify-content-center gap-2">
                            <a href="{% url 'main:gallery_category_list' %}" class="btn btn-secondary">
                                <i class="fas fa-times"></i> Cancel
                            </a>
                            <button type="submit" class="btn btn-danger">
                                <i class="fas fa-trash"></i> Delete Category
                            </button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
""",

    "gallery_image_list.html": """{% extends 'main/custom_admin/base.html' %}
{% load static %}

{% block title %}Gallery Images - Custom Admin{% endblock %}

{% block content %}
<div class="container-fluid">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h1>Gallery Images</h1>
        <a href="{% url 'main:gallery_image_add' %}" class="btn btn-primary">
            <i class="fas fa-plus"></i> Add New Image
        </a>
    </div>

    {% if messages %}
        {% for message in messages %}
            <div class="alert alert-{{ message.tags }} alert-dismissible fade show" role="alert">
                {{ message }}
                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            </div>
        {% endfor %}
    {% endif %}

    <div class="card">
        <div class="card-body">
            {% if images %}
                <div class="table-responsive">
                    <table class="table table-hover">
                        <thead>
                            <tr>
                                <th>Image</th>
                                <th>Title</th>
                                <th>Category</th>
                                <th>Featured</th>
                                <th>Order</th>
                                <th>Upload Date</th>
                                <th>Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for image in images %}
                                <tr>
                                    <td>
                                        {% if image.image %}
                                            <img src="{{ image.image.url }}" alt="{{ image.title }}" style="width: 80px; height: 60px; object-fit: cover;">
                                        {% endif %}
                                    </td>
                                    <td>{{ image.title|truncatechars:30 }}</td>
                                    <td>{{ image.category.name }}</td>
                                    <td>
                                        {% if image.is_featured %}
                                            <span class="badge bg-success">Yes</span>
                                        {% else %}
                                            <span class="badge bg-secondary">No</span>
                                        {% endif %}
                                    </td>
                                    <td>{{ image.order }}</td>
                                    <td>{{ image.upload_date|date:"M d, Y" }}</td>
                                    <td>
                                        <a href="{% url 'main:gallery_image_edit' image.id %}" class="btn btn-sm btn-warning">
                                            <i class="fas fa-edit"></i>
                                        </a>
                                        <a href="{% url 'main:gallery_image_delete' image.id %}" class="btn btn-sm btn-danger">
                                            <i class="fas fa-trash"></i>
                                        </a>
                                    </td>
                                </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
            {% else %}
                <div class="text-center py-5">
                    <i class="fas fa-images fa-3x text-muted mb-3"></i>
                    <h4>No images found</h4>
                    <p class="text-muted">Add your first gallery image to get started.</p>
                    <a href="{% url 'main:gallery_image_add' %}" class="btn btn-primary">
                        <i class="fas fa-plus"></i> Add First Image
                    </a>
                </div>
            {% endif %}
        </div>
    </div>
</div>
{% endblock %}
""",

    "gallery_image_form.html": """{% extends 'main/custom_admin/base.html' %}

{% block title %}{% if image %}Edit{% else %}Add{% endif %} Gallery Image - Custom Admin{% endblock %}

{% block content %}
<div class="container-fluid">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h1>{% if image %}Edit Gallery Image{% else %}Add New Gallery Image{% endif %}</h1>
        <a href="{% url 'main:gallery_image_list' %}" class="btn btn-secondary">
            <i class="fas fa-arrow-left"></i> Back to List
        </a>
    </div>

    <div class="row">
        <div class="col-md-8">
            <div class="card">
                <div class="card-body">
                    <form method="post" enctype="multipart/form-data">
                        {% csrf_token %}
                        
                        {% if form.non_field_errors %}
                            <div class="alert alert-danger">
                                {{ form.non_field_errors }}
                            </div>
                        {% endif %}

                        <div class="mb-3">
                            <label for="{{ form.title.id_for_label }}" class="form-label">Title *</label>
                            {{ form.title }}
                            {% if form.title.errors %}
                                <div class="text-danger">{{ form.title.errors }}</div>
                            {% endif %}
                        </div>

                        <div class="mb-3">
                            <label for="{{ form.image.id_for_label }}" class="form-label">Image *</label>
                            {{ form.image }}
                            {% if form.image.errors %}
                                <div class="text-danger">{{ form.image.errors }}</div>
                            {% endif %}
                        </div>

                        {% if image and image.image %}
                            <div class="mb-3">
                                <label class="form-label">Current Image</label>
                                <img src="{{ image.image.url }}" alt="Current image" class="img-fluid" style="max-width: 200px;">
                            </div>
                        {% endif %}

                        <div class="mb-3">
                            <label for="{{ form.category.id_for_label }}" class="form-label">Category *</label>
                            {{ form.category }}
                            {% if form.category.errors %}
                                <div class="text-danger">{{ form.category.errors }}</div>
                            {% endif %}
                        </div>

                        <div class="mb-3">
                            <label for="{{ form.description.id_for_label }}" class="form-label">Description</label>
                            {{ form.description }}
                            {% if form.description.errors %}
                                <div class="text-danger">{{ form.description.errors }}</div>
                            {% endif %}
                        </div>

                        <div class="row">
                            <div class="col-md-6">
                                <div class="mb-3">
                                    <label for="{{ form.order.id_for_label }}" class="form-label">Order</label>
                                    {{ form.order }}
                                </div>
                            </div>
                            <div class="col-md-6">
                                <div class="mb-3">
                                    <div class="form-check mt-4">
                                        {{ form.is_featured }}
                                        <label class="form-check-label" for="{{ form.is_featured.id_for_label }}">
                                            Featured Image
                                        </label>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <div class="text-end">
                            <a href="{% url 'main:gallery_image_list' %}" class="btn btn-secondary">Cancel</a>
                            <button type="submit" class="btn btn-primary">
                                <i class="fas fa-save"></i> {% if image %}Update{% else %}Save{% endif %} Image
                            </button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
        
        <div class="col-md-4">
            <div class="card">
                <div class="card-header">
                    <h5 class="mb-0">Tips</h5>
                </div>
                <div class="card-body">
                    <ul>
                        <li>Upload high-quality images</li>
                        <li>Assign images to appropriate categories</li>
                        <li>Mark important images as featured</li>
                        <li>Use descriptive titles</li>
                    </ul>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}
""",

    "school_info_list.html": """{% extends 'main/custom_admin/base.html' %}
{% load static %}

{% block title %}School Information - Custom Admin{% endblock %}

{% block content %}
<div class="container-fluid">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h1>School Information</h1>
        <a href="{% url 'main:school_info_add' %}" class="btn btn-primary">
            <i class="fas fa-plus"></i> Add New Info
        </a>
    </div>

    {% if messages %}
        {% for message in messages %}
            <div class="alert alert-{{ message.tags }} alert-dismissible fade show" role="alert">
                {{ message }}
                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            </div>
        {% endfor %}
    {% endif %}

    <div class="card">
        <div class="card-body">
            {% if infos %}
                <div class="table-responsive">
                    <table class="table table-hover">
                        <thead>
                            <tr>
                                <th>Name</th>
                                <th>Established</th>
                                <th>Status</th>
                                <th>Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for info in infos %}
                                <tr>
                                    <td><strong>{{ info.name }}</strong></td>
                                    <td>{{ info.established_year }}</td>
                                    <td>
                                        {% if info.is_active %}
                                            <span class="badge bg-success">Active</span>
                                        {% else %}
                                            <span class="badge bg-secondary">Inactive</span>
                                        {% endif %}
                                    </td>
                                    <td>
                                        <a href="{% url 'main:school_info_edit' info.id %}" class="btn btn-sm btn-warning">
                                            <i class="fas fa-edit"></i> Edit
                                        </a>
                                        <a href="{% url 'main:school_info_delete' info.id %}" class="btn btn-sm btn-danger">
                                            <i class="fas fa-trash"></i> Delete
                                        </a>
                                    </td>
                                </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
            {% else %}
                <div class="text-center py-5">
                    <i class="fas fa-school fa-3x text-muted mb-3"></i>
                    <h4>No school information found</h4>
                    <p class="text-muted">Add school information to get started.</p>
                    <a href="{% url 'main:school_info_add' %}" class="btn btn-primary">
                        <i class="fas fa-plus"></i> Add School Info
                    </a>
                </div>
            {% endif %}
        </div>
    </div>
</div>
{% endblock %}
""",
}

# Create directory if it doesn't exist
os.makedirs('templates/main/custom_admin', exist_ok=True)

# Write all templates
for filename, content in templates.items():
    filepath = f'templates/main/custom_admin/{filename}'
    with open(filepath, 'w') as f:
        f.write(content)
    print(f"Created: {filepath}")

print("All templates created successfully!")