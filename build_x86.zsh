#!/bin/zsh

EXIFTOOL_VERSION="13.33"
EXIFTOOL_ARCHIVE_NAME="Image-ExifTool-$EXIFTOOL_VERSION.tar.gz"
BUILD_DIR_NAME="x86_build"


set -e

# Make a temp build directory
mkdir -p $BUILD_DIR_NAME

# Grab the git hash of the current commit
git rev-parse HEAD > $BUILD_DIR_NAME/build_id.txt

# Grab the current version from pyproject.toml
cat pyproject.toml | grep "version = " | sed -E "s/version = \"(.*)\"/\1/" | tr -d '\n' > $BUILD_DIR_NAME/version.txt

# Download exiftool
wget -O "$BUILD_DIR_NAME/$EXIFTOOL_ARCHIVE_NAME" "https://sourceforge.net/projects/exiftool/files/$EXIFTOOL_ARCHIVE_NAME/download"
tar -xzvf $BUILD_DIR_NAME/$EXIFTOOL_ARCHIVE_NAME -C $BUILD_DIR_NAME

# Install Python packages
uv venv
uv pip install ".[dev]"


# Generate the binary
uv run pyinstaller --clean --noconfirm main.spec

# Create the zip file
cd dist
ditto -c -k --sequesterRsrc --keepParent "iBenthos Geotagging Tool.app" "iBenthos Geotagging Tool x86 v$(cat ../$BUILD_DIR_NAME/version.txt).zip"
cd ..

# Clean up build files
rm -rf $BUILD_DIR_NAME
