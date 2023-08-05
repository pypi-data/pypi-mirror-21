"""PubNub REST API access module."""
import time
import requests
import pubnub_blocks_client.endpoints as endpoints
from pubnub_blocks_client.utils import value_for_keypath

# Path to PubNub BLOCKS REST API
PUBNUB_API_URL = "https://admin.pubnub.com/api"
PN_BLOCK_STATE_CHECK_INTERVAL = 1
PN_BLOCK_STATE_CHECK_MAX_COUNT = 30


def authorize(email, password):
    """Start new PubNub block management API access session using provided
    account credentials.

    :type email:     str
    :param email:    Email of account for which REST API calls should be
                     authorized.
    :type password:  str
    :param password: Account's password.

    :rtype:  dict
    :return: Reference on tuple which in case of successful request will
             contain account authorization information as first value. In
             case of failure second tuple value will contain dictionary
             with error description.
    """
    return _request(_endpoint_url(endpoints.authorization()), method='POST',
                    data=dict(email=email, password=password),
                    value_key='result')[:2]


def account(access, account_id):
    """Fetch information about applications / keys which has been created.

    :raise: AuthorizationError in case if not all or wrong credentials has
            been provided. GeneralPubNubError will be raised in case if
            occurred error which is not related to authorization request.

    :type access:      APIAccess
    :param access:     PubNub REST API access information.
    :type account_id:  int
    :param account_id: Reference on unique authorized account identifier
                       for which list of registered applications should be
                       received.

    :rtype:  tuple(dict, dict)
    :return: Reference on tuple which in case of successful request will
             contain list of registered application as first value. In case
             of failure second tuple value will contain dictionary with
             error description.
    """
    return _request(_endpoint_url(endpoints.applications(account_id)),
                    access=access, value_key='result')[:2]


def accounts(access, user_id):
    """Fetch information about accessible PubNub accounts.

    Allow to retrieve list of accounts to which authorized user has access.

    :raise: AuthorizationError in case if not all or wrong credentials has
            been provided. GeneralPubNubError will be raised in case if
            occurred error which is not related to authorization request.

    :type access:   APIAccess
    :param access:  PubNub REST API access information.
    :type user_id:  int
    :param user_id: Reference on unique authorized PubNub user identifier
                    for which accessible accounts list should be received.

    :rtype:  tuple(list, dict)
    :return: Reference on tuple which in case of successful request will
             contain list of accessible accounts as first value. In case
             of failure second tuple value will contain dictionary with
             error description.
    """
    return _request(_endpoint_url(endpoints.user_accounts(user_id)),
                    access=access, value_key='result')[:2]


def blocks(access, keyset_id):
    """Retrieve list of blocks created for keyset.

    :raise: AuthorizationError in case if not all or wrong credentials has
            been provided. GeneralPubNubError will be raised in case if
            occurred error which is not related to authorization request.

    :type access:     APIAccess
    :param access:    PubNub REST API access information.
    :type keyset_id:  int
    :param keyset_id: Reference on unique identifier of application's
                      keyset for which list of blocks should be retrieved.

    :rtype:  tuple(dict, dict)
    :return: Reference on tuple which in case of successful request will
             contain list blocks with event handlers information as first
             value. In case of failure second tuple value will contain
             dictionary with error description.
    """
    return _request(_endpoint_url(endpoints.block(keyset_id=keyset_id)),
                    access=access, value_key='payload')[:2]


def block(access, keyset_id, block_id):
    """Retrieve information about specific block.

    Request allow to get smaller amount of information with request
    performed against concrete block using it's ID.

    :raise: AuthorizationError in case if not all or wrong credentials has
            been provided. GeneralPubNubError will be raised in case if
            occurred error which is not related to authorization request.

    :type access:     APIAccess
    :param access:    PubNub REST API access information.
    :type keyset_id:  int
    :param keyset_id: Reference on unique identifier of keyset for which
                      block should be retrieved.
    :type block_id:   int
    :param block_id:  Reference on unique identifier of block which should
                      be retrieved.

    :rtype:  tuple(dict, dict)
    :return: Reference on tuple which in case of successful request will
             contain dictionary which represent concrete block with event
             handlers information as first value. In case of failure second
             tuple value will contain dictionary with error description.
    """
    return _request(_endpoint_url(endpoints.block(keyset_id=keyset_id,
                                                  block_id=block_id)),
                    access=access, value_key='payload.0')[:2]


