import json
from six.moves import urllib

from ecsclient.common import error_codes


class ECSClientException(Exception):
    """
    This is a custom ECSClientException Exception class to better handle
    errors that ECSClientException can return in HTML format rather than JSON.
    It includes the original error message from ECS (ecs_message) and the
    HTTP status code returned (http_status_code).
    """

    def __init__(self, message, ecs_code=None, ecs_retryable=None, ecs_description='',
                 ecs_details='', http_scheme='', http_host='', http_port='',
                 http_path='', http_query='', http_status=None, http_reason='',
                 http_response_content='', http_response_headers=None):
        """
        This is a custom ECSClientException class to handle API error responses
        """
        super(ECSClientException, self).__init__(message)
        self.message = message
        self.ecs_code = ecs_code
        self.ecs_retryable = ecs_retryable
        self.ecs_description = ecs_description
        self.ecs_details = ecs_details
        self.http_scheme = http_scheme
        self.http_host = http_host
        self.http_port = http_port
        self.http_path = http_path
        self.http_query = http_query
        self.http_status = http_status
        self.http_reason = http_reason
        self.http_response_content = http_response_content
        self.http_response_headers = http_response_headers

    @classmethod
    def from_response(cls, resp, message=None):
        code = None
        retryable = None
        description = ''
        details = ''
        try:
            m = json.loads(resp.text)
            code = m.get('code', None)
            retryable = m.get('retryable', None)
            description = m.get('description', '')
            details = m.get('details', '')
        except:
            pass

        parsed_url = urllib.parse.urlparse(resp.request.url)
        message = message or details or description or error_codes.ERROR_CODES.get(code) or '%s %s' % (
                  resp.status_code, resp.reason)

        return cls(message,
                   ecs_code=code,
                   ecs_retryable=retryable,
                   ecs_description=description,
                   ecs_details=details,
                   http_scheme=parsed_url.scheme,
                   http_host=parsed_url.hostname,
                   http_port=parsed_url.port,
                   http_path=parsed_url.path,
                   http_query=parsed_url.query,
                   http_status=resp.status_code,
                   http_reason=resp.reason,
                   http_response_content=resp.text or resp.content,
                   http_response_headers=resp.headers)

    def __str__(self):
        a = self.message
        if self.ecs_details not in a:
            a += ' - %s' % self.ecs_details
        if self.ecs_description not in a:
            a += ' - %s' % self.ecs_description
        b = ''
        if self.http_scheme:
            b += '%s://' % self.http_scheme
        if self.http_host:
            b += self.http_host
        if self.http_port:
            b += ':%s' % self.http_port
        if self.http_path:
            b += self.http_path
        if self.http_query:
            b += '?%s' % self.http_query
        if self.http_status:
            if b:
                b = '%s %s' % (b, self.http_status)
            else:
                b = str(self.http_status)
        if self.http_reason:
            if b:
                b = '%s %s' % (b, self.http_reason)
            else:
                b = '- %s' % self.http_reason
        if self.http_response_content:
            if len(self.http_response_content) <= 60:
                b += '   %s' % self.http_response_content
            else:
                b += '  [first 60 chars of response] %s' \
                     % self.http_response_content[:60]
        return b and '%s: %s' % (a, b) or a
