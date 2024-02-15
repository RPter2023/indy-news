#!/usr/bin/env sh

pip freeze -q -r requirements-prod.txt | sed '/freeze/,$ d' >requirements.txt
