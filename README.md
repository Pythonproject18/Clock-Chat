# Clock-Chat

# git clone from :

=> git clone https://github.com/Pythonproject18/Clock-Chat.git

# for enter into folder:

=> cd Clock-Chat

# create a virtual environment :

=> python -m venv venv

# Activate scripts :

=> venv/scripts/activate
<<<<<<< HEAD
=======

>>>>>>> d2d88cb779eca0185a2ec56227852055190157b1
# Install Requirements :

=> pip install -r requirements.txt

# Make migrations:

=> python manage.py makemigrations CLOCK_CHAT

    => python manage.py migrate

    (if having some error of psycopg2 then )

        =>pip install psycopg2 binary

    # redo :

    => python manage.py makemigrations CLOCK_CHAT

        => python manage.py migrate

# open runserver:

=> python manage.py runserver
<<<<<<< HEAD

=======
>>>>>>> d2d88cb779eca0185a2ec56227852055190157b1
