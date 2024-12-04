import os
import django
import pandas as pd
from django.conf import settings

# Explicitly set the DJANGO_SETTINGS_MODULE before importing models
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "emitra.settings")

# Set up Django environment
django.setup()

from user.models import Location  # Import models after django.setup()

def import_locations_from_excel(file_path):
    # Read Excel file
    df = pd.read_excel(file_path)

    # Use columns 'State Name' and 'District Name (In English)'
    for _, row in df.iterrows():
        state = row['State Name']
        district = row['District Name']

        # Create Location instance and save to database
        Location.objects.create(state=state, district=district)

    print("Import complete.")

# Replace with your actual file path
file_path = "DD.xlsx"
import_locations_from_excel(file_path)
