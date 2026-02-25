import io
import os
from supabase import Client
import mimetypes

DEBUG_SAVE_DIR = "/tmp/tmp_uploads"
os.makedirs(DEBUG_SAVE_DIR, exist_ok=True)

class StorageRepository:
    def __init__(self, db_client: Client, bucket: str):
        self.db_client = db_client
        self.bucket = bucket

    def upload_photos(self, folder: str, photos: list) -> list[str]:
        urls = []
        for photo in photos:
            print(f"IMAGEN: {photo}")
            print(f"NOMBRE DE LA IMAGEN: {photo['filename']}")

            if photo["filename"] and photo["content"]:
                temp_path = os.path.join(DEBUG_SAVE_DIR, photo["filename"])
                with open(temp_path, "wb") as f:
                    f.write(photo["content"])
                print(f"[DEBUG] Guardada imagen temporal: {temp_path}")

            path = f'{folder}/{photo["filename"]}'

            mime_type, _ = mimetypes.guess_type(photo["filename"])
            if not mime_type:
                mime_type = "application/octet-stream"


            urls.append(self.db_client.storage.from_(self.bucket).get_public_url(path))

        return urls
