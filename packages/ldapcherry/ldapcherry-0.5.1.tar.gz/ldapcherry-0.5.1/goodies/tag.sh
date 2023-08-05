#!/bin/sh

cd  `dirname $0`/../

version=`sed -e "s/version\ * = \ *'\(.*\)'.*/\1/;tx;d;:x" ./ldapcherry/__init__.py`

git tag "$version"
git push origin "$version"
