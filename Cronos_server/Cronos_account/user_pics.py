from Cronos_core.models import *
from PIL import Image, ImageOps
import glob


class UserPic():
    """ Class User profile picture """

    def __init__(self, user: User):
        """ Initialize user profile picture """
        self.user = user

    # UPLOAD USER PROFILE PICTURE
    # =========================================================================

    def upload_pic(self, pic):
        """ Upload user profile picture """
        _, file_extension = os.path.splitext(pic.name)

        filename = f"{self.user.id}{file_extension.lower()}"

        # Dir when user profile pictures are stored
        filepath = os.path.join(settings.MEDIA_ROOT + '/user_pic/', filename)

        # Rename pic with user id
        filename_no_ext = f"{self.user.id}"
        existing_files = glob.glob(f"{settings.MEDIA_ROOT}'/user_pic'/{filename_no_ext}.*")

        # Replace file if already exists
        for existing_file in existing_files:
            os.remove(existing_file)

        resized_img = self.resize_pic(pic)

        with open(filepath, 'wb') as f:
            resized_img.save(f)

        return filename

    # SHOW USER PROFILE PICTURE
    # =========================================================================

    def show_pic(self):
        """ Show user profile picture """
        filepath = os.path.join(settings.MEDIA_ROOT + '/user_pic')
        search_file = f"{filepath}/{self.user.id}".split('.')[0]

        # Display default pic if user has not uploaded any
        if not any(glob.glob(f"{search_file}.*")):
            pic = 'default_pic.png'
            return settings.MEDIA_URL + 'user_pic/' + pic

        for file in os.listdir(filepath):
            user_id = file.split('.')[0]
            ext = file.split('.')[1]

            if user_id == str(self.user.id):
                pic = f"{user_id}.{ext}"
                break

        image_url = settings.MEDIA_URL + 'user_pic/' + pic

        return image_url

    # RESIZE USER PROFILE PICTURE
    # =========================================================================

    @staticmethod
    def resize_pic(pic, size=200):
        """ Resize user profile picture """
        img = Image.open(pic)
        img_width, img_height = img.size
        aspect_ratio = img_width / img_height

        # Square size
        if img_width > img_height:
            new_width = size
            new_height = int(size / aspect_ratio)
        else:
            new_height = size
            new_width = int(size * aspect_ratio)

        resized_img = img.resize((new_width, new_height))

        # Create a new image with a transparent background if needed
        if img.mode in ('RGBA', 'LA'):
            square_img = Image.new('RGBA', (size, size), (255, 255, 255, 0))
        else:
            square_img = Image.new('RGB', (size, size), (255, 255, 255))

        # Paste the resized image into the center of the square image
        offset = ((size - new_width) // 2, (size - new_height) // 2)
        square_img.paste(resized_img, offset)

        cropped_img = ImageOps.fit(resized_img, (size, size), method=0, bleed=0.0, centering=(0.5, 0.5))

        return cropped_img
