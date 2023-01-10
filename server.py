import logging
from waitress import serve

from my_notes_project.wsgi import application

logger = logging.getLogger('waitress')
logger.setLevel(logging.INFO)

if __name__ == '__main__':
    serve(application, port='80')
