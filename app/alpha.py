
import os
from dotenv import load_dotenv

load_dotenv() #> invoking this function loads contents of the ".env" file into the script's environment...

ODDS_API_KEY = os.getenv("97f1ced329ee20e60eb41602c56495b9")