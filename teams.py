#!/usr/bin/env python
# Notify via Micrsoft Teams

import os
import requests
import sys

COLORS = {
    "CRITICAL": "#EE0000",
    "DOWN": "#EE0000",
    "WARNING": "#FFDD00",
    "OK": "#00CC00",
    "UP": "#00CC00",
    "UNKNOWN": "#CCCCCC",
    "UNREACHABLE": "#CCCCCC",
}

def teams_msg(context):
    """Build the message for teams"""
    facts = []
    if context.get('WHAT', None) == "SERVICE":
        state = context["SERVICESTATE"]
        color = COLORS.get(state)
        subtitle = "Service Notification"
        facts.append({"name": "Service:", "value": context["SERVICEDESC"]})
        output = context["SERVICEOUTPUT"] if context["SERVICEOUTPUT"] else ""
    else:
        state = context["HOSTSTATE"]
        color = COLORS.get(state)
        subtitle = "Host Notification"
        output = context["HOSTOUTPUT"] if context["HOSTOUTPUT"] else ""

    facts.extend([
        {
            "name": "Host:",
            "value": context["HOSTNAME"]
        },
        {
            "name": "State:",
            "value": state
        }
    ])

    return {
        "@type": "MessageCard",
        "@context": "https://schema.org/extensions",
        "summary": subtitle,
        "themeColor": color,
        "sections": [
            {
                "activityTitle": "CheckMK",
                "activitySubtitle": subtitle,
                "activityImage": "https://checkmk.com/images/favicon.png",
                "facts": facts,
                "text": output
            }
        ]
    }

def collect_context():
    return {
        var[7:]: value.decode("utf-8")
        for (var, value) in os.environ.items()
        if var.startswith("NOTIFY_")
    }

def post_request(message_constructor, success_code=200):
    context = collect_context()

    url = context.get("PARAMETERS")
    r = requests.post(url=url, json=message_constructor(context))

    if r.status_code == success_code:
        sys.exit(0)
    else:
        sys.stderr.write(
            "Failed to send notification. Status: %i, Response: %s\n" % (r.status_code, r.text))
        sys.exit(2)

if __name__ == "__main__":
    post_request(teams_msg)
