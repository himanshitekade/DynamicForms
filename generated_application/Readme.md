NOTE: 
      1) DYNAMIC FORMS CURRENTLY SUPPORTS PYTHON 3.9 & above
      2) DYNAMIC FORMS CURRENTLY SUPPORTS DJANGO 4.0 & above
      3) FOLLOW ALL THE STEPS GIVEN BELOW
      4) FOLLOW ALL #TO DO FROM views.py file.
     

Step 1: INSTALLATION

        If the requirements.txt already exists in your project then just copy the content from the requirements.txt provided in zip folder to your requirements.txt and if not just install it using ("pip3 install -r requirements.txt")

Step 2: DATA COPYING

       A) If you are working on fresh project just copy all the files from zip Extracted Folder to your django application except form_jsons folder.

        if not then just --> Copy the content of models.py, views.py , urls.py to respective .py files.

       B) If templates folder already exists in your application then just copy html files to your templates folder.

       C) If static folder already exists in your application, then check your static folder containing files and zip extracted static containing files are same or not, if not then copy the required files to your static folder.

Step 3: DJANGO CONFIGURATIONS

        Go to settings.py and add this line ----> 
        from decouple import config (if does not exists) 

        Go to settings.py ----> TEMPLATES
        Paste the 
            'builtins': [
                '<your application name>.templatetags.custom_tags',
            ]

                TEMPLATES = [
            {
                'BACKEND': 'django.template.backends.django.DjangoTemplates',
                'DIRS': [],
                'APP_DIRS': True,
                'OPTIONS': {
                    'context_processors': [
                        'django.template.context_processors.debug',
                        'django.template.context_processors.request',
                        'django.contrib.auth.context_processors.auth',
                        'django.contrib.messages.context_processors.messages',
                    ],
                    
                <----------------- HERE ------------------->    

                },
            },
        ]

Step 4: JSON FILE FOLDER
 
        Copy the form_jsons folder to your main directory (Folder which contains manage.py), if it does not exist.

Step 5: URLS
        Copy the urls.py file to your application and add your application name
        (from <your application name> import views)
        (if urls.py already exists then just copy the url)

Step 6: MIGRATIONS

        Run migrations using (python manage.py makemigrations and then migrate)

