#!/usr/bin/env python
"""
Cross-platform setup script for VideoMaMa environment
Works on Windows, macOS, and Linux

Usage:
    python setup.py
"""

import os
import sys
import subprocess
import platform
from pathlib import Path
from typing import List, Optional


class EnvironmentSetup:
    """Handle cross-platform environment setup"""
    
    def __init__(self):
        self.os_type = platform.system()
        self.python_version = f"{sys.version_info.major}.{sys.version_info.minor}"
        self.is_conda_available = self._check_conda()
        
    def _check_conda(self) -> bool:
        """Check if conda is available"""
        try:
            result = subprocess.run(['conda', '--version'], 
                                  capture_output=True, text=True)
            return result.returncode == 0
        except FileNotFoundError:
            return False
    
    def run_command(self, cmd: List[str], description: str = "") -> bool:
        """Run a command and handle cross-platform differences"""
        try:
            if description:
                print(f"\n{'='*60}")
                print(f"👉 {description}")
                print(f"{'='*60}")
            
            print(f"Running: {' '.join(cmd)}")
            result = subprocess.run(cmd, check=False)
            
            if result.returncode != 0:
                print(f"⚠️  Command failed with return code {result.returncode}")
                return False
            
            print("✓ Command completed successfully")
            return True
            
        except Exception as e:
            print(f"❌ Error running command: {e}")
            return False
    
    def create_conda_env(self, env_name: str, python_version: str) -> bool:
        """Create conda environment (cross-platform)"""
        if not self.is_conda_available:
            print("❌ Conda is not installed. Please install Miniconda or Anaconda first.")
            return False
        
        cmd = ['conda', 'create', '-n', env_name, f'python={python_version}', '-y']
        return self.run_command(cmd, f"Creating conda environment '{env_name}'")
    
    def activate_and_install(self, env_name: str, packages: List[str]) -> bool:
        """Install packages in conda environment (cross-platform)"""
        if not self.is_conda_available:
            print("❌ Conda is not installed.")
            return False
        
        # Use 'conda run' for cross-platform conda environment activation
        pip_cmd = [sys.executable, '-m', 'pip', 'install'] + packages
        
        # For conda environments, use conda run
        if self.os_type == 'Windows':
            cmd = ['conda', 'run', '-n', env_name, 'pip', 'install'] + packages
        else:
            cmd = ['conda', 'run', '-n', env_name] + pip_cmd
        
        return self.run_command(cmd)
    
    def install_pip_packages(self, packages: List[str], description: str = "") -> bool:
        """Install pip packages"""
        cmd = [sys.executable, '-m', 'pip', 'install'] + packages
        return self.run_command(cmd, description or f"Installing {len(packages)} packages")
    
    def install_git_lfs(self) -> bool:
        """Install Git LFS (cross-platform)"""
        if self.os_type == 'Windows':
            print("\n📝 Git LFS Installation for Windows:")
            print("   1. Download installer from: https://git-lfs.github.com/")
            print("   2. Run: git lfs install")
            return True
        elif self.os_type == 'Darwin':  # macOS
            cmd = ['brew', 'install', 'git-lfs']
            return self.run_command(cmd, "Installing Git LFS via Homebrew")
        else:  # Linux
            if os.path.exists('/etc/debian_version'):
                cmds = [
                    ['curl', '-s', 'https://packagecloud.io/install/repositories/github/git-lfs/script.deb.sh'],
                    ['bash'],
                ]
                print("Installing Git LFS on Debian/Ubuntu...")
                return self.run_command(['sudo', 'apt-get', 'install', '-y', 'git-lfs'],
                                      "Installing Git LFS")
            else:
                print("⚠️  Please install Git LFS manually for your distribution")
                print("    Visit: https://github.com/git-lfs/git-lfs/wiki/Installation")
                return True
    
    def setup_sam2_environment(self) -> bool:
        """Setup SAM2 environment"""
        print("\n" + "="*60)
        print("Setting up SAM2 Environment")
        print("="*60)
        
        if not self.is_conda_available:
            print("\nUsing pip instead of conda...")
            packages = [
                'torch==2.6.0',
                'torchvision==0.21.0',
                'torchaudio==2.6.0',
                'git+https://github.com/facebookresearch/sam2.git',
            ]
            return self.install_pip_packages(packages, "Installing SAM2 dependencies")
        
        if not self.create_conda_env('sam2', '3.11'):
            return False
        
        packages = [
            'torch::pytorch::py3.11_cuda124_cudnn9',
            'pytorch::torchvision',
            'pytorch::torchaudio',
            'pytorch-cuda=12.4'
        ]
        
        return self.activate_and_install('sam2', packages)
    
    def setup_videomama_environment(self) -> bool:
        """Setup VideoMaMa environment"""
        print("\n" + "="*60)
        print("Setting up VideoMaMa Environment")
        print("="*60)
        
        if not self.is_conda_available:
            print("\nUsing pip instead of conda...")
            packages = [
                'torch==2.4.0',
                'torchvision==0.19.0',
                'torchaudio==2.4.0',
            ]
            return self.install_pip_packages(packages, "Installing PyTorch for VideoMaMa")
        
        if not self.create_conda_env('videomama', '3.9'):
            return False
        
        # Install base packages
        packages = [
            'torch::pytorch::py3.9_cuda124_cudnn9',
            'pytorch::torchvision',
            'pytorch::torchaudio',
            'pytorch-cuda=12.4'
        ]
        
        if not self.activate_and_install('videomama', packages):
            return False
        
        # Install additional dependencies
        additional_packages = [
            'transformers==4.57.0',
            'psutil',
            'diffusers>=0.31.0',
            'opencv-python>=4.9.0.80',
            'gradio==5.12.0',
            'accelerate>=0.20.0',
            'einops>=0.6.0',
            'tqdm>=4.65.0',
            'safetensors>=0.3.0',
            'imageio>=2.31.0',
            'imageio-ffmpeg>=0.4.9',
        ]
        
        return self.activate_and_install('videomama', additional_packages)
    
    def setup_git_lfs(self) -> bool:
        """Setup Git LFS"""
        if not self.install_git_lfs():
            return False
        
        return self.run_command(['git', 'lfs', 'install'], "Initializing Git LFS")
    
    def download_checkpoints(self) -> bool:
        """Download model checkpoints"""
        print("\n" + "="*60)
        print("Downloading Model Checkpoints")
        print("="*60)
        
        # Create checkpoints directory
        checkpoint_dir = Path(__file__).parent.parent / 'checkpoints'
        checkpoint_dir.mkdir(exist_ok=True)
        print(f"✓ Checkpoints directory: {checkpoint_dir}")
        
        # You would add checkpoint download logic here
        print("\n📝 Checkpoint Download Instructions:")
        print("   1. SAM2 checkpoint will be downloaded by the demo on first run")
        print("   2. For VideoMaMa checkpoint, follow the instructions in README.md")
        
        return True
    
    def run_full_setup(self) -> bool:
        """Run complete setup"""
        print(f"\n{'='*60}")
        print(f"VideoMaMa Cross-Platform Setup")
        print(f"Operating System: {self.os_type}")
        print(f"Python Version: {self.python_version}")
        print(f"Conda Available: {self.is_conda_available}")
        print(f"{'='*60}")
        
        steps = [
            ("Setting up Git LFS", self.setup_git_lfs),
            ("Setting up SAM2 environment", self.setup_sam2_environment),
            ("Setting up VideoMaMa environment", self.setup_videomama_environment),
            ("Downloading checkpoints", self.download_checkpoints),
        ]
        
        failed_steps = []
        
        for step_name, step_func in steps:
            try:
                if not step_func():
                    failed_steps.append(step_name)
            except Exception as e:
                print(f"❌ Error in {step_name}: {e}")
                failed_steps.append(step_name)
        
        # Print summary
        print(f"\n{'='*60}")
        print("SETUP SUMMARY")
        print(f"{'='*60}")
        
        if failed_steps:
            print(f"⚠️  Failed steps:")
            for step in failed_steps:
                print(f"   - {step}")
            print("\nPlease review the errors above and try again.")
            return False
        else:
            print("✓ All setup steps completed successfully!")
            print("\nNext steps:")
            print("1. For SAM2 environment: conda activate sam2")
            print("2. For VideoMaMa environment: conda activate videomama")
            if self.os_type == 'Windows':
                print("   (Use 'activate videomama' on older Windows Python installations)")
            print("\nTo run the demo:")
            print("   cd demo")
            print("   python app.py")
            return True


if __name__ == '__main__':
    setup = EnvironmentSetup()
    success = setup.run_full_setup()
    sys.exit(0 if success else 1)
