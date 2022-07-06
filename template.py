from pprint import pprint

import chevron
import orjson

payload = {
    "other_key": "some_value",
    "user_name": "Akshat",
    "dataset_name": "Netflix dataset",
    "dataset_id": 3425435,
    "some_other_key": "some_random_value_we_dont_care_right_now",
}

notification_type = "dataset_registration"
notifier_type = "slack"

message_template = None
with open("message_template.json", "rb") as f:
    message_template = orjson.loads(f.read())

template = message_template[notification_type][notifier_type]["template"]
plugin_variables = message_template[notification_type][notifier_type][
    "plugin_variables"
]

template_str = str(template)

data = {variable: payload[variable] for variable in plugin_variables}

pprint(template_str)
print()
pprint(data)
print()

result = chevron.render(template_str, data=data)
pprint(result)
