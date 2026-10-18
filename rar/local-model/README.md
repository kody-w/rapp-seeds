# Local model

Your Brainstem thinks with a model on your own computer instead of Copilot. Your memory and agents were already
files on your computer; now the thinking is too.

```
python3 local_model.py --offline
```

It starts a small bridge that answers the Brainstem the way Copilot does, then starts your unchanged Brainstem
pointed at it. Nothing in your Brainstem's folder is edited. To go back to Copilot, close it and run your normal
install line.

- **Needs:** [Ollama](https://ollama.com) with a model that can call tools: `ollama pull qwen2.5:14b`.
- **`--model`** picks another Ollama model. **`--brainstem`** points at a Brainstem folder other than
  `~/.brainstem/src/rapp_brainstem`. **`--port`** sets the page's port (default 7071).
- **`--offline`** sends every web request through a proxy that does not exist, except to this computer and to
  Ollama, so an agent that tries to reach the internet fails. It guards ordinary Python web requests. It is not a
  firewall: for a machine that must never connect, also cut the network.

## Checked on 2026-10-18 (Brainstem blob 3f7102f, qwen2.5:14b)

- Asked a sum: answered "51." in about 9 seconds, on this computer.
- With `--offline`: told it a fact, closed it, started it again, asked: "You prefer a flat white."
- With `--offline`: asked the Hacker News agent for the top story; the fetch was refused.
