
# Create and activate virtual environment
python -m venv x86_build
& "x86_build\Scripts\Activate.ps1"

# Install Python packages
pip install pyside6 pyexiftool pyyaml pyinstaller
pip install git+ssh://git@bitbucket.csiro.au:7999/visage/geotag_pt.git

# Save the current git commit hash
$buildId = git rev-parse HEAD
$buildId | Out-File -Encoding ascii -NoNewline "x86_build\build_id.txt"

# Run PyInstaller
pyinstaller --clean --noconfirm main.spec

# Zip the output using Compress-Archive
Set-Location dist
$zipName = "iBenthos Geotagging Tool Windows x86 $buildId.zip"
Compress-Archive -Path "iBenthos Geotagging Tool" -DestinationPath $zipName

# Deactivate virtual environment
deactivate

# Return to root and clean up
Set-Location ..
Remove-Item -Recurse -Force x86_build
