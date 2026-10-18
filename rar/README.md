# Add-ons

Things you add around your Brainstem. Each one leaves the Brainstem itself unchanged: it is an agent you drop in,
a small program that runs beside it, or an edition that pins the unchanged Brainstem and adds pieces around it.

| Add-on | What it does | Checked |
|---|---|---|
| [local-model](local-model/) | Your Brainstem thinks with a model on your own computer, through Ollama. With `--offline`, it also blocks every outside connection. | 2026-10-18: answered, and remembered a fact across a restart, with outside connections blocked; an outside fetch was refused |
| [offline-edition](offline-edition/) | One line installs the unchanged Brainstem plus the local-model add-on, in its own folder, on port 7081. | 2026-10-18: fresh Ubuntu 24.04 container, installed in 32 s, remembered a fact across a restart |
