#!/bin/zsh

EXIFTOOL_VERSION="13.29"
EXIFTOOL_ARCHIVE_NAME="Image-ExifTool-$EXIFTOOL_VERSION.tar.gz"
BUILD_DIR_NAME="x86_build"


set -e

python3 -m venv $BUILD_DIR_NAME
source $BUILD_DIR_NAME/bin/activate

arch -x86_64 pip install pyside6 pyexiftool pyyaml pyinstaller
arch -x86_64 pip install git+ssh://git@bitbucket.csiro.au:7999/visage/geotag_pt.git

git rev-parse HEAD > $BUILD_DIR_NAME/build_id.txt

# Download exiftool
wget -O "$BUILD_DIR_NAME/$EXIFTOOL_ARCHIVE_NAME" "https://exiftool.org/$EXIFTOOL_ARCHIVE_NAME"
tar -xzvf $BUILD_DIR_NAME/$EXIFTOOL_ARCHIVE_NAME -C $BUILD_DIR_NAME

pyinstaller --clean --noconfirm main.spec
# codesign --force --sign "Mac Developer: Brendan Do (V4NYX6N27N)" "./dist/iBenthos Geotagging Tool.app"

cd dist

ditto -c -k --sequesterRsrc --keepParent "iBenthos Geotagging Tool.app" "iBenthos Geotagging Tool x86 $(cat ../$BUILD_DIR_NAME/build_id.txt).zip"

deactivate

cd ..

rm -rf $BUILD_DIR_NAME
