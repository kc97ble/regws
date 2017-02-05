#!/bin/bash
export FLASK_APP=regws
export FLASK_DEBUG=1
python -m flask $@

