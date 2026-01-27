#!/usr/bin/env python
"""
Cross-platform checkpoint download script for VideoMaMa demo
Works on Windows, macOS, and Linux

Usage:
    python download_checkpoints.py
"""

import os
import sys
import subprocess
import platform
from pathlib import Path
from typing import Optional
import shutil


class CheckpointDownloader:
    """Handle cross-platform checkpoint downloads"""
    
    def __init__(self):
        self.os_type = platform.system()
        self.checkpoint_dir = Path(__file__).parent / 'checkpoints'
        
    def create_checkpoint_dir(self) -> bool:
        """Create checkpoints directory"""
        try:
            self.checkpoint_dir.mkdir(parents=True, exist_ok=True)
            print(f"✓ Checkpoints directory ready: {self.checkpoint_dir}")
            return True
        except Exception as e:
            print(f"❌ Error creating checkpoint directory: {e}")
            return False
    
    def download_with_wget(self, url: str, output_path: Path) -> bool:
        """Download using wget"""
        try:
            cmd = ['wget', url, '-O', str(output_path)]
            print(f"Downloading with wget: {' '.join(cmd)}")
            result = subprocess.run(cmd, check=False)
            return result.returncode == 0
        except FileNotFoundError:
            return False
    
    def download_with_curl(self, url: str, output_path: Path) -> bool:
        """Download using curl"""
        try:
            cmd = ['curl', '-L', url, '-o', str(output_path)]
            print(f"Downloading with curl: {' '.join(cmd)}")
            result = subprocess.run(cmd, check=False)
            return result.returncode == 0
        except FileNotFoundError:
            return False
    
    def download_file(self, url: str, output_path: Path, description: str) -> bool:
        """Download file with fallback methods"""
        print(f"\n{'='*60}")
        print(f"Downloading {description}")
        print(f"{'='*60}")
        print(f"URL: {url}")
        print(f"Output: {output_path}")
        
        # Check if file already exists
        if output_path.exists():
            print(f"✓ File already exists: {output_path}")
            return True
        
        # Try wget first, then curl, then Python
        print("\nAttempting download...")
        
        if self.download_with_wget(url, output_path):
            print("✓ Download successful with wget")
            return True
        
        if self.download_with_curl(url, output_path):
            print("✓ Download successful with curl")
            return True
        
        # Fallback: use Python's urllib
        try:
            print("Attempting download with Python urllib...")
            import urllib.request
            from urllib.request import urlopen
            
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            with urlopen(url) as response, open(output_path, 'wb') as out_file:
                total_size = int(response.headers.get('content-length', 0))
                downloaded = 0
                chunk_size = 8192
                
                while True:
                    chunk = response.read(chunk_size)
                    if not chunk:
                        break
                    out_file.write(chunk)
                    downloaded += len(chunk)
                    
                    if total_size > 0:
                        percent = (downloaded / total_size) * 100
                        print(f"  Downloaded: {downloaded / (1024*1024):.1f}MB / {total_size / (1024*1024):.1f}MB ({percent:.1f}%)", 
                              end='\r')
            
            print(f"\n✓ Download successful with Python urllib")
            return True
            
        except Exception as e:
            print(f"❌ Download failed: {e}")
            return False
    
    def download_sam2_checkpoint(self) -> bool:
        """Download SAM2 checkpoint"""
        url = "https://dl.fbaipublicfiles.com/segment_anything_2/072824/sam2_hiera_large.pt"
        output_path = self.checkpoint_dir / "sam2_hiera_large.pt"
        
        return self.download_file(url, output_path, "SAM2 checkpoint (900MB)")
    
    def check_videomama_checkpoint(self) -> bool:
        """Check if VideoMaMa checkpoint exists"""
        print(f"\n{'='*60}")
        print("Checking VideoMaMa Checkpoint")
        print(f"{'='*60}")
        
        checkpoint_dir = self.checkpoint_dir / "videomama_unet"
        
        if checkpoint_dir.exists():
            config_exists = (checkpoint_dir / "config.json").exists()
            model_exists = (checkpoint_dir / "diffusion_pytorch_model.safetensors").exists() or \
                          (checkpoint_dir / "diffusion_pytorch_model.bin").exists()
            
            if config_exists and model_exists:
                print(f"✓ VideoMaMa checkpoint found at: {checkpoint_dir}")
                return True
            else:
                print(f"⚠️  VideoMaMa checkpoint directory exists but is incomplete")
                print(f"   Location: {checkpoint_dir}")
                print(f"   Config exists: {config_exists}")
                print(f"   Model exists: {model_exists}")
        else:
            print(f"⚠️  VideoMaMa checkpoint not found")
            print(f"   Expected location: {checkpoint_dir}")
        
        print("\n📝 Manual step required:")
        print("   1. Obtain VideoMaMa checkpoint from the authors")
        print("   2. Place files in the following structure:")
        print(f"      {checkpoint_dir}/")
        print("      ├── config.json")
        print("      └── diffusion_pytorch_model.safetensors (or .bin)")
        
        return False
    
    def run_full_download(self) -> bool:
        """Run complete checkpoint download"""
        print(f"\n{'='*60}")
        print(f"VideoMaMa Checkpoint Downloader")
        print(f"Operating System: {self.os_type}")
        print(f"{'='*60}")
        
        if not self.create_checkpoint_dir():
            return False
        
        # Download SAM2
        if not self.download_sam2_checkpoint():
            print("⚠️  Failed to download SAM2 checkpoint")
            print("   The demo will attempt to download it on first run")
        
        # Check VideoMaMa
        self.check_videomama_checkpoint()
        
        # Print summary
        print(f"\n{'='*60}")
        print("Download Summary")
        print(f"{'='*60}")
        print(f"Checkpoints directory: {self.checkpoint_dir}")
        print("\nFiles to check:")
        for item in self.checkpoint_dir.iterdir():
            if item.is_file():
                size_mb = item.stat().st_size / (1024 * 1024)
                print(f"  ✓ {item.name} ({size_mb:.1f}MB)")
            elif item.is_dir():
                print(f"  📁 {item.name}/")
        
        return True


if __name__ == '__main__':
    downloader = CheckpointDownloader()
    success = downloader.run_full_download()
    sys.exit(0 if success else 1)
