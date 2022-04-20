""" A very simple AWS Lambda function responding to HTTP GET requests
https://h7avjhz2p2.execute-api.us-west-2.amazonaws.com/Prod/odd?8
"""

import json
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def lambda_handler(event, context) -> dict:
    """
    :param event: input data, usually a dict, but can also be list, str, int, float, or NoneType type.
    :param context: object providing information about invocation, function, and execution environment
    :return: dict with http header, status code, and body
    """
    if not event.get('httpMethod') or 'GET' != event['httpMethod']:  # maybe invoked directly not through Gateway
        return {"status_code": 400, "message": "Bad Request"}
    logger.info(json.dumps(event))
    status_code, content = get(event['path'], event['queryStringParameters'])
    return {
        "statusCode": status_code,
        "headers": {'Content-Type': 'application/json; charset=UTF-8'},
        "body": json.dumps(content)
    }


def get(file_path: str, params: dict) -> (int, dict):
    """
    This function will do the work
    :param file_path: will be interpreted as what needs to be done
    :param params: function arguments
    :return: HTTP code, dict with results
    """
    d = {}
    try:
        function_name = file_path.split("/")[-1]
        d["function"] = function_name
        if 'odd' == function_name:
            x = list(params.keys()).pop(0)
            d["argument"] = x
            if x:
                d["result"] = int(x) % 2 == 1
                status_code = 200
            else:
                d["message"] = "bad request"
                status_code = 400
        else:
            d["message"] = "bad request"
            status_code = 400
    except Exception as e:
        d["error"] = str(e)
        status_code = 500
    return status_code, d
