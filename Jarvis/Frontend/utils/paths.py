import os

class Paths:
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    @classmethod
    def get_path(cls, *paths):
        """Get absolute path from project root"""
        return os.path.join(cls.BASE_DIR, *paths)
    
    @classmethod
    def ensure_dir(cls, *paths):
        """Ensure directory exists"""
        path = cls.get_path(*paths)
        os.makedirs(path, exist_ok=True)
        return path

    # Commonly used paths
    DATA_DIR = os.path.join(BASE_DIR, 'Data')
    FRONTEND_FILES = os.path.join(BASE_DIR, 'Frontend', 'Files')
    GRAPHICS_CACHE = os.path.join(BASE_DIR, 'Frontend', 'Graphics', 'cache')
    
    # File paths
    MIC_STATUS = os.path.join(FRONTEND_FILES, 'Mic.data')
    ASSISTANT_STATUS = os.path.join(FRONTEND_FILES, 'Status.data')
    RESPONSES = os.path.join(FRONTEND_FILES, 'Responses.data')
    IMAGE_GEN = os.path.join(FRONTEND_FILES, 'ImageGeneration.data')
    CHAT_LOG = os.path.join(DATA_DIR, 'ChatLog.json') 