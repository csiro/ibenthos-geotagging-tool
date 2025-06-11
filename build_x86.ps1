
$EXIFTOOL_VERSION = "13.29"
$EXIFTOOL_ARCHIVE_NAME = "exiftool-${EXIFTOOL_VERSION}_64"
$BUILD_DIR_NAME = "x86_build"

# Create and activate virtual environment
python -m venv $BUILD_DIR_NAME
& "$BUILD_DIR_NAME\Scripts\Activate.ps1"

# Install Python packages
pip install pyside6 pyexiftool pyyaml pyinstaller
pip install git+ssh://git@bitbucket.csiro.au:7999/visage/geotag_pt.git

# Save the current git commit hash
$buildId = git rev-parse HEAD
$buildId | Out-File -Encoding ascii -NoNewline "$BUILD_DIR_NAME\build_id.txt"

# Download exiftool
Invoke-WebRequest -Uri "https://exiftool.org/$EXIFTOOL_ARCHIVE_NAME.zip" -OutFile "$BUILD_DIR_NAME\$EXIFTOOL_ARCHIVE_NAME.zip"
Expand-Archive -Path "$BUILD_DIR_NAME\$EXIFTOOL_ARCHIVE_NAME.zip" -DestinationPath $BUILD_DIR_NAME -Force
Rename-Item -Path "$BUILD_DIR_NAME\$EXIFTOOL_ARCHIVE_NAME\exiftool(-k).exe" -NewName "exiftool.exe"

# Run PyInstaller
pyinstaller --clean --noconfirm main.spec

# Compile the installer
ISCC.exe /O"dist" ".\windows_setup_builder.iss"

# Deactivate virtual environment
deactivate

# clean up
Remove-Item -Recurse -Force x86_build
