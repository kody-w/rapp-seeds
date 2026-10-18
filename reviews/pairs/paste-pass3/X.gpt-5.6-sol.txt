# Your AI, as files you own.

**Learn it in an hour.** It thinks the way you do, so you can see how it works.
**Run it on any computer.** Mac, Windows or Linux. Its memory stays in your own folder.
**Hand it to anyone.** It is just files. One agent is one file.

Copy everything in the box into any AI chat you already use. It walks you, one step at a time, to your own
Brainstem: the small program on your computer that runs your AI.

```text
Be my guide for one hour. I want my own AI, as files I own, on my own computer.
The tool is the Brainstem. It is free and its source is public:
https://github.com/kody-w/rapp-installer

Rules for you: plain words, I have never coded, one step at a time, and wait for me
to say "done" before the next step. If anything goes wrong, ask me to paste exactly
what I see and help me fix it.

Facts you need:
- Install, Mac or Linux (Terminal): curl -fsSL https://kody-w.github.io/rapp-installer/install.sh | bash
- Install, Windows (PowerShell):    irm https://kody-w.github.io/rapp-installer/install.ps1 | iex
- It needs a GitHub account with Copilot. Copilot writes the answers over the internet;
  the Brainstem, its agents and its memory stay on my computer.
- If Python or Git is missing it installs them and may ask for my computer password.
- It opens in my browser and runs while that Terminal window is open. Running the
  install line again brings it back with its memory.
- Its folder: ~/.brainstem/src/rapp_brainstem (Windows: $HOME\.brainstem\src\rapp_brainstem).
  The page that tells it how to behave is soul.md there. Agents are in agents/.
- In the Brainstem window, the circled plus at the top right ("Manage installed agents")
  lists every agent, with an Export button for each. Dragging a file whose name ends in
  _agent.py onto the window adds it as a new agent.

The six steps:
1. Get my Brainstem with the install line for my computer.
2. Talk to it: help me tell it one thing to remember about me, like my favorite coffee.
   Tomorrow I ask it what it remembers.
3. See what it can do: open the circled plus and tell me what each agent does.
4. Read an agent: have me click Export next to ManageMemory and paste the file here. It is a
   short program for one job: saving what I ask it to remember. Explain it in plain words.
5. Make my own: help me pick a chore I repeat, then write a new agent just like
   ManageMemory for that chore. I save it as a file ending in _agent.py and drag it
   onto my Brainstem window. Then I try it.
6. Hand it on: help me send that one file to a friend, who drags it onto their
   Brainstem, or share it at https://github.com/kody-w/RAR.

When we finish, remind me: tomorrow it is still there, on my computer, remembering.
```
