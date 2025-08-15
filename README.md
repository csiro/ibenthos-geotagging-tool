# iBenthos Geotagging Tool

A desktop application for geotagging underwater photos using GPS data from transect files. The application helps marine researchers synchronize underwater images with GPS tracks and export metadata in iFDO (Image File Data Object) format for marine research purposes.

## Features

- **Photo Geotagging**: Automatically add GPS coordinates to underwater photos using GPX track data
- **Time Synchronization**: Sync camera timestamps with GPS timestamps using reference photos
- **Marine Research Metadata**: Export comprehensive iFDO metadata files for FAIR data principles
- **KML Export**: Generate KML/KMZ files with geotagged photo locations for visualization in Google Earth
- **Attribution Metadata**: Embed researcher and copyright information directly into photo EXIF data
- **Cross-Platform**: Native desktop applications for Windows and macOS

## Requirements

- Python 3.11 or higher (for development)
- uv for dependency management
- ExifTool (automatically downloaded during build)

## Development Setup

### Prerequisites

1. Install Python 3.11+ from [python.org](https://python.org)
2. Install uv:
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/csiro/ibenthos-geotagging-tool.git
   cd ibenthos-geotagging-tool
   ```

2. Install dependencies using Poetry:
   ```bash
   uv venv
   uv pip install .
   source .venv/bin/activate
   ```

3. Run the application in development mode:
   ```bash
   python src/main.py
   ```

### Testing

Run the test suite:
```bash
pytest
```

Run specific test files:
```bash
pytest tests/test_user_input_model.py
```

## Building for Distribution

### macOS (Universal x86)

The macOS build targets x86_64 architecture, which runs natively on Intel Macs and via Rosetta on Apple Silicon Macs.

#### Automated Build

```bash
./build_x86.zsh
```

#### Manual Build Steps

1. Build the application bundle:
   ```bash
   pyinstaller --clean --noconfirm main.spec
   ```

#### Building Universal x86 on Apple Silicon

To ensure x86_64 compatibility on Apple Silicon Macs:

1. Install Python using the universal2 build from python.org
2. Set your terminal to Rosetta mode: Right-click iTerm2 → Get Info → Use Rosetta
3. Create an x86_64 virtual environment:
   ```bash
   python -m venv x86_builder
   source x86_builder/bin/activate
   ```
4. Install packages with x86_64 architecture:
   ```bash
   arch -x86_64 pip install poetry
   arch -x86_64 poetry install
   ```
5. Set `target_arch = "x86_64"` in `main.spec`
6. Build with PyInstaller

### Windows

#### Automated Build

```powershell
./build_x86.ps1
```

This script:
- Builds the application bundle using PyInstaller
- Downloads ExifTool for Windows
- Creates a Windows installer using Inno Setup

#### Manual Build Steps

1. Build the application:
   ```bash
   poetry run pyinstaller --clean --noconfirm main.spec
   ```

2. The Windows installer setup is defined in the `.iss` file and can be compiled with Inno Setup.

## Dependencies and Acknowledgments

This application is built using the following open-source libraries and tools:

### Core Framework
- **PySide6** - Cross-platform GUI framework by The Qt Company
- **Python** - Programming language by the Python Software Foundation

### Image and GPS Processing
- **geotag-pt** - GPS photo tagging library (CSIRO internal)
- **PyExifTool** - Python wrapper for ExifTool by Phil Harvey
- **Pillow (PIL)** - Python Imaging Library for image processing
- **simplekml** - KML generation library

### Data and Configuration
- **PyYAML** - YAML parser and emitter for Python
- **NumPy** - Numerical computing library

### Build and Distribution
- **PyInstaller** - Packaging Python applications
- **Poetry** - Dependency management and packaging
- **Inno Setup** - Windows installer creator (Windows builds)

### External Tools
- **ExifTool** by Phil Harvey - Command-line application for reading, writing and editing meta information

## License

This project is distrbuted under the [LGPLv3](LICENSE) license.

## Citation

If you use this software in your research, please cite:

```
iBenthos Geotagging Tool. (2025). Commonwealth Scientific and Industrial Research Organisation (CSIRO). 
https://github.com/csiro/ibenthos-geotagging-tool
```

---

**Author**: Brendan Do (brendan.do@csiro.au)  
**Organization**: Commonwealth Scientific and Industrial Research Organisation (CSIRO)