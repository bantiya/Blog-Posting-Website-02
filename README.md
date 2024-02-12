# Blog Post Website

This repository contains the code for a Blog Post website built with Python's Flask framework. The website allows users to create, read, update, and delete blog posts. Additionally, users can register, login, and leave comments on posts.

## Features

- User authentication (register, login, logout)
- Create, read, update, and delete blog posts
- Comment on posts
- Rich text editor for post content
- Responsive design

## Prerequisites

Before you begin, ensure you have met the following requirements:
- Python 3.8 or higher
- pip (Python package installer)

## Installation

Follow these steps to get your development env running:

1. Clone the repository to your local machine: ```git clone https://github.com/bantiya/Blog-Posting-Website-01.git```

2. Navigate to the project directory:

3. Install the requirements.
   
## Setting Up the Database

This project uses SQLite by default. If you wish to use another database, configure the `DATABASES` setting in `settings.py` according to your database choice.

Run the following commands to create your database tables:

python manage.py makemigrations
python manage.py migrate


## Running the Server

To start the Django development server, run: ```python manage.py runserver```

Open a web browser and go to `http://127.0.0.1:8000/` to view the website.

## Admin Panel

To create an admin user to manage blog posts and comments through the Django admin interface, run: ```python manage.py createsuperuser```

Follow the prompts to create your superuser. You can then log in to the admin panel by navigating to `http://127.0.0.1:8000/admin/`.

## Contributing

Contributions are welcome! For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
