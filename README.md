# User Simulation overview

The basic idea behind this repository is to:
- Use demographic datasets (e.g. from the Office of National Statistics) to create a population of representative people
- Use additional information and randomly chosen data to give each person a backstory (desires, family, interests) based on reasonable assumptions
- Generate a context from this data that a local LLM can understand to output realistic search queries
   (in this case Phi4 Mini from Microsoft, served via Ollama)
- Use this data to assess the accuracy of an existing search algorithm

## Running the script

I have kept the Python script using only built-in modules, so any machine running Python 3 should be able to run this.
I also had to:
- Install Ollama, but note I didn't get the LLM model GGUF file (a compressed LLM file) from Ollama due to network restrictions
- I downloaded Phi4-Mini from Huggingface, one of the weirdest websites I've ever used!

[Link-Phi4-Mini](https://huggingface.co/bartowski/microsoft_Phi-4-mini-instruct-GGUF/tree/main)

- You want the download for the model: `microsoft_Phi-4-mini-instruct-Q4_K_M.gguf` - ideally into this repository
- I've made the Modelfile (no extension) to direct ollama to the gguf file
- Now run ```ollama create phi4-sim -f ./Modelfile``` to tell ollama your nickname for the model and its location
- If the Model you downloaded has been saved elsewhere, modify the Modelfile to point to wherever your model is saved
- Then run the command ```ollama serve``` which serves the LLM on localhost port 11434. Key point: this is served with NO CONTEXT (turns out without it, LLMs are very unhelpful - hence a great deal of frustration with the repository involves tweaking the initial context we provide it)
- Note you can also play with the chat version separately via ollama by running ```ollama run phi4-sim``` which includes ollama's chat context
