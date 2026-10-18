# Proofs behind the claims

`prove.py` checks the claim every seed makes: tell it something, and tomorrow it still remembers.
It runs the unchanged Brainstem with a scripted stand-in model, saves one memory, stops the
program, starts it again with an empty conversation, and checks that the memory reaches the model.

```
python3 prove.py <dir holding grail/src/rapp_brainstem and rapp-1/conformance/grail>
```

Result on 2026-10-18, Brainstem blob 3f7102f:

```
before remember: SYSTEM PROMPT HAS FLAT WHITE: False
day 1: SAVED: Successfully stored preference memory in shared memory: "favorite coffee is a flat white"
kernel stopped (Terminal closed)
day 2, fresh process, empty history: SYSTEM PROMPT HAS FLAT WHITE: True
memory files in the folder: ['.brainstem_data/shared_memories/memory.json']
```

Not proven here: that a real model chooses to save the memory. The memory agent tells the model it
must save whenever someone asks it to remember.
