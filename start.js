module.exports = {
  daemon: true,
  run: [
    {
      method: "shell.run",
      params: {
        path: "app",
        venv: "venv",
        message: "python demo/download_checkpoints.py"
      }
    },
    {
      method: "shell.run",
      params: {
        path: "app",
        venv: "venv",
        on: [
          {
            event: "/(http:\\/\\/\\S+)/",
            done: true
          }
        ],
        message: "python demo/app.py"
      }
    },
    {
      when: "{{input && input.event && Array.isArray(input.event) && input.event.length > 0}}",
      method: "local.set",
      params: {
        url: "{{input.event[0]}}"
      }
    }
  ]
}
