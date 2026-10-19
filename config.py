import os
BASE_URL = os.getenv("STELLAR_URL", "https://stellarburgers.education-services.ru").rstrip("/")
REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "20"))
