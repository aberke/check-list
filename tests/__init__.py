
import os

# Set ENVIRONMENT=TESTING before loading any packages so that they load with the TESTING configuration
# config.py checks environment variable ENVIRONMENT for setting: MONGODB_DB,
os.environ["ENVIRONMENT"] = "TESTING"