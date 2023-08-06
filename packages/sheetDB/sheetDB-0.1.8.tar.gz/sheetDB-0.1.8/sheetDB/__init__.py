"""

sheetDB
~~~~~~~~~~

Google Sheets as a backend

"""

__version__ = '0.1.8'
__author__ = 'knyte'

from .credentials import Credentials
from .database import Database
from .table import Table, POSITIVE, NEGATIVE
