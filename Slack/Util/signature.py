import time
import sys
import hmac
import hashlib
import datetime


def verify_slack_signature(event, verification_token):
    if "X-Slack-Request-Timestamp" not in event["headers"] \
        or "X-Slack-Signature" not in event["headers"]:
        raise Exception("Header Invalid")


    timestamp = event["headers"]["X-Slack-Request-Timestamp"]
    signature = event["headers"]["X-Slack-Signature"]

    if abs(time.time() - int(timestamp)) > 60 * 5:
        raise Exception("Timestamp Invalid")

    body = event["body"]
    message = "v0:{}:{}".format(timestamp, body)
    message_bytes = bytes(message, 'UTF-8')
    request_hash = 'v0=' + hmac.new(
        str.encode(verification_token),
        message_bytes,
        hashlib.sha256
    ).hexdigest()

    result = False
    if hasattr(hmac, "compare_digest"):
        if (sys.version_info[0] == 2):
            result = hmac.compare_digest(bytes(request_hash), bytes(signature))
        else:
            result = hmac.compare_digest(request_hash, signature)
    else:
        if len(request_hash) != len(signature):
            raise Exception("Signature invalid")
        result = 0
        if isinstance(request_hash, bytes) and isinstance(signature, bytes):
            for x, y in zip(request_hash, signature):
                result |= x ^ y
        else:
            for x, y in zip(request_hash, signature):
                result |= ord(x) ^ ord(y)
        result = result == 0

    if not result:
        raise Exception("Signature invalid")
    return result
