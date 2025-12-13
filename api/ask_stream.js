export const config = {
  runtime: "edge",
};

const COHERE_API_KEY = process.env.COHERE_API_KEY;
const QDRANT_URL = process.env.QDRANT_URL;
const QDRANT_API_KEY = process.env.QDRANT_API_KEY;

const COLLECTION_NAME = "physical_ai_docs";
const COHERE_API_URL = "https://api.cohere.ai/v1";

const getQdrantBaseUrl = () =>
  QDRANT_URL.endsWith("/") ? QDRANT_URL.slice(0, -1) : QDRANT_URL;

// ---------- SAFETY CHECK ----------
function checkEnv() {
  if (!COHERE_API_KEY || !QDRANT_URL || !QDRANT_API_KEY) {
    throw new Error("Missing environment variables on Vercel");
  }
}

// ---------- EMBEDDINGS ----------
async function getEmbeddings(texts) {
  const res = await fetch(`${COHERE_API_URL}/embed`, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${COHERE_API_KEY}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      texts,
      model: "embed-english-v3.0",
      input_type: "search_document",
    }),
  });

  if (!res.ok) {
    throw new Error(`Cohere embed error: ${res.status}`);
  }

  const data = await res.json();
  return data.embeddings;
}

// ---------- QDRANT SEARCH ----------
async function searchDocuments(query, maxResults = 5) {
  const [queryVector] = await getEmbeddings([query]);

  const res = await fetch(
    `${getQdrantBaseUrl()}/collections/${COLLECTION_NAME}/points/search`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Api-Key": QDRANT_API_KEY,
      },
      body: JSON.stringify({
        vector: queryVector,
        limit: maxResults,
        with_payload: true,
      }),
    }
  );

  if (!res.ok) {
    throw new Error(`Qdrant search error: ${res.status}`);
  }

  const data = await res.json();

  return data.result.map((p) => ({
    id: p.id,
    text: p.payload?.text || "",
    chapter: p.payload?.chapter || "",
    section: p.payload?.section || "",
    score: p.score,
  }));
}

// ---------- SIMPLE VALIDATION ----------
function detectHallucination(answer, context) {
  const keyTerms = [
    "physical ai",
    "humanoid",
    "robotics",
    "kinematics",
    "dynamics",
    "control",
    "embodiment",
  ];

  const matched = keyTerms.filter(
    (t) =>
      answer.toLowerCase().includes(t) &&
      context.toLowerCase().includes(t)
  );

  return {
    confidence_score: matched.length / keyTerms.length,
  };
}

// ---------- HANDLER ----------
export default async function handler(req) {
  if (req.method !== "POST") {
    return new Response(
      JSON.stringify({ error: "Method not allowed" }),
      { status: 405 }
    );
  }

  try {
    checkEnv();

    const { query, max_results = 5, temperature = 0.7 } =
      await req.json();

    if (!query) {
      return new Response(
        JSON.stringify({ error: "Query is required" }),
        { status: 400 }
      );
    }

    const searchResults = await searchDocuments(query, max_results);
    const context = searchResults.map((r) => r.text).join("\n\n");

    const prompt = `
Answer strictly based on the context below.
If the answer is not in the context, say "Not found in the book".

Context:
${context}

Question:
${query}
`;

    const chatRes = await fetch(`${COHERE_API_URL}/chat`, {
      method: "POST",
      headers: {
        Authorization: `Bearer ${COHERE_API_KEY}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        model: "command-r-08-2024",
        message: prompt,
        temperature,
      }),
    });

    if (!chatRes.ok) {
      throw new Error(`Cohere chat error: ${chatRes.status}`);
    }

    const chatData = await chatRes.json();

    const answer =
      chatData?.text ||
      chatData?.message?.content?.[0]?.text ||
      "No answer generated";

    const validation = detectHallucination(answer, context);

    return new Response(
      JSON.stringify({
        answer,
        validation,
        sources: searchResults,
      }),
      { headers: { "Content-Type": "application/json" } }
    );
    } catch (error) {
  console.error("API ERROR:", error);

  return new Response(
    JSON.stringify({
      answer: "Backend error: " + error.message,
      sources: [],
      validation: { confidence_score: 0 }
    }),
    { status: 500 }
  );
}
}

  