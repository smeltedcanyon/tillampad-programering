
import sys
from os import environ
op = environ.get('OS','okänd')



for item in environ:
    print(item + ': ' + environ.get(item))