# Noagaon High School Website

A modern, responsive school website built with Django, HTML, and Tailwind CSS.

## Features

- **Homepage**: School information, logo, and latest notices
- **Notices Section**: Paginated notices (PDF upload or text content) with dual functionality
- **Teachers Page**: Paginated teacher profiles with photos and information
- **Headmaster Page**: Dedicated page for headmaster profile and message
- **Managing Committee**: Committee member profiles and information
- **Contact Page**: Contact information and contact form
- **School Branding**: Dynamic school logo and information management
- **Admin Panel**: Django admin for managing all content

## Technology Stack

- **Backend**: Django 5.2.4
- **Frontend**: HTML5, Tailwind CSS
- **Database**: SQLite (default)
- **File Handling**: Pillow for image processing

## Installation & Setup

1. **Clone and navigate to the project**:
   ```bash
   cd /path/to/school
   ```

2. **Activate virtual environment**:
   ```bash
   source venv/bin/activate
   ```

3. **Install dependencies** (already installed):
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations** (already done):
   ```bash
   python manage.py migrate
   ```

5. **Create superuser** (already created - username: admin):
   ```bash
   python manage.py createsuperuser
   ```

6. **Populate sample data** (already done):
   ```bash
   python manage.py populate_sample_data
   ```

7. **Run the development server**:
   ```bash
   python manage.py runserver
   ```

8. **Access the website**:
   - Main site: http://127.0.0.1:8000/
   - Admin panel: http://127.0.0.1:8000/admin/

## Admin Credentials

- **Username**: admin
- **Password**: 123 (change this in production!)

## Usage

### Admin Panel Features

1. **Notices Management**:
   - Upload PDF notices
   - Set notice titles and dates
   - Automatic creator tracking

2. **Teachers Management**:
   - Add teacher profiles
   - Upload teacher photos
   - Set subjects and designations

3. **Committee Management**:
   - Add committee members
   - Set roles and order
   - Upload member photos

### Website Features

- **Responsive Design**: Works on all devices
- **Pagination**: Notices (10 per page), Teachers (8 per page)
- **File Downloads**: Direct PDF downloads for notices
- **Clean UI**: Modern Tailwind CSS styling

## File Structure

```
school/
├── main/                   # Main Django app
│   ├── models.py          # Database models
│   ├── views.py           # View functions
│   ├── admin.py           # Admin configuration
│   └── urls.py            # URL patterns
├── templates/             # HTML templates
│   ├── base.html          # Base template
│   └── main/              # App-specific templates
├── static/                # Static files (CSS, JS)
├── media/                 # User uploads
└── school_website/        # Django project settings
```

## Customization

1. **School Information**: Edit templates to update school name, logo, and contact details
2. **Colors**: Modify Tailwind CSS classes in templates
3. **Pagination**: Adjust items per page in views.py
4. **Upload Paths**: Modify upload_to paths in models.py

## Production Deployment

Before deploying to production:

1. Set `DEBUG = False` in settings.py
2. Configure proper database (PostgreSQL recommended)
3. Set up static file serving
4. Configure media file serving
5. Use environment variables for sensitive settings
6. Set up proper email backend for contact forms

## Next Steps

- Implement contact form functionality
- Add search functionality for notices and teachers
- Add user authentication for protected areas
- Implement email notifications
- Add more content management features