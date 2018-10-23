#!/bin/bash
git diff -U0 --cached | flake8 --diff
if [ $? != 0 ]; then
   echo "Code fails pyflake check."
   exit 1
fi
exit 0