def create_block(access, keyset_id, block_payload):
    """Create new block using initial payload.

    New block can be created with minimal block information (name and/
    description).

    :raise: AuthorizationError in case if not all or wrong credentials has
            been provided. GeneralPubNubError will be raised in case if
            occurred error which is not related to authorization request.

    :type access:         APIAccess
    :param access:        PubNub REST API access information.
    :type keyset_id:      int
    :param keyset_id:     Reference on unique identifier of keyset for
                          which new block should be created.
    :type block_payload:  dict
    :param block_payload: Reference on payload which should be pushed to
                          PubNub REST API to create new block.

    :rtype:  tuple(dict, dict)
    :return: Reference on tuple which in case of successful request will
             contain PubNub service information about created block as
             first value. In case of failure second tuple value will
             contain dictionary with error description.
    """
    # Prepare new block payload
    payload = dict(key_id=keyset_id)
    payload.update(block_payload or dict())

    return _request(_endpoint_url(endpoints.block(keyset_id=keyset_id)),
                    method='POST', access=access, data=payload,
                    value_key='payload')[:2]


def update_block(access, keyset_id, block_id, block_payload):
    """Update block information using data from payload.

    :raise: AuthorizationError in case if not all or wrong credentials has
            been provided. GeneralPubNubError will be raised in case if
            occurred error which is not related to authorization request.

    :type access:         APIAccess
    :param access:        PubNub REST API access information.
    :type keyset_id:      int
    :param keyset_id:     Reference on unique identifier of keyset for
                          which block should be updated.
    :type block_id:       int
    :param block_id:      Reference on unique identifier of block for which
                          changes should be done.
    :type block_payload:  dict
    :param block_payload: Reference on payload which contain changed for
                          block.

    :rtype:  tuple(dict, dict)
    :return: Reference on tuple which in case of successful request will
             contain PubNub service information about updated block as
             first value. In case of failure second tuple value will
             contain dictionary with error description.
    """
    # Prepare new block payload
    payload = dict(key_id=keyset_id, block_id=block_id)
    payload.update(block_payload or dict())
    payload['id'] = block_id

    return _request(_endpoint_url(endpoints.block(keyset_id=keyset_id,
                                                  block_id=block_id)),
                    method='PUT', access=access, data=payload)[:2]


def delete_block(access, keyset_id, block_id):
    """Remove block from keyset.

    :raise: AuthorizationError in case if not all or wrong credentials has
            been provided. GeneralPubNubError will be raised in case if
            occurred error which is not related to authorization request.

    :type access:     APIAccess
    :param access:    PubNub REST API access information.
    :type keyset_id:  int
    :param keyset_id: Reference on unique identifier of keyset from which
                      block should be removed.
    :type block_id:   int
    :param block_id:  Reference on unique identifier of block which should
                      be removed.

    :rtype:  tuple(dict, dict)
    :return: Reference on tuple which in case of successful request will
             contain PubNub service information about block removal as
             first value. In case of failure second tuple value will
             contain dictionary with error description.
    """
    return _request(_endpoint_url(endpoints.block(keyset_id=keyset_id,
                                                  block_id=block_id)),
                    method='DELETE', access=access)[:2]


def start_block(access, keyset_id, block_id, current_state=None):
    """Start target block.

    Client will try to start specific block and verify operation success by
    requesting updated block information.

    :raise: AuthorizationError in case if not all or wrong credentials has
            been provided. GeneralPubNubError will be raised in case if
            occurred error which is not related to authorization request.

    :type access:         APIAccess
    :param access:        PubNub REST API access information.
    :type keyset_id:      int
    :param keyset_id:     Reference on unique identifier of keyset for
                          which block should be started.
    :type block_id:       int
    :param block_id:      Reference on unique identifier of block which
                          should be started.
    :type current_state:  str
    :param current_state: Reference on current block (specified with
                          block_id) state. In case if it reached, change
                          request won't be sent and only wait for
                          transition to new state completion.

    :rtype:  tuple
    :return: Tuple with details of block starting results.
    """
    return _set_block_operation_state(access=access, keyset_id=keyset_id,
                                      block_id=block_id, state='start',
                                      current_state=current_state)


def stop_block(access, keyset_id, block_id, current_state=None):
    """Start target block.

    Client will try to start specific block and verify operation success by
    requesting updated block information.

    :raise: AuthorizationError in case if not all or wrong credentials has
            been provided. GeneralPubNubError will be raised in case if
            occurred error which is not related to authorization request.

    :type access:         APIAccess
    :param access:        PubNub REST API access information.
    :type keyset_id:      int
    :param keyset_id:     Reference on unique identifier of keyset from
                          which block should be stopped.
    :type block_id:       int
    :param block_id:      Reference on unique identifier of block which
                          should be stopped.
    :type current_state:  str
    :param current_state: Reference on current block (specified with
                          block_id) state. In case if it reached, change
                          request won't be sent and only wait for
                          transition to new state completion.

    :rtype:  tuple
    :return: Tuple with details of block stopping results.
    """
    return _set_block_operation_state(access=access, keyset_id=keyset_id,
                                      block_id=block_id, state='stop',
                                      current_state=current_state)


