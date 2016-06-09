from monkey import settings
from .. import recaptcha as captcha


class Recaptcha(object):
    """
    Provides captcha protection
    https://www.google.com/recaptcha
    """
    def __init__(self, controller):
        self.controller = controller
        self.controller.events.before_render += self._gen_html_code

    def _gen_html_code(self, controller, *args, **kwargs):
        chtml = captcha.displayhtml(
          public_key=settings.get('recaptcha_site_key'),
          use_ssl=(controller.request.scheme == 'https'),
          error=None)
        if settings.get('recaptcha_site_key') == "" or \
            settings.get('recaptcha_secret_key') == "":
          chtml = '<div class="alert alert-danger"><strong>Error</strong>: You have to ' \
              '<a href="http://www.google.com/recaptcha/whyrecaptcha" target="_blank">sign up ' \
              'for API keys</a> in order to use reCAPTCHA.</div>' \
              '<input type="hidden" name="recaptcha_challenge_field" value="manual_challenge" />' \
              '<input type="hidden" name="recaptcha_response_field" value="manual_challenge" />'

        controller.context['captcha_html'] = chtml


def require_captcha_for_post(controller):
    """
    Returns True if the request method is POST and the captcha challenge was successful, otherwise returns False.
    """
    if controller.request.method == 'POST' and not controller.request.path.startswith('/taskqueue'):

        # check captcha
        challenge = controller.request.POST.get('recaptcha_challenge_field')
        response = controller.request.POST.get('recaptcha_response_field')
        remoteip = controller.request.remote_addr

        cResponse = captcha.submit(
          challenge,
          response,
          settings.get('recaptcha_secret_key'),
          remoteip)

        if not cResponse.is_valid:
            return (False, 'Wrong image verification code.')

    return True