export const config = { runtime: "edge" };

// Environment variables
const COHERE_API_KEY = process.env.COHERE_API_KEY;
const QDRANT_URL = process.env.QDRANT_URL;
const QDRANT_API_KEY = process.env.QDRANT_API_KEY;

const COLLECTION_NAME = "physical_ai_docs";
const COHERE_API_URL = "https://api.cohere.ai/v1";

if (!COHERE_API_KEY || !QDRANT_URL || !QDRANT_API_KEY) {
  console.error("Missing required environment variables: COHERE_API_KEY, QDRANT_URL, QDRANT_API_KEY");
}

// Normalize Qdrant URL
const getQdrantBaseUrl = () => QDRANT_URL.endsWith('/') ? QDRANT_URL.slice(0, -1) : QDRANT_URL;

// Get embeddings from Cohere
async function getEmbeddings(texts) {
  const res = await fetch(`${COHERE_API_URL}/embed`, {
    method: "POST",
    headers: {
      "Authorization": `Bearer ${COHERE_API_KEY}`,
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ texts, model: "embed-english-v3.0", input_type: "search_document" })
  });

  if (!res.ok) throw new Error(`Cohere embed API error: ${res.status}`);
  const data = await res.json();
  return data.embeddings;
}

// Search Qdrant
async function searchDocuments(query, maxResults = 5) {
  if (!QDRANT_API_KEY) throw new Error("Qdrant API key missing");

  const [queryVector] = await getEmbeddings([query]);

  const res = await fetch(`${getQdrantBaseUrl()}/collections/${COLLECTION_NAME}/points/search`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Api-Key": QDRANT_API_KEY
    },
    body: JSON.stringify({ vector: queryVector, limit: maxResults, with_payload: true })
  });




  const data = await res.json();
  console.log(data.answer);
}

askBot("What is Physical AI?");





  if (!res.ok) throw new Error(`Qdrant search error: ${res.status}`);
  const data = await res.json();

  return data.result.map(point => ({
    id: point.id,
    text: point.payload.text || "",
    chapter: point.payload.chapter || "",
    section: point.payload.section || "",
    score: point.score
  }));


// Simple hallucination detection
function detectHallucination(answer, context) {
  const keyTerms = ["physical ai","humanoid","robotics","kinematics","dynamics","control","embodiment"];
  const matchedTerms = keyTerms.filter(t => answer.toLowerCase().includes(t) && context.toLowerCase().includes(t));
  const confidence = keyTerms.length ? matchedTerms.length / keyTerms.length : 1.0;
  return { confidence_score: confidence };
}

// Edge API handler
export default async function handler(req) {
  if (req.method !== "POST") {
    return new Response(JSON.stringify({ error: "Method not allowed" }), { status: 405 });
  }

  try {
    const { query, max_results = 5, temperature = 0.7 } = await req.json();
    if (!query) return new Response(JSON.stringify({ error: "Query is required" }), { status: 400 });

    const searchResults = await searchDocuments(query, max_results);
    const context = searchResults.map(r => r.text).join("\n\n");

    const prompt = `Answer user query based on this context:\n${context}\n\nUser: ${query}\n`;

    const chatRes = await fetch(`${COHERE_API_URL}/chat`, {
      method: "POST",
      headers: {
        "Authorization": `Bearer ${COHERE_API_KEY}`,
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ message: prompt, model: "command-r-08-2024", temperature, stream: false })
    });

    if (!chatRes.ok) throw new Error(`Cohere chat API error: ${chatRes.status}`);
    const chatData = await chatRes.json();
    const answer = chatData?.text || "No answer generated";

    const validation = detectHallucination(answer, context);

    return new Response(JSON.stringify({ answer, validation, sources: searchResults }), {
      headers: { "Content-Type": "application/json" }
    });

  } catch (error) {
    console.error("API error:", error);
    return new Response(JSON.stringify({ error: error.message }), { status: 500 });
  }
}
