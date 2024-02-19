from Cronos_core.models import *


class UserPic():
    """ Class User profile picture """

    def __init__(self, user):
        """ Initialize user profile picture """
        self.user = user

    def upload_pic(self, pic):
        """ Upload user profile picture """

        _, file_extension = os.path.splitext(pic.name)

        filename = f"{self.user.id}{file_extension.lower()}"
        filepath = os.path.join(settings.MEDIA_ROOT, filename)

        with open(filepath, 'wb') as f:
            for chunk in pic.chunks():
                f.write(chunk)

        return filename

    def show_pic(self):
        """ Show user profile picture """

        filepath = os.path.join(settings.MEDIA_ROOT)

        for file in os.listdir(filepath):
            user_id = file.split('.')[0]
            ext = file.split('.')[1]

            if user_id == str(self.user.id):
                pic = f"{user_id}.{ext}"

        image_url = settings.MEDIA_URL + pic

        return image_url
