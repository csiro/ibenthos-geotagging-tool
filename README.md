
## Build the package

`pyinstaller main.spec`

## Sign the package for MacOS

`codesign --force --sign "Mac Developer: Brendan Do (XXXXXXXXXX)" ./iBenthos\ Geotagging\ Tool.app`

## Compiling for x86 macOS (thus effectively universal)

Trying to build for universal2 is fairly difficult to get repeatibility just because some packages don't support universal2. It's fairly cumbersome to lipo binaries together
My solution:
1. Install Python using the universal2 build on python.org. Add to path: /Library/Frameworks/Python.framework/Versions/3.12/bin
2. Set the terminal you're going to use to build to Rosetta mode: right click iTerm2 in Applications -> Get Info -> Use Rosetta
3. Start the terminal
4. Create a new venv to install your packages python -m venv x86_builder
5. Source the venv and install your packages using pip. Make sure when you're installing them to specify arch -x86_64 before the pip command
6. Change your target_arch in your .spec file to "x86_64"
7. Compile using pyinstaller
This will result in a binary that can be executed natively on x86_64 and via Rosetta on ARM64
