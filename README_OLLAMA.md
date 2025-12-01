# NovaBoard Local AI Setup (Ollama)

NovaBoard uses a local LLM via Ollama to provide privacy-focused, offline-capable AI assistance.

## Prerequisites

1.  **Install Ollama**:
    - macOS / Linux: `curl -fsSL https://ollama.com/install.sh | sh`
    - Windows: Download from [ollama.com](https://ollama.com)

2.  **Pull the Model**:
    We recommend `llama3.2` (lightweight, 3B parameters) or `mistral` for better reasoning.
    
    ```bash
    ollama pull llama3.2
    ```
    
    Or for very low-end devices:
    ```bash
    ollama pull tinyllama
    ```

3.  **Start Ollama Service**:
    Ensure Ollama is running on the default port (11434).
    
    ```bash
    ollama serve
    ```

## Integration

The NovaBoard backend (`backend/routes/ai.py`) attempts to connect to `http://localhost:11434/api/generate`.

- If connected: It sends the board context + user query to the local model.
- If failed: It falls back to a "Mock AI" mode for demonstration purposes.

## Troubleshooting

- **"Backend offline" toast**: Ensure `python backend/app.py` is running.
- **"Using mock AI" toast**: Ensure Ollama is running (`ollama serve`) and the model is pulled.