def _set_block_operation_state(access, keyset_id, block_id, state,
                               current_state=None):
    """Update current block's operation state.

    Depending from requested state block can be stopped or started.

    :raise: AuthorizationError in case if not all or wrong credentials has
            been provided. GeneralPubNubError will be raised in case if
            occurred error which is not related to authorization request.

    :type access:         APIAccess
    :param access:        PubNub REST API access information.
    :type keyset_id:      int
    :param keyset_id:     Reference on unique identifier of keyset from
                          which block should be removed.
    :type block_id:       int
    :param block_id:      Reference on unique identifier of block which
                          should be removed.
    :type state:          str
    :param state:         Reference on new block state to which it should
                          be switched.
    :type current_state:  str
    :param current_state: Reference on current block (specified with
                          block_id) state. In case if it reached, change
                          request won't be sent and only wait for
                          transition to new state completion.

    :rtype:  tuple(bool, str, str)
    :return: Tuple with details of block operation state change.
    """
    final_state = 'running' if state == 'start' else 'stopped'
    in_transition = current_state is not None and current_state == final_state
    response = None
    result = [False, None, None]
    info = None
    if not in_transition:
        url = _endpoint_url(endpoints.block_state(keyset_id=keyset_id,
                                                  block_id=block_id,
                                                  state=state))
        response, _, info = _request(url, method='POST', access=access,
                                     data=dict(block_id=block_id))

    if info and info['status'] != 409 or in_transition:
        result[0] = _wait_for_block_state_change(access=access,
                                                 keyset_id=keyset_id,
                                                 block_id=block_id)
    else:
        result[1] = value_for_keypath(response, 'message.text')
        result[2] = value_for_keypath(response, 'message.stack',
                                      default='Not available')

    return tuple(result)


def _wait_for_block_state_change(access, keyset_id, block_id):
    """Wait for block state transition to intended.

    Perform state request with delays till number of retry won't reach
    specified limit or state will be changed.

    :raise: AuthorizationError in case if not all or wrong credentials has
            been provided. GeneralPubNubError will be raised in case if
            occurred error which is not related to authorization request.

    :type access:         APIAccess
    :param access:        PubNub REST API access information.
    :type keyset_id:      int
    :param keyset_id:     Reference on unique identifier of keyset from
                          which block should be removed.
    :type block_id:       int
    :param block_id:      Reference on unique identifier of block which
                          should be removed.

    :rtype:  bool
    :return: 'True' in case if block didn't changed it's state in time and
             process completed with timeout error.
    """
    timeout = False
    check_count = 0
    block_data, error = block(access=access, keyset_id=keyset_id,
                              block_id=block_id)

    # Block require some time to change it's state, so this while loop
    # will check it few times after specified interval. In case if
    # after fixed iterations count state still won't be same as
    # requested it will report error.
    while (block_data['state'] != block_data['intended_state']
           and error is None):
        check_count += 1
        if check_count != PN_BLOCK_STATE_CHECK_MAX_COUNT:
            time.sleep(PN_BLOCK_STATE_CHECK_INTERVAL)
            block_data, error = block(access=access, keyset_id=keyset_id,
                                      block_id=block_id)
        else:
            timeout = True
            break

    return timeout


def create_event_handler(access, keyset_id, payload):
    """Create new event handler for block.

    :raise: AuthorizationError in case if not all or wrong credentials has
            been provided. GeneralPubNubError will be raised in case if
            occurred error which is not related to authorization request.

    :type access:     APIAccess
    :param access:    PubNub REST API access information.
    :type keyset_id:  int
    :param keyset_id: Reference on unique identifier of keyset for which
                      event handler should be created for target block.
    :type payload:    dict
    :param payload:   Reference on new event handler payload.

    :rtype:  tuple(dict, dict)
    :return: Reference on tuple which in case of successful request will
             contain PubNub service information about created event handler
             as first value. In case of failure second tuple value will
             contain dictionary with error description.
    """
    url = _endpoint_url(endpoints.event_handler(keyset_id=keyset_id))

    return _request(url, method='POST', access=access, data=payload,
                    value_key='payload')[:2]


