# Cross-Platform Setup Guide for VideoMaMa

This guide explains how to set up and use VideoMaMa on Windows, macOS, and Linux. All scripts and paths have been updated to work seamlessly across different operating systems.

## Platform Support

- ✅ **Windows** (10/11 with Python 3.9+)
- ✅ **macOS** (10.14+ with Python 3.9+)
- ✅ **Linux** (Ubuntu 18.04+, CentOS 7+, etc. with Python 3.9+)

## Quick Start

### 1. Prerequisites

**All Platforms:**
- Python 3.9 or higher
- pip (comes with Python)
- Git with Git LFS support
- CUDA 12.1+ (for GPU support) or CPU-only mode

**Windows:**
- Visual C++ Build Tools (for compiling some packages)
- Download installer from: https://git-lfs.github.com/

**macOS:**
- Xcode Command Line Tools: `xcode-select --install`
- Homebrew: `/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"`
- Git LFS: `brew install git-lfs`

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get update
sudo apt-get install -y build-essential git git-lfs
git lfs install
```

### 2. Automated Setup (Recommended)

#### Using Python Setup Script (Recommended for all platforms)

```bash
# Clone or navigate to the VideoMaMa directory
cd VideoMaMa-main

# Run the cross-platform setup script
python scripts/setup.py
```

This script will automatically:
- Detect your operating system
- Check for conda/pip availability
- Create separate environments for SAM2 and VideoMaMa
- Install all dependencies
- Set up Git LFS

**Platform-specific notes:**
- **Windows:** On older Python installations, use `activate videomama` instead of `conda activate videomama`
- **macOS/Linux:** Conda activation works with `conda activate videomama`

### 3. Manual Setup

If you prefer manual setup, follow the appropriate instructions for your platform:

#### Windows Setup

```powershell
# Install Git LFS first
# Download from https://git-lfs.github.com/ and run installer
git lfs install

# Option A: Using Conda (Recommended)
conda create -n videomama python=3.9 -y
conda activate videomama

# Option B: Using venv
python -m venv videomama_env
videomama_env\Scripts\activate

# Install PyTorch (Windows with CUDA 12.1)
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

# Install dependencies
pip install -r demo/requirements.txt
pip install -e .
```

#### macOS Setup

```bash
# Install Git LFS via Homebrew
brew install git-lfs
git lfs install

# Create and activate virtual environment
conda create -n videomama python=3.9 -y
conda activate videomama

# Install PyTorch (CPU or Metal GPU support)
pip install torch torchvision torchaudio

# Install dependencies
pip install -r demo/requirements.txt
pip install -e .
```

#### Linux Setup (Ubuntu/Debian)

```bash
# Install system dependencies
sudo apt-get update
sudo apt-get install -y build-essential python3-dev python3-pip git-lfs

# Initialize Git LFS
git lfs install

# Create and activate virtual environment
python3 -m venv videomama_env
source videomama_env/bin/activate

# Install PyTorch (Linux with CUDA 12.1)
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

# Install dependencies
pip install -r demo/requirements.txt
pip install -e .
```

## Configuration

### Environment Variables

You can customize paths using environment variables (cross-platform compatible):

```bash
# Set SAM2 path
export SAM2_PATH=/path/to/sam2  # Linux/macOS
set SAM2_PATH=C:\path\to\sam2    # Windows (PowerShell)

# Set VideoMaMa model paths
export VIDEOMAMA_BASE_MODEL=/path/to/stable-video-diffusion-img2vid-xt
export VIDEOMAMA_UNET_CHECKPOINT=/path/to/videomama
```

**Windows PowerShell:**
```powershell
$env:SAM2_PATH = "C:\path\to\sam2"
$env:VIDEOMAMA_BASE_MODEL = "C:\path\to\models\stable-video-diffusion-img2vid-xt"
$env:VIDEOMAMA_UNET_CHECKPOINT = "C:\path\to\models\videomama"
```

### Default Checkpoint Locations

If environment variables aren't set, the scripts look for checkpoints in:
```
VideoMaMa-main/
├── checkpoints/
│   ├── stable-video-diffusion-img2vid-xt/
│   └── videomama/
```

## Usage

### 1. Download Checkpoints (Cross-platform)

```bash
cd demo
python download_checkpoints.py
```

This Python script automatically:
- Detects your OS and available download tools (wget/curl)
- Downloads SAM2 checkpoint
- Checks for VideoMaMa checkpoint
- Provides setup instructions if needed

**Note:** Works on Windows, macOS, and Linux without modification.

### 2. Run the Interactive Demo

```bash
cd demo
conda activate videomama  # or source videomama_env/bin/activate on Linux/macOS
python app.py
```

The Gradio interface will open at `http://localhost:7860`

