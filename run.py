from app import JarvisAssistant
from config import GOOGLE_JSON_CREDENTIALS

if __name__ == "__main__":
    JarvisAssistant(str(GOOGLE_JSON_CREDENTIALS)).run()
