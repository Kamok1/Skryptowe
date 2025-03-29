import os
import sys
import re

def get_variable(name):
    return os.environ.get(name)

def get_variables_dict(filters, match_exactly=False):
    if not filters:
        return dict(os.environ)

    if match_exactly:
        return { k: os.environ[k] for k in os.environ if any(k.lower() == f.lower() for f in filters) }

    else:
        pattern = re.compile("|".join(re.escape(f) for f in filters), re.IGNORECASE)
        return {k: os.environ[k] for k in os.environ if pattern.search(k)}


if __name__ == "__main__":
    filters = sys.argv[1:]
    variables = get_variables_dict(filters)
    for key in sorted(variables.keys()):
        print(f"{key}={variables[key]}")