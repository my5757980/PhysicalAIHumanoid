# PhysicalAIHumanoid - Physical AI & Humanoid Robotics Textbook

This is an AI-native textbook covering Physical AI, Humanoid Robotics, robotics foundations, AI for embodied intelligence, humanoid locomotion, manipulation, and autonomy. The textbook is built using [Docusaurus](https://docusaurus.io/) and includes an integrated RAG chatbot powered by Cohere and Qdrant.

## Features

- Comprehensive content on Physical AI & Humanoid Robotics
- Interactive chatbot with RAG (Retrieval-Augmented Generation)
- Text selection priority mode
- Source citations for all answers
- Streaming responses for better UX

## Installation

```bash
npm install
```

## Local Development

```bash
npm start
```

This command starts a local development server and opens up a browser window. Most changes are reflected live without having to restart the server.

## Build

```bash
npm run build
```

This command generates static content into the `build` directory and can be served using any static contents hosting service.

## Vercel Deployment

This project is configured for one-click deployment on Vercel. To deploy:

1. Push your code to a GitHub repository
2. Connect your repository to [Vercel](https://vercel.com)
3. Set the following environment variables in your Vercel project settings:
   - `COHERE_API_KEY`: Your Cohere API key
   - `QDRANT_URL`: Your Qdrant Cloud cluster URL
   - `QDRANT_API_KEY`: Your Qdrant API key
4. Vercel will automatically build and deploy your site

### Environment Variables for Vercel

For the RAG chatbot to work properly, you need to set these environment variables in your Vercel dashboard:

- `COHERE_API_KEY`: API key for Cohere (used for embeddings and text generation)
- `QDRANT_URL`: URL of your Qdrant Cloud instance
- `QDRANT_API_KEY`: API key for your Qdrant Cloud instance

## Local Development with Backend

If you want to run the full stack locally (frontend + backend):

1. Set up the backend:
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. Create a `.env` file in the `backend` directory:
   ```
   QDRANT_URL=your_qdrant_cluster_url
   QDRANT_API_KEY=your_qdrant_api_key
   COHERE_API_KEY=your_cohere_api_key
   ```

3. Ingest the documentation:
   ```bash
   python ingest_docs.py
   ```

4. Start the backend:
   ```bash
   uvicorn main:app --reload --port 8000
   ```

5. In the project root, start the frontend:
   ```bash
   npm start
   ```

## Architecture

- **Frontend**: Docusaurus 3 with React-based chat widget
- **Backend**: Vercel Edge Functions with Cohere and Qdrant
- **Database**: Qdrant Cloud for vector storage
- **Embeddings**: Cohere multilingual embeddings
- **Generation**: Cohere for responses

## License

This project is open source and available under the MIT License."# PhysicalAIHumanoid" 