def update_event_handler(access, keyset_id, handler_id, payload):
    """Update event handler's event data.

    Use provided information to update event handler behaviour and data
    processing flow (handler code).

    :raise: AuthorizationError in case if not all or wrong credentials has
            been provided. GeneralPubNubError will be raised in case if
            occurred error which is not related to authorization request.

    :type access:      APIAccess
    :param access:     PubNub REST API access information.
    :type keyset_id:   int
    :param keyset_id:  Reference on unique identifier of keyset for which
                       event handler data should be updated.
    :type handler_id:  int
    :param handler_id: Reference on unique identifier of event handler
                       which should be updated.
    :type payload:     dict
    :param payload:    Reference on updated event handler payload.

    :rtype:  tuple(dict, dict)
    :return: Reference on tuple which in case of successful request will
             contain PubNub service information about updated event handler
             as first value. In case of failure second tuple value will
             contain dictionary with error description.
    """
    # Append handler identifier to payload.
    payload['id'] = handler_id
    url = _endpoint_url(endpoints.event_handler(keyset_id=keyset_id,
                                                handler_id=handler_id))

    return _request(url, method='PUT', access=access, data=payload)[:2]


def delete_event_handler(access, keyset_id, handler_id):
    """Remove event handler from target block.

    :raise: AuthorizationError in case if not all or wrong credentials has
            been provided. GeneralPubNubError will be raised in case if
            occurred error which is not related to authorization request.

    :type access:      APIAccess
    :param access:     PubNub REST API access information.
    :type keyset_id:   int
    :param keyset_id:  Reference on unique identifier of keyset from which
                       event handler data should be removed.
    :type handler_id:  int
    :param handler_id: Reference on unique identifier of event handler
                       which should be removed.

    :rtype:  tuple(dict, dict)
    :return: Reference on tuple which in case of successful request will
             contain PubNub service information about event handler removal
             as first value. In case of failure second tuple value will
             contain dictionary with error description.
    """
    url = _endpoint_url(endpoints.event_handler(keyset_id=keyset_id,
                                                handler_id=handler_id))

    return _request(url, method='DELETE', access=access)[:2]


def _endpoint_url(endpoint):
    """Merge API endpoint path with PubNub REST API base URL.

    :type endpoint:  str
    :param endpoint: Reference to one of endpoint paths.

    :rtype:  str
    :return: Composed REST API call url.
    """
    return "{0}{1}".format(PUBNUB_API_URL, endpoint)


def _request(url, method='GET', data=None, access=None, **kwargs):
    """Perform actual request using provided information.

    :raise: AuthorizationError in case if not all or wrong credentials has
            been provided. GeneralPubNubError will be raised in case if
            occurred error which is not related to authorization request.

    :type url:        str
    :param url:       Reference on full REST API url which should be
                      called.
    :type method:     str
    :param method:    Reference on one of available methods: GET, POST,
                      PUT, DELETE.
    :type data:       dict | None
    :param data:      Reference on object which should be sent along with
                      POST or PUT requests.
    :type access:     APIAccess | None
    :param access:    PubNub REST API access information.
    :type value_key:  str | None
    :param value_key: Reference on name of key under which stored value
                      which should be returned in case of successful
                      request processing.

    :rtype:  tuple(dict, dict, dict)
    :return: Reference on tuple which in case of successful processing as
             first element will contain service response. In case of
             failure second tuple element will contain error description.
    """
    value_key = kwargs.get('value_key')
    reset_access_token = kwargs.get('reset_access_token', False)
    retry_count = kwargs.get('retry_count', 1)

    headers = {'Accept': 'application/json', 'Accept-Encoding': 'gzip,deflate'}
    if access:
        headers['X-Session-Token'] = access.token(expired=reset_access_token)
    if data is not None:
        headers['Content-Type'] = 'application/json'
    response = requests.request(method, url, json=data, headers=headers)
    response_inf = dict(status=response.status_code, headers=response.headers,
                        url=response.url)
    if 200 <= response.status_code < 400:
        value = response.json()
        if value_key is not None:
            value = value_for_keypath(value, keypath=value_key)
        service_response = tuple([value, None, response_inf])
    else:
        error = response.json()
        error['url'] = response.url
        if 'code' not in error:
            error['code'] = response.status_code
        service_response = tuple([None, error, response_inf])

    if service_response[1] is not None and retry_count > 0:
        reset_access_token = service_response[1]['code'] == 403
        kwargs['reset_access_token'] = reset_access_token
        kwargs['retry_count'] = retry_count - 1
        service_response = _request(url=url, method=method, data=data,
                                    access=access, **kwargs)

    return service_response
