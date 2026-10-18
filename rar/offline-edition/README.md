# Offline edition

The unchanged Brainstem plus the local-model add-on, in one line:

```
curl -fsSL https://kody-w.github.io/rapp-seeds/rar/offline-edition/install.sh | bash
```

- Installs into `~/.brainstem-offline` and opens on http://127.0.0.1:7081, so a normal Brainstem keeps working.
- Pins the Brainstem by commit and checks its fingerprint before running it (`pin.json`).
- Installs Ollama if it is missing (Homebrew on a Mac, the official installer on Linux) and downloads the model
  once, several GB. Needs the internet for the install; after that, the thinking needs none.
- Start it again any time with `brainstem-offline`. `LOCAL_MODEL=qwen2.5:7b` picks a smaller model.

## Checked on 2026-10-18

Fresh Ubuntu 24.04 container: the one line installed in 32 seconds, the fingerprint matched, it answered with
outside connections blocked, and after a restart it recalled "Your dog is called Biscuit." Not yet checked: the
Ollama install and model download steps (that run used an existing Ollama), and a Mac or Windows machine.
