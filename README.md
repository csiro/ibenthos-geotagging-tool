
## Build the package

`pyinstaller main.spec`

## Sign the package for MacOS

`codesign --force --sign "Mac Developer: Brendan Do (XXXXXXXXXX)" ./iBenthos\ Geotagging\ Tool.app`