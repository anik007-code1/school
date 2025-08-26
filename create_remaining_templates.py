#!/usr/bin/env python3
"""
Script to create remaining custom admin templates for ContactInfo, ExamType, StudentClass, and ClasswiseStudentCount
"""

import os

# Templates for remaining models
remaining_templates = {
    "school_info_form.html": """{% extends 'main/custom_admin/base.html' %}

{% block title %}{% if info %}Edit{% else %}Add{% endif %} School Info - Custom Admin{% endblock %}

{% block content %}
<div class="container-fluid">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h1>{% if info %}Edit School Information{% else %}Add School Information{% endif %}</h1>
        <a href="{% url 'main:school_info_list' %}" class="btn btn-secondary">
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

                        <div class="row">
                            <div class="col-md-6">
                                <div class="mb-3">
                                    <label for="{{ form.name.id_for_label }}" class="form-label">School Name *</label>
                                    {{ form.name }}
                                    {% if form.name.errors %}
                                        <div class="text-danger">{{ form.name.errors }}</div>
                                    {% endif %}
                                </div>
                            </div>
                            <div class="col-md-6">
                                <div class="mb-3">
                                    <label for="{{ form.tagline.id_for_label }}" class="form-label">Tagline</label>
                                    {{ form.tagline }}
                                    {% if form.tagline.errors %}
                                        <div class="text-danger">{{ form.tagline.errors }}</div>
                                    {% endif %}
                                </div>
                            </div>
                        </div>

                        <div class="mb-3">
                            <label for="{{ form.logo.id_for_label }}" class="form-label">School Logo</label>
                            {{ form.logo }}
                            {% if form.logo.errors %}
                                <div class="text-danger">{{ form.logo.errors }}</div>
                            {% endif %}
                        </div>

                        {% if info and info.logo %}
                            <div class="mb-3">
                                <label class="form-label">Current Logo</label>
                                <img src="{{ info.logo.url }}" alt="Current logo" class="img-fluid" style="max-width: 150px;">
                            </div>
                        {% endif %}

                        <div class="mb-3">
                            <label for="{{ form.address.id_for_label }}" class="form-label">Address</label>
                            {{ form.address }}
                            {% if form.address.errors %}
                                <div class="text-danger">{{ form.address.errors }}</div>
                            {% endif %}
                        </div>

                        <div class="row">
                            <div class="col-md-4">
                                <div class="mb-3">
                                    <label for="{{ form.phone.id_for_label }}" class="form-label">Phone</label>
                                    {{ form.phone }}
                                    {% if form.phone.errors %}
                                        <div class="text-danger">{{ form.phone.errors }}</div>
                                    {% endif %}
                                </div>
                            </div>
                            <div class="col-md-4">
                                <div class="mb-3">
                                    <label for="{{ form.email.id_for_label }}" class="form-label">Email</label>
                                    {{ form.email }}
                                    {% if form.email.errors %}
                                        <div class="text-danger">{{ form.email.errors }}</div>
                                    {% endif %}
                                </div>
                            </div>
                            <div class="col-md-4">
                                <div class="mb-3">
                                    <label for="{{ form.website.id_for_label }}" class="form-label">Website</label>
                                    {{ form.website }}
                                    {% if form.website.errors %}
                                        <div class="text-danger">{{ form.website.errors }}</div>
                                    {% endif %}
                                </div>
                            </div>
                        </div>

                        <div class="row">
                            <div class="col-md-6">
                                <div class="mb-3">
                                    <label for="{{ form.established_year.id_for_label }}" class="form-label">Established Year</label>
                                    {{ form.established_year }}
                                    {% if form.established_year.errors %}
                                        <div class="text-danger">{{ form.established_year.errors }}</div>
                                    {% endif %}
                                </div>
                            </div>
                            <div class="col-md-6">
                                <div class="mb-3">
                                    <div class="form-check mt-4">
                                        {{ form.is_active }}
                                        <label class="form-check-label" for="{{ form.is_active.id_for_label }}">
                                            Active
                                        </label>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <div class="mb-3">
                            <label for="{{ form.about.id_for_label }}" class="form-label">About School</label>
                            {{ form.about }}
                            {% if form.about.errors %}
                                <div class="text-danger">{{ form.about.errors }}</div>
                            {% endif %}
                        </div>

                        <div class="text-end">
                            <a href="{% url 'main:school_info_list' %}" class="btn btn-secondary">Cancel</a>
                            <button type="submit" class="btn btn-primary">
                                <i class="fas fa-save"></i> {% if info %}Update{% else %}Save{% endif %} School Info
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

    "school_info_confirm_delete.html": """{% extends 'main/custom_admin/base.html' %}

{% block title %}Delete School Info - Custom Admin{% endblock %}

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
                    <h5 class="text-center">Are you sure you want to delete this school information?</h5>
                    <p class="text-center"><strong>{{ info.name }}</strong></p>
                    
                    <form method="post">
                        {% csrf_token %}
                        <div class="d-flex justify-content-center gap-2">
                            <a href="{% url 'main:school_info_list' %}" class="btn btn-secondary">
                                <i class="fas fa-times"></i> Cancel
                            </a>
                            <button type="submit" class="btn btn-danger">
                                <i class="fas fa-trash"></i> Delete Info
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

    "contact_info_list.html": """{% extends 'main/custom_admin/base.html' %}
{% load static %}

{% block title %}Contact Information - Custom Admin{% endblock %}

{% block content %}
<div class="container-fluid">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h1>Contact Information</h1>
        <a href="{% url 'main:contact_info_add' %}" class="btn btn-primary">
            <i class="fas fa-plus"></i> Add New Contact Info
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
                                <th>Page Title</th>
                                <th>Main Phone</th>
                                <th>General Email</th>
                                <th>Status</th>
                                <th>Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for info in infos %}
                                <tr>
                                    <td>{{ info.page_title }}</td>
                                    <td>{{ info.main_phone }}</td>
                                    <td>{{ info.general_email }}</td>
                                    <td>
                                        {% if info.is_active %}
                                            <span class="badge bg-success">Active</span>
                                        {% else %}
                                            <span class="badge bg-secondary">Inactive</span>
                                        {% endif %}
                                    </td>
                                    <td>
                                        <a href="{% url 'main:contact_info_edit' info.id %}" class="btn btn-sm btn-warning">
                                            <i class="fas fa-edit"></i> Edit
                                        </a>
                                        <a href="{% url 'main:contact_info_delete' info.id %}" class="btn btn-sm btn-danger">
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
                    <i class="fas fa-address-book fa-3x text-muted mb-3"></i>
                    <h4>No contact information found</h4>
                    <p class="text-muted">Add contact information to get started.</p>
                    <a href="{% url 'main:contact_info_add' %}" class="btn btn-primary">
                        <i class="fas fa-plus"></i> Add Contact Info
                    </a>
                </div>
            {% endif %}
        </div>
    </div>
</div>
{% endblock %}
""",

    "contact_info_form.html": """{% extends 'main/custom_admin/base.html' %}

{% block title %}{% if info %}Edit{% else %}Add{% endif %} Contact Info - Custom Admin{% endblock %}

{% block content %}
<div class="container-fluid">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h1>{% if info %}Edit Contact Information{% else %}Add Contact Information{% endif %}</h1>
        <a href="{% url 'main:contact_info_list' %}" class="btn btn-secondary">
            <i class="fas fa-arrow-left"></i> Back to List
        </a>
    </div>

    <div class="row">
        <div class="col-md-8">
            <div class="card">
                <div class="card-body">
                    <form method="post">
                        {% csrf_token %}
                        
                        {% if form.non_field_errors %}
                            <div class="alert alert-danger">
                                {{ form.non_field_errors }}
                            </div>
                        {% endif %}

                        <div class="row">
                            <div class="col-md-6">
                                <div class="mb-3">
                                    <label for="{{ form.page_title.id_for_label }}" class="form-label">Page Title</label>
                                    {{ form.page_title }}
                                    {% if form.page_title.errors %}
                                        <div class="text-danger">{{ form.page_title.errors }}</div>
                                    {% endif %}
                                </div>
                            </div>
                            <div class="col-md-6">
                                <div class="mb-3">
                                    <label for="{{ form.main_phone.id_for_label }}" class="form-label">Main Phone</label>
                                    {{ form.main_phone }}
                                    {% if form.main_phone.errors %}
                                        <div class="text-danger">{{ form.main_phone.errors }}</div>
                                    {% endif %}
                                </div>
                            </div>
                        </div>

                        <div class="mb-3">
                            <label for="{{ form.address.id_for_label }}" class="form-label">Address</label>
                            {{ form.address }}
                            {% if form.address.errors %}
                                <div class="text-danger">{{ form.address.errors }}</div>
                            {% endif %}
                        </div>

                        <div class="row">
                            <div class="col-md-6">
                                <div class="mb-3">
                                    <label for="{{ form.general_email.id_for_label }}" class="form-label">General Email</label>
                                    {{ form.general_email }}
                                    {% if form.general_email.errors %}
                                        <div class="text-danger">{{ form.general_email.errors }}</div>
                                    {% endif %}
                                </div>
                            </div>
                            <div class="col-md-6">
                                <div class="mb-3">
                                    <div class="form-check mt-4">
                                        {{ form.enable_contact_form }}
                                        <label class="form-check-label" for="{{ form.enable_contact_form.id_for_label }}">
                                            Enable Contact Form
                                        </label>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <div class="mb-3">
                            <label for="{{ form.map_embed_code.id_for_label }}" class="form-label">Map Embed Code</label>
                            {{ form.map_embed_code }}
                            {% if form.map_embed_code.errors %}
                                <div class="text-danger">{{ form.map_embed_code.errors }}</div>
                            {% endif %}
                        </div>

                        <div class="text-end">
                            <a href="{% url 'main:contact_info_list' %}" class="btn btn-secondary">Cancel</a>
                            <button type="submit" class="btn btn-primary">
                                <i class="fas fa-save"></i> {% if info %}Update{% else %}Save{% endif %} Contact Info
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

    "contact_info_confirm_delete.html": """{% extends 'main/custom_admin/base.html' %}

{% block title %}Delete Contact Info - Custom Admin{% endblock %}

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
                    <h5 class="text-center">Are you sure you want to delete this contact information?</h5>
                    <p class="text-center"><strong>{{ info.page_title }}</strong></p>
                    
                    <form method="post">
                        {% csrf_token %}
                        <div class="d-flex justify-content-center gap-2">
                            <a href="{% url 'main:contact_info_list' %}" class="btn btn-secondary">
                                <i class="fas fa-times"></i> Cancel
                            </a>
                            <button type="submit" class="btn btn-danger">
                                <i class="fas fa-trash"></i> Delete Contact Info
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

    "exam_type_list.html": """{% extends 'main/custom_admin/base.html' %}
{% load static %}

{% block title %}Exam Types - Custom Admin{% endblock %}

{% block content %}
<div class="container-fluid">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h1>Exam Types</h1>
        <a href="{% url 'main:exam_type_add' %}" class="btn btn-primary">
            <i class="fas fa-plus"></i> Add New Exam Type
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
            {% if types %}
                <div class="table-responsive">
                    <table class="table table-hover">
                        <thead>
                            <tr>
                                <th>Name</th>
                                <th>Code</th>
                                <th>Description</th>
                                <th>Order</th>
                                <th>Status</th>
                                <th>Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for type_obj in types %}
                                <tr>
                                    <td><strong>{{ type_obj.name }}</strong></td>
                                    <td>{{ type_obj.code }}</td>
                                    <td>{{ type_obj.description|truncatechars:50|default:"-" }}</td>
                                    <td>{{ type_obj.order }}</td>
                                    <td>
                                        {% if type_obj.is_active %}
                                            <span class="badge bg-success">Active</span>
                                        {% else %}
                                            <span class="badge bg-secondary">Inactive</span>
                                        {% endif %}
                                    </td>
                                    <td>
                                        <a href="{% url 'main:exam_type_edit' type_obj.id %}" class="btn btn-sm btn-warning">
                                            <i class="fas fa-edit"></i> Edit
                                        </a>
                                        <a href="{% url 'main:exam_type_delete' type_obj.id %}" class="btn btn-sm btn-danger">
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
                    <i class="fas fa-clipboard-list fa-3x text-muted mb-3"></i>
                    <h4>No exam types found</h4>
                    <p class="text-muted">Add your first exam type to get started.</p>
                    <a href="{% url 'main:exam_type_add' %}" class="btn btn-primary">
                        <i class="fas fa-plus"></i> Add First Exam Type
                    </a>
                </div>
            {% endif %}
        </div>
    </div>
</div>
{% endblock %}
""",

    "exam_type_form.html": """{% extends 'main/custom_admin/base.html' %}

{% block title %}{% if type_obj %}Edit{% else %}Add{% endif %} Exam Type - Custom Admin{% endblock %}

{% block content %}
<div class="container-fluid">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h1>{% if type_obj %}Edit Exam Type{% else %}Add New Exam Type{% endif %}</h1>
        <a href="{% url 'main:exam_type_list' %}" class="btn btn-secondary">
            <i class="fas fa-arrow-left"></i> Back to List
        </a>
    </div>

    <div class="row">
        <div class="col-md-8">
            <div class="card">
                <div class="card-body">
                    <form method="post">
                        {% csrf_token %}
                        
                        {% if form.non_field_errors %}
                            <div class="alert alert-danger">
                                {{ form.non_field_errors }}
                            </div>
                        {% endif %}

                        <div class="row">
                            <div class="col-md-6">
                                <div class="mb-3">
                                    <label for="{{ form.name.id_for_label }}" class="form-label">Name *</label>
                                    {{ form.name }}
                                    {% if form.name.errors %}
                                        <div class="text-danger">{{ form.name.errors }}</div>
                                    {% endif %}
                                </div>
                            </div>
                            <div class="col-md-6">
                                <div class="mb-3">
                                    <label for="{{ form.code.id_for_label }}" class="form-label">Code *</label>
                                    {{ form.code }}
                                    {% if form.code.errors %}
                                        <div class="text-danger">{{ form.code.errors }}</div>
                                    {% endif %}
                                </div>
                            </div>
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
                                        {{ form.is_active }}
                                        <label class="form-check-label" for="{{ form.is_active.id_for_label }}">
                                            Active
                                        </label>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <div class="text-end">
                            <a href="{% url 'main:exam_type_list' %}" class="btn btn-secondary">Cancel</a>
                            <button type="submit" class="btn btn-primary">
                                <i class="fas fa-save"></i> {% if type_obj %}Update{% else %}Save{% endif %} Exam Type
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

    "exam_type_confirm_delete.html": """{% extends 'main/custom_admin/base.html' %}

{% block title %}Delete Exam Type - Custom Admin{% endblock %}

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
                    <h5 class="text-center">Are you sure you want to delete this exam type?</h5>
                    <p class="text-center"><strong>{{ type_obj.name }} ({{ type_obj.code }})</strong></p>
                    
                    <form method="post">
                        {% csrf_token %}
                        <div class="d-flex justify-content-center gap-2">
                            <a href="{% url 'main:exam_type_list' %}" class="btn btn-secondary">
                                <i class="fas fa-times"></i> Cancel
                            </a>
                            <button type="submit" class="btn btn-danger">
                                <i class="fas fa-trash"></i> Delete Exam Type
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

    "student_class_list.html": """{% extends 'main/custom_admin/base.html' %}
{% load static %}

{% block title %}Student Classes - Custom Admin{% endblock %}

{% block content %}
<div class="container-fluid">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h1>Student Classes</h1>
        <a href="{% url 'main:student_class_add' %}" class="btn btn-primary">
            <i class="fas fa-plus"></i> Add New Class
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
            {% if classes %}
                <div class="table-responsive">
                    <table class="table table-hover">
                        <thead>
                            <tr>
                                <th>Name</th>
                                <th>Code</th>
                                <th>Description</th>
                                <th>Order</th>
                                <th>Status</th>
                                <th>Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for class_obj in classes %}
                                <tr>
                                    <td><strong>{{ class_obj.name }}</strong></td>
                                    <td>{{ class_obj.code }}</td>
                                    <td>{{ class_obj.description|truncatechars:50|default:"-" }}</td>
                                    <td>{{ class_obj.order }}</td>
                                    <td>
                                        {% if class_obj.is_active %}
                                            <span class="badge bg-success">Active</span>
                                        {% else %}
                                            <span class="badge bg-secondary">Inactive</span>
                                        {% endif %}
                                    </td>
                                    <td>
                                        <a href="{% url 'main:student_class_edit' class_obj.id %}" class="btn btn-sm btn-warning">
                                            <i class="fas fa-edit"></i> Edit
                                        </a>
                                        <a href="{% url 'main:student_class_delete' class_obj.id %}" class="btn btn-sm btn-danger">
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
                    <i class="fas fa-graduation-cap fa-3x text-muted mb-3"></i>
                    <h4>No classes found</h4>
                    <p class="text-muted">Add your first class to get started.</p>
                    <a href="{% url 'main:student_class_add' %}" class="btn btn-primary">
                        <i class="fas fa-plus"></i> Add First Class
                    </a>
                </div>
            {% endif %}
        </div>
    </div>
</div>
{% endblock %}
""",

    "student_class_form.html": """{% extends 'main/custom_admin/base.html' %}

{% block title %}{% if class_obj %}Edit{% else %}Add{% endif %} Student Class - Custom Admin{% endblock %}

{% block content %}
<div class="container-fluid">
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h1>{% if class_obj %}Edit Student Class{% else %}Add New Student Class{% endif %}</h1>
        <a href="{% url