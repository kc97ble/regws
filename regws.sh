#!/bin/bash
export FLASK_APP=regws
export FLASK_DEBUG=0
python -m flask $@

