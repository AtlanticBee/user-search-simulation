# User Simulation overview

The basic idea behind this repository is to:
- Use demographic datasets (e.g. from the Office of National Statistics) to create a population of representative people
- Use additional information and randomly chosen data to give each person a backstory (desires, family, interests) based on reasonable assumptions
- Generate a context from this data that a local LLM can understand to output realistic search queries
   (in this case Phi4 Mini from Microsoft, served via Ollama)
- Use this data to assess the accuracy of an existing search algorithm

## Running the script

I have kept the Python script using only built-in modules, so any machine running Python 3 should be able to run this.

Initially I worked on a shared machine with network restrictions so I had to download the GGUF file via HuggingFace (a very strange website, but apparently the standard source for GGUF files and other LLMs). Now however on my own machine I'm just using Ollama's CLI and then using the default Phi4:Mini model.

If you are downloading the LLM from HuggingFace, download this version:
[Link-Phi4-Mini](https://huggingface.co/bartowski/microsoft_Phi-4-mini-instruct-GGUF/tree/main)

You should make sure the file is then downloaded into the same folder as this repository.
DO NOT commit the LLM to the commit history. It is not source code.

- I've made the Modelfile (no extension) to direct ollama to the gguf file
- Now run ```ollama create phi4-mini -f ./Modelfile``` to tell ollama your nickname for the model and its location - the Modelfile should contain: FROM microsoft_Phi-4-mini-instruct-Q4_K_M.gguf
- If the Model you downloaded has been saved elsewhere, modify the Modelfile to point to wherever your model is saved
- Then run the command ```ollama serve``` which serves the LLM on localhost port 11434. Key point: this is served with NO CONTEXT (turns out without it, LLMs are very unhelpful - hence a great deal of frustration with the repository involves tweaking the initial context we provide it)
- Note you can also play with the chat version separately via ollama by running ```ollama run phi4-sim``` which includes ollama's chat context

If you're just using Ollama's LLMs, then do this:
- Run ```ollama run phi4-mini```

This command automatically runs and serves the LLM on port 11434 and can be interacted with e.g.

```
curl http://localhost:11434/api/chat -d '{
  "model": "phi4-mini",
  "messages": [
    { "role": "user", "content": "Explain quantum computing in one sentence." }
  ],
  "stream": false
}'
```