### 3. Run Batch Inference

```bash
# Activate environment
conda activate videomama

# Run inference with cross-platform compatible paths
python inference_onestep_folder.py \
    --base_model_path "path/to/stable-video-diffusion-img2vid-xt" \
    --unet_checkpoint_path "path/to/videomama" \
    --image_root_path "path/to/image/folder" \
    --mask_root_path "path/to/mask/folder" \
    --output_dir "path/to/output"
```

**Cross-platform path examples:**

```bash
# Windows (PowerShell)
python inference_onestep_folder.py `
    --image_root_path "C:\data\images" `
    --mask_root_path "C:\data\masks" `
    --output_dir "C:\output"

# Linux/macOS
python inference_onestep_folder.py \
    --image_root_path "/home/user/data/images" \
    --mask_root_path "/home/user/data/masks" \
    --output_dir "/home/user/output"
```

## Troubleshooting

### Path Issues

**Problem:** "No such file or directory" errors on Windows
**Solution:** All scripts now use Python's `pathlib.Path` for cross-platform compatibility. Ensure paths are properly quoted:
```powershell
# Windows PowerShell - use quotes for paths with spaces
python script.py --path "C:\My Documents\data"
```

### Module Import Errors

**Problem:** `ModuleNotFoundError: No module named 'sam2'`
**Solution:** Set the SAM2_PATH environment variable:

```bash
# Linux/macOS
export SAM2_PATH=$(which sam2)  # or path to sam2 directory

# Windows PowerShell
$env:SAM2_PATH = "C:\path\to\sam2"
```

Or clone SAM2 in one of the default locations:
- `../sam2` (relative to current directory)
- `~/sam2` (home directory)
- `/opt/sam2` (Linux systems)

### GPU Memory Issues

If you encounter CUDA out of memory errors:

```bash
# Reduce batch size or use CPU
python app.py --device cpu

# Or set environment variable
export CUDA_VISIBLE_DEVICES=0  # Use specific GPU
```

### Package Installation Failures

**Windows:** Install Visual C++ Build Tools
**macOS:** Install Xcode Command Line Tools: `xcode-select --install`
**Linux:** `sudo apt-get install build-essential python3-dev`

## Advanced Configuration

### Using Different Python Versions

Create environment for specific Python version:

```bash
# Conda approach
conda create -n videomama python=3.10 -y
conda activate videomama

# venv approach (Python 3.9)
python3.9 -m venv videomama_env
```

### Using CPU-Only Mode

```bash
# Install CPU-only PyTorch
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

# Run with CPU
python app.py --device cpu
```

### Development Setup

For contributing to the project:

```bash
# Install with development dependencies
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install

# Run tests
pytest tests/
```

## File Structure for Cross-Platform Compatibility

All Python scripts now use:
- `pathlib.Path` instead of string concatenation
- `os.path.join()` for path operations
- `sys.path.insert()` with dynamic path resolution

Example from updated code:
```python
from pathlib import Path

current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir.parent))
```

## Platform-Specific Notes

### Windows
- Use forward slashes `/` in Python code (handled automatically by pathlib)
- PowerShell: Use backtick `` ` `` for line continuation, not backslash `\`
- File paths can be quoted or unquoted

### macOS
- Ensure Xcode Command Line Tools are installed
- Metal GPU acceleration available with PyTorch
- Use `source` command for venv activation

### Linux
- Most distributions supported (Ubuntu, CentOS, Debian, etc.)
- May need `python3` instead of `python`
- Use `source` command for venv activation

## Getting Help

1. Check the main [README.md](../README.md)
2. See [inference.md](../inference.md) for detailed inference options
3. For platform-specific issues, file an issue with:
   - OS and Python version
   - Error message
   - Command used
   - Output from `python --version`

## Next Steps

1. Run `python scripts/setup.py` or follow manual setup
2. Download checkpoints with `python demo/download_checkpoints.py`
3. Test with `python demo/app.py`
4. Run inference with `python inference_onestep_folder.py`

Happy matting! 🎉
