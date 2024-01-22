import os


class config:
    # Get the current working directory to place sched.db during development.
    # In production, use absolute paths or a database management system.
    PWD = os.path.abspath(os.curdir)
    
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:////home/lawson/Documents/Projet_Flask/sched/sched.db'.format(PWD)
   # SECRET_KEY = 'secret222'  # Create your own.
    #SESSION_PROTECTION = 'strong'
