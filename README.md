# Overview

In order to learn about LLMs and practice Python, this repository aims to simulate what a user might enter into a search bar on a sports website. (It could be easily transferred to any other scenario).

The basic flow is as follows:
- Download and install the Phi4-mini model with Ollama
- Create a set of users (names, ages, moods...) and build a system prompt for each of them
- Get the LLM to suggest what the user searches in the search bar

The program is written in python and runs completely locally without any non-standard libraries.

Later, I could then tweak features like LLM temperature (a kind of unpredictability), the prompt and other factors to learn about LLMs and how to use them appropriately.

## Data Sources

Since I like simulations to be tied in realism, and it's often harder to "fake" data than it is to just get real data, I headed to Google and the Office of National Statistics (ONS) for some demographic data.

## Keeping the "database" simple

Plaintext movements and readability are important to me, so I've organised the data into textfiles in the simplest way I could think of: rows of data. Not even CSVs are simple enough! (Complications arise such as parsing delimiters and data types per column, missing column data...)

## Running the program

I have kept the Python script using only built-in modules, so any machine running Python 3 should be able to run this.

### Download Ollama

This should be straight forward on any operating system using the browser.

### Get the correct model running

Once Ollama is installed, run this command:
```ollama run phi4-mini```

This will check if the model has been downloaded, and if not download it from their servers.
It will then run the model (typically defaults to port 11434 - as hardcoded in the Python script too).

### Run the Python script

Run:
```python3 main.py Size Temp```
Where:
- Size is a positive integer for the number of users you wish to simulate,
- Temp is a value from 0 to 1 representing the temperature of the LLM (a measure of unpredictability with 0 being most predictable/deterministic) 

### For those without access to Ollama models

Initially I worked on a shared machine with network restrictions so I had to download the GGUF file via HuggingFace (a very strange website, but apparently the standard source for GGUF files and other LLMs). If you shalso have this restriction with Ollama, try downloading from Huggingface too here:

[Link-Phi4-Mini](https://huggingface.co/bartowski/microsoft_Phi-4-mini-instruct-GGUF/tree/main)

You should make sure the file is then downloaded into the same folder as this repository.
DO NOT commit the LLM to the commit history. It is not source code.

Once downloaded, you will need to make use of the Modelfile (which just has saved information about the LLM including the path to it) and create an alias for Ollama to use.

- Adjust the path in the Modelfile to suit your downloaded GGUF file
- Run ```ollama create phi4-mini -f ./Modelfile``` - this nicknames the model as "phi4-mini" - you can choose an alternative nickname
- Run ```ollama serve``` in the Modelfile directory

Note, if you'd like to play with the interactive chat version of a model, use the command:
```ollama run X``` where "X" is the name of your model

If you'd like to test the availability of the Ollama model try this shell command:

```
curl http://localhost:11434/api/chat -d '{
  "model": "phi4-mini",
  "messages": [
    { "role": "user", "content": "Explain quantum computing in one sentence." }
  ],
  "stream": false
}'
```
