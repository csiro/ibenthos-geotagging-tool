#!/bin/zsh

set -e

python3 -m venv x86_build
source x86_build/bin/activate

arch -x86_64 pip install pyside6 pyexiftool pyyaml pyinstaller
arch -x86_64 pip install git+ssh://git@bitbucket.csiro.au:7999/visage/geotag_pt.git

git rev-parse HEAD > x86_build/build_id.txt

pyinstaller --clean --noconfirm main.spec
codesign --force --sign "Mac Developer: Brendan Do (V4NYX6N27N)" "./dist/iBenthos Geotagging Tool.app"

cd dist

ditto -c -k --sequesterRsrc --keepParent "iBenthos Geotagging Tool.app" "iBenthos Geotagging Tool x86 $(cat ../x86_build/build_id.txt).zip"

deactivate

cd ..

rm -rf x86_build
