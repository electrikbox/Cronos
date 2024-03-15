from Cronos_core.models import *


# TEMPORARY TOKEN (reset pwd + activation)
# =============================================================================

class PasswordTemporaryToken(models.Model):
    """ Class for temporary password reset token  """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    change_pwd_token = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(default=timezone.now)
    expires_at = models.DateTimeField()

    def save(self, *args, **kwargs):
        """ Generate a token if not exists & set the expiration date """
        if not self.change_pwd_token:
            self.change_pwd_token = secrets.token_urlsafe(32)

        if not self.expires_at:
            self.expires_at = timezone.now() + datetime.timedelta(minutes=2)  # modif ici le délai
        super().save(*args, **kwargs)

    def is_valid(self):
        """ Check if token is valid  """
        return timezone.now() <= self.expires_at


# TEMPORARY TOKEN (activation)
# =============================================================================

class ActivationTemporaryToken(models.Model):
    """ Class for activation temporary token  """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    activation_token = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(default=timezone.now)
    expires_at = models.DateTimeField()

    def save(self, *args, **kwargs):
        """ Generate a token if not exists & set the expiration date """
        if not self.activation_token:
            self.activation_token = secrets.token_urlsafe(32)

        if not self.expires_at:
            self.expires_at = timezone.now() + datetime.timedelta(hours=2)  # modif ici le délai
        super().save(*args, **kwargs)

    def is_valid(self):
        """ Check if token is valid  """
        return timezone.now() <= self.expires_at
