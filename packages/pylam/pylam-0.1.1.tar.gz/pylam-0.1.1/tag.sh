#!/usr/bin/env sh

PWD=$(pwd)
BASEPATH=$(dirname $PWD)
VERSION=`grep "__version__" pylam/__init__.py  | cut -f 2 -d '=' | tr -d ' ' | tr -d "'"`
SVN_ROOT=`svn info | grep "^Repository Root:" | cut -d' ' -f3-`


if [ -n "$1" ]; then
    TAG_NAME=$1
    M="Created tag $TAG_NAME"
else
    TAG_NAME="v.$VERSION"
    M="Tag Release Version $VERSION"
fi

echo $TAG_NAME
echo $M
echo $SVN_ROOT

svn up ../tags
TAGS_OLD=`ls ../tags/`

if echo $TAGS_OLD | grep -q $TAG_NAME ; then
    echo "Tag Name $TAG_NAME already exists! Quit."
    exit 1
fi

svn copy $SVN_ROOT/trunk $SVN_ROOT/tags/$TAG_NAME -m "$M"

svn up ../tags

#cd "$BASEPATH" || exit
#svn up tags
#TAGS_OLD=`ls ../tags/`

#svn copy -rf trunk tags/$VERSION
#svn ci tags -m "Created tag TAG_NAME"

#cd 
#svn up 
#svn up ../tags/

#TAGS_OLD=`ls ../tags/`

#svn copy -rf ../trunk ../tags/$VERSION
#svn ci ..
