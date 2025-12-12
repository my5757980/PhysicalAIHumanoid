export const config = { runtime: "edge" };

import fetch from "node-fetch";

export default async function handler(request) {
  try {
    const { query } = await request.json();

    // Environment variables
    const COHERE_API_KEY = process.env.COHERE_API_KEY;
    const QDRANT_URL = process.env.QDRANT_URL;
    const QDRANT_API_KEY = process.env.QDRANT_API_KEY;

    if (!COHERE_API_KEY || !QDRANT_URL || !QDRANT_API_KEY) {
      return new Response(
        JSON.stringify({ type: "error", message: "Missing environment variables" }),
        { status: 500 }
      );
    }

    // 1️⃣ Search documents from Qdrant
    const qdrantResp = await fetch(`${QDRANT_URL}/collections/physical_ai_docs/points/scroll?limit=5`, {
      headers: { "api-key": QDRANT_API_KEY }
    });

    const qdrantData = await qdrantResp.json();
    const search_results = qdrantData.points || [];

    const sources = search_results.map(r => ({
      id: r.id,
      text: r.payload.text?.slice(0, 200) + (r.payload.text?.length>200?"...":""),
      chapter: r.payload.chapter || "",
      section: r.payload.section || "",
      score: r.vector ? 1.0 : 0.0
    }));

    const context = search_results.map(r => r.payload.text).join("\n\n");

    // 2️⃣ Prepare Cohere prompt
    const final_prompt = `Based on the following context from the Physical AI & Humanoid Robotics textbook, please answer the user's question. If the context doesn't contain the information needed to answer the question, please say so clearly.

Context:
${context}

User's question: ${query}

Please provide a clear, concise answer based on the context, and cite relevant sections when possible.`;

    // 3️⃣ Call Cohere chat API with streaming
    const cohereResp = await fetch("https://api.cohere.com/v2/chat", {
      method: "POST",
      headers: {
        "Authorization": `Bearer ${COHERE_API_KEY}`,
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        model: "command-r-08-2024",
        message: final_prompt,
        stream: true
      })
    });

    // 4️⃣ Stream response directly
    return new Response(cohereResp.body, {
      headers: { "Content-Type": "text/event-stream" }
    });

  } catch (err) {
    return new Response(
      JSON.stringify({ type: "error", message: err.message }),
      { status: 500 }
    );
  }
}
