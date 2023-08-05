import json

import pytest

from lambda_utils.api_gateway import ApiGateway
from lambda_utils.exceptions import *


@ApiGateway()
def function(event, context):
    return event



def test_successful_response(event, context):
    result = function(event, context)

    assert result['statusCode'] == 200
    assert json.loads(result['body']) == event


@pytest.mark.parametrize('body', [{}, None, '{}'])
def test_content_type_application_json(event, context, body):
    event['body'] = body
    event['headers']['Content-Type'] = 'application/json'

    result = function(event, context)

    event['body'] = {}
    assert json.loads(result['body']) == event

@pytest.mark.parametrize('body', [{}, None, '{}'])
def test_content_type_missing(event, context, body):
    event['body'] = body
    del event['headers']['Content-Type']

    result = function(event, context)

    assert json.loads(result['body'])['body'] == body

@pytest.mark.parametrize('body', [{}, None, '{}'])
def test_content_type_application_json_and_charset(event, context, body):
    event['body'] = body
    event['headers']['Content-Type'] = 'application/json; charset=utf-8;'

    result = function(event, context)

    event['body'] = {}
    assert json.loads(result['body']) == event



def test_content_type_application_x_www_form_urlencoded_empty(event, context):
    event['body'] = None
    event['headers']['Content-Type'] = 'application/x-www-form-urlencoded'

    result = function(event, context)

    event['body'] = {}
    assert json.loads(result['body']) == event


def test_content_type_application_x_www_form_urlencoded(event, context):
    event['body'] = 'string=a&empty&special=%21%40J%23%3ALOIJ'
    event['headers']['Content-Type'] = 'application/x-www-form-urlencoded'

    result = function(event, context)

    body = json.loads(result['body'])['body']
    assert body['string'] == ['a']
    assert body['empty'] == ['']
    assert body['special'] == [u'!@J#:LOIJ']


def test_access_control_allow_origion_header_is_set(event, context):
    result = function(event, context)

    assert result['headers']['Access-Control-Allow-Origin'] == "*"


@pytest.mark.parametrize('exception', [
    BadRequest, Unauthorized, Forbidden, NotFound, MethodNotAllowed, NotAcceptable, RequestTimeout, Conflict, Gone, LengthRequired, PreconditionFailed,
    RequestEntityTooLarge, RequestURITooLarge, UnsupportedMediaType, RequestedRangeNotSatisfiable, ExpectationFailed, UnprocessableEntity,
    PreconditionRequired, TooManyRequests, RequestHeaderFieldsTooLarge, InternalServerError, BadGateway, ServiceUnavailable, HTTPVersionNotSupported
])
def test_http_exception(event, context, exception):
    @ApiGateway()
    def function(event, context):
        raise exception()

    result = function(event, context)

    assert result['statusCode'] == exception.code
    assert result['body'] == HTTP_STATUS_CODES.get(exception.code)
