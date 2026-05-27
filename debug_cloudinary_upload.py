import os
import cloudinary
import cloudinary.uploader

cloudinary.config(
    cloud_name="ddq299bju",
    api_key="599189223837844",
    api_secret="hKYrwwL-cG2gQ2b-ui7bZlONcyA"
)

MEDIA_ROOT = "media"

for root, dirs, files in os.walk(MEDIA_ROOT):

    for file in files:

        file_path = os.path.join(root, file)

        # create cloudinary folder structure
        cloud_folder = root.replace("\\", "/")

        try:

            print(f"Uploading: {file_path}")

            response = cloudinary.uploader.upload(
                file_path,
                folder=cloud_folder
            )

            print("SUCCESS")
            print(response['secure_url'])

        except Exception as e:

            print("FAILED")
            print(e)