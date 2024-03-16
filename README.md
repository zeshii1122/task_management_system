<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Django-User_Authentication</title>
</head>
<body>

<h1>Django-User_Authentication</h1>

<p>Full user authentication system implemented in Django 2.1 and Bootstrap.</p>

<h2>Installing</h2>

<p>Open terminal and clone the repository:</p>

<pre><code>git clone https://github.com/devmahmud/Django-User_Authentication.git</code></pre>

<h4>or simply download using the url below</h4>

<code>https://github.com/devmahmud/Django-User_Authentication.git</code>

- Go to the project directory

```bash
cd task-manager
```

- Create a virtual environment

```bash
python3 -m venv venv
```

- Activate the virtual environment

```bash
source venv/bin/activate
```

- Install the dependencies

```bash
pip3 install -r requirements.txt
```

<h2>Database Migration</h2>

<p>To migrate the database, open a terminal in the project directory and run:</p>

<pre><code>python manage.py makemigrations
python manage.py migrate
</code></pre>

<h2>Email Settings for Password Reset</h2>

<p>Fill up the following information in your project settings for password reset functionality via email:</p>

<pre><code>EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'example@gmail.com'
EMAIL_HOST_PASSWORD = 'your_email_password'
</code></pre>

<h2>Running the Project</h2>

<h3>Ubuntu/Mac</h3>

<p>Replace <code>/path/to/your/virtualenv/bin/activate</code> with the actual path to your virtual environment's activation script.</p>

<p>Make the script executable:</p>

<pre><code>chmod +x run_apps.sh</code></pre>

<p>Run the script:</p>

<pre><code>run_apps.sh</code></pre>

<h3>Windows</h3>

<p>Replace <code>C:\path\to\your\virtualenv\Scripts\activate</code> with the actual path to your virtual environment's activation script.</p>

<p>Double-click <code>run_apps.bat</code> to run the batch file.</p>

<h2>Author</h2>
<blockquote>
  Muhammad Zeeshan Tariq<br>
  Email: muhammadzeeshantariq1@gmail.com
</blockquote>

</body>
</html>
