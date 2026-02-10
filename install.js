module.exports = {
  run: [
    {
      method: "shell.run",
      params: {
        message: [
          "git clone https://github.com/manat0912/VideoMaMa-CrossPlatform.git app"
        ]
      }
    },
    {
      method: "shell.run",
      params: {
        venv: "venv",
        path: "app",
        message: [
          "uv pip install gradio",
          "{{platform === 'win32' ? 'cmd /c call ../scripts/setup.bat' : (platform === 'darwin' ? 'bash ../scripts/setup-macos.sh' : 'bash scripts/setup.sh')}}",
          "uv pip install -r demo/requirements.txt"
        ]
      }
    },
    {
      method: "script.start",
      params: {
        uri: "torch.js",
        params: {
          path: "app",
          venv: "venv",
          xformers: false,
          triton: "{{platform === 'linux' ? 'true' : ''}}",
          sageattention: false
        }
      }
    }
  ]
};

const os = require('os');

