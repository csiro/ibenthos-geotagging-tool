
$EXIFTOOL_VERSION = "13.33"
$EXIFTOOL_ARCHIVE_NAME = "exiftool-${EXIFTOOL_VERSION}_64"
$BUILD_DIR_NAME = "x86_build"

# Make a temp build directory
New-Item -ItemType Directory -Path $BUILD_DIR_NAME -Force

# Save the current git commit hash
$buildId = git rev-parse HEAD
$buildId | Out-File -Encoding UTF8 -NoNewline "$BUILD_DIR_NAME\build_id.txt"

# Grab the current version from pyproject.toml
$versionLine = (Get-Content pyproject.toml) -match 'version\s*=\s*"(.*)"'
"$versionLine" -match 'version\s*=\s*"(.*)"'
$Matches[1] | Out-File  -Encoding UTF8 -NoNewline "$BUILD_DIR_NAME\version.txt"
$versionStr = $Matches[1]

# Download exiftool
Invoke-WebRequest -UserAgent "Wget" -Uri "https://sourceforge.net/projects/exiftool/files/$EXIFTOOL_ARCHIVE_NAME.zip/download" -OutFile "$BUILD_DIR_NAME\$EXIFTOOL_ARCHIVE_NAME.zip"
Expand-Archive -Path "$BUILD_DIR_NAME\$EXIFTOOL_ARCHIVE_NAME.zip" -DestinationPath $BUILD_DIR_NAME -Force
Rename-Item -Path "$BUILD_DIR_NAME\$EXIFTOOL_ARCHIVE_NAME\exiftool(-k).exe" -NewName "exiftool.exe"

# Install Python packages
poetry install

# Run PyInstaller
poetry run pyinstaller --clean --noconfirm main.spec

# Compile the installer
ISCC.exe /O"dist" /F"ibenthosgeotaggingtool_setup_v$versionStr" /D"MyAppVersion=$versionStr" ".\windows_setup_builder.iss"

# Clean up
Remove-Item -Recurse -Force x86_build
