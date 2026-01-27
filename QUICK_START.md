# Quick Reference - Cross-Platform VideoMaMa

## TL;DR - Get Started in 3 Steps

### Step 1: Clone and Setup
```bash
# All platforms
python scripts/setup.py
```

### Step 2: Download Checkpoints
```bash
cd demo
python download_checkpoints.py
```

### Step 3: Run Demo
```bash
conda activate videomama  # or use your environment
python app.py
```

---

## Platform Quick Links

### Windows (PowerShell)
```powershell
# Setup
python scripts/setup.py

# Activate environment
conda activate videomama
# OR for legacy Python: activate videomama

# Run demo
python demo/app.py

# Run inference with quoted paths
python inference_onestep_folder.py `
    --image_root_path "C:\Users\YourName\data\images" `
    --mask_root_path "C:\Users\YourName\data\masks" `
    --output_dir "C:\Users\YourName\output"
```

### macOS (zsh/bash)
```bash
# Setup
python3 scripts/setup.py

# Install Git LFS via Homebrew (if needed)
brew install git-lfs
git lfs install

# Activate environment
conda activate videomama

# Run demo
python3 demo/app.py

# Run inference
python3 inference_onestep_folder.py \
    --image_root_path ~/data/images \
    --mask_root_path ~/data/masks \
    --output_dir ~/output
```

### Linux (bash)
```bash
# Install dependencies
sudo apt-get update
sudo apt-get install -y build-essential git-lfs python3-pip

# Setup
python3 scripts/setup.py

# Activate environment
source videomama_env/bin/activate

# Run demo
python3 demo/app.py

# Run inference
python3 inference_onestep_folder.py \
    --image_root_path /home/$USER/data/images \
    --mask_root_path /home/$USER/data/masks \
    --output_dir /home/$USER/output
```

---

## Environment Variables (Optional)

Set these once to avoid typing long paths repeatedly:

### Windows (PowerShell - add to $PROFILE)
```powershell
$env:VIDEOMAMA_BASE_MODEL = "C:\models\stable-video-diffusion-img2vid-xt"
$env:VIDEOMAMA_UNET_CHECKPOINT = "C:\models\videomama"
$env:SAM2_PATH = "C:\repos\sam2"
```

### macOS/Linux (add to ~/.bashrc or ~/.zshrc)
```bash
export VIDEOMAMA_BASE_MODEL="$HOME/models/stable-video-diffusion-img2vid-xt"
export VIDEOMAMA_UNET_CHECKPOINT="$HOME/models/videomama"
export SAM2_PATH="$HOME/repos/sam2"
```

---

## Common Issues & Solutions

| Issue | Windows | macOS | Linux |
|-------|---------|-------|-------|
| `ModuleNotFoundError: sam2` | Set `$env:SAM2_PATH` | Export `SAM2_PATH` | Export `SAM2_PATH` |
| `No space left` (path with spaces) | Quote path: `"C:\My Documents\..."` | Quote path: `~/My\ Documents/...` | Quote path: `~/My\ Documents/...` |
| CUDA out of memory | `--device cpu` | N/A | `--device cpu` |
| Git LFS not working | Download installer | `brew install git-lfs` | `sudo apt install git-lfs` |

---

## Project Structure

```
VideoMaMa-main/
├── demo/                          # Interactive demo
│   ├── app.py                    # Main Gradio interface
│   ├── download_checkpoints.py   # ⭐ Download models (cross-platform)
│   ├── requirements.txt
│   ├── videomama_wrapper.py      # ✅ Updated for cross-platform
│   ├── sam2_wrapper.py           # ✅ Updated for cross-platform
│   └── tools/
│       ├── base_segmenter.py     # ✅ Updated for cross-platform
│       ├── painter.py
│       └── interact_tools.py
├── scripts/
│   └── setup.py                  # ⭐ Cross-platform setup (new)
├── src/
│   └── unet_spatio_temporal_condition.py
├── inference_onestep_folder.py   # ✅ Updated for cross-platform
├── pipeline_svd_mask.py
├── setup.py
├── CROSS_PLATFORM_SETUP.md       # 📖 Detailed setup guide (new)
├── CROSS_PLATFORM_CHANGES.md     # 📋 Changes summary (new)
└── README.md
```

⭐ = New files
✅ = Updated for cross-platform

---

## File Paths Reference

### Checkpoint Locations (Default)
```
VideoMaMa-main/
├── checkpoints/
│   ├── sam2_hiera_large.pt              # Downloaded by script
│   ├── stable-video-diffusion-img2vid-xt/
│   │   ├── config.json
│   │   └── diffusion_pytorch_model.safetensors
│   └── videomama/
│       ├── config.json
│       └── diffusion_pytorch_model.safetensors
```

### Data Format (Input)
```
/path/to/dataset/
├── image/
│   ├── video_001/
│   │   ├── 0000.png
│   │   ├── 0001.png
│   │   └── ...
│   └── video_002/
│       └── ...
└── mask/
    ├── video_001/
    │   ├── 0000.png
    │   ├── 0001.png
    │   └── ...
    └── video_002/
        └── ...
```

---

## Useful Commands

### Check Environment
```bash
# All platforms
python --version          # Should be 3.9+
pip list | grep torch     # Check PyTorch installed
conda env list            # List conda environments (if conda installed)
```

### Test Torch/CUDA
```python
import torch
print(f"PyTorch version: {torch.__version__}")
print(f"CUDA available: {torch.cuda.is_available()}")
print(f"Device: {torch.device('cuda' if torch.cuda.is_available() else 'cpu')}")
```

### Run with Logging
```bash
# Windows
python demo/app.py --debug 2>&1 | Tee-Object -FilePath log.txt

# macOS/Linux
python3 demo/app.py --debug 2>&1 | tee log.txt
```

---

## Documentation Files

| File | Purpose |
|------|---------|
| **README.md** | Original project documentation |
| **CROSS_PLATFORM_SETUP.md** | Complete setup guide for all platforms |
| **CROSS_PLATFORM_CHANGES.md** | Detailed list of all changes made |
| **This file** | Quick reference and cheat sheet |
| **inference.md** | Detailed inference options and examples |

---

## Next Steps

1. Read [CROSS_PLATFORM_SETUP.md](CROSS_PLATFORM_SETUP.md) for your platform
2. Run `python scripts/setup.py` to set up environment
3. Run `python demo/download_checkpoints.py` to get models
4. Test with `python demo/app.py`
5. Try batch inference with `python inference_onestep_folder.py`

---

## Need Help?

Check these in order:
1. This quick reference (command for your platform)
2. [CROSS_PLATFORM_SETUP.md](CROSS_PLATFORM_SETUP.md) (detailed guide)
3. [CROSS_PLATFORM_CHANGES.md](CROSS_PLATFORM_CHANGES.md) (technical details)
4. [README.md](README.md) (original documentation)
5. [inference.md](inference.md) (inference options)

---

## Tips & Tricks

### Speed up downloads
```bash
# Pre-create checkpoints folder
mkdir -p checkpoints
cd checkpoints
# Download manually and place files here
```

### Use CPU for testing
```bash
python demo/app.py --device cpu
```

### Custom model paths
```bash
export VIDEOMAMA_BASE_MODEL="/path/to/custom/model"
python demo/app.py
```

### Debug import issues
```bash
python -c "import sys; print('\n'.join(sys.path))"
```

---

Happy matting! 🎉
