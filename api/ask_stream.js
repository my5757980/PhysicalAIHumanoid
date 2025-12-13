export const config = { runtime: "edge" };

// Environment variables in Vercel Edge Runtime
const COHERE_API_KEY = process.env.COHERE_API_KEY;
const QDRANT_URL = process.env.QDRANT_URL;
const QDRANT_API_KEY = process.env.QDRANT_API_KEY;

// Collection name
const COLLECTION_NAME = "physical_ai_docs";

if (!COHERE_API_KEY || !QDRANT_URL || !QDRANT_API_KEY) {
  console.error("Missing required environment variables. Set COHERE_API_KEY, QDRANT_URL, QDRANT_API_KEY.");
}

const COHERE_API_URL = "https://api.cohere.ai/v1";

const getQdrantBaseUrl = () => {
  if (!QDRANT_URL) return null;
  return QDRANT_URL.endsWith('/') ? QDRANT_URL.slice(0, -1) : QDRANT_URL;
};

async function getEmbeddings(texts) {
  if (!COHERE_API_KEY) throw new Error("COHERE_API_KEY is not set");

  const response = await fetch(`${COHERE_API_URL}/embed`, {
    method: "POST",
    headers: {
      "Authorization": `Bearer ${COHERE_API_KEY}`,
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      texts: texts,
      model: "embed-english-v3.0",
      input_type: "search_document"
    })
  });

  if (!response.ok) {
    const errorData = await response.json();
    throw new Error(`Cohere API error: ${response.status} - ${JSON.stringify(errorData)}`);
  }

  const data = await response.json();
  return data.embeddings;
}

async function searchDocuments(query, maxResults = 5) {
  if (!QDRANT_API_KEY || !getQdrantBaseUrl()) throw new Error("QDRANT_URL or QDRANT_API_KEY is not set");

  const queryEmbedding = await getEmbeddings([query]);
  const queryVector = queryEmbedding[0];

  const qdrantResponse = await fetch(`${getQdrantBaseUrl()}/collections/${COLLECTION_NAME}/points/search`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Api-Key": QDRANT_API_KEY
    },
    body: JSON.stringify({
      vector: queryVector,
      limit: maxResults,
      with_payload: true
    })
  });

  if (!qdrantResponse.ok) {
    const errorData = await qdrantResponse.json();
    throw new Error(`Qdrant search error: ${qdrantResponse.status} - ${JSON.stringify(errorData)}`);
  }

  const searchData = await qdrantResponse.json();

  return searchData.result.map(point => ({
    id: point.id,
    text: point.payload.text || "",
    chapter: point.payload.chapter || "",
    section: point.payload.section || "",
    score: point.score,
    metadata: point.payload.metadata || {}
  }));
}

function detectHallucination(answer, context, sources = null) {
  const answerLower = answer.toLowerCase();
  const contextLower = context.toLowerCase();
  const keyTerms = answerLower.match(/\b(physical ai|humanoid|robotics|kinematics|dynamics|control|embodiment|perception|learning|actuators|sensors|locomotion|manipulation|slam|reinforcement learning|imitation learning)\b/g) || [];
  const matchedTerms = keyTerms.filter(term => contextLower.includes(term));
  const confidenceScore = keyTerms.length > 0 ? matchedTerms.length / keyTerms.length : 1.0;
  const uncertaintyPhrases = ["i don't know", "not mentioned", "not specified", "not found", "not in the text"];
  const hasUncertainty = uncertaintyPhrases.some(phrase => answerLower.includes(phrase));

  let citationAccuracy = 1.0;
  const citationIssues = [];
  if (sources && sources.length > 0) {
    const sourceTexts = sources.map(source => source.text.toLowerCase());
    const sourceFullText = sourceTexts.join(" ");
    const sourceMatchedTerms = keyTerms.filter(term => sourceFullText.includes(term));
    citationAccuracy = keyTerms.length > 0 ? sourceMatchedTerms.length / keyTerms.length : 1.0;
    if (sourceMatchedTerms.length < matchedTerms.length) citationIssues.push("Some concepts in the answer may not be fully supported by the provided sources");
  }

  const hasHallucination = confidenceScore < 0.3 && !hasUncertainty;
  const hasCitationIssues = citationAccuracy < 0.5;

  return {
    has_hallucination: hasHallucination,
    has_citation_issues: hasCitationIssues,
    confidence_score: confidenceScore,
    citation_accuracy: citationAccuracy,
    matched_terms: matchedTerms,
    total_terms: keyTerms.length,
    citation_issues: citationIssues,
    has_uncertainty_indicators: hasUncertainty,
    message: hasHallucination || hasCitationIssues
      ? "Potential issues detected: low confidence in context support or citation accuracy"
      : `Answer validation: ${(confidenceScore*100).toFixed(2)}% of key terms found in context, citation accuracy: ${(citationAccuracy*100).toFixed(2)}%`
  };
}

export default async function handler(req) {
  if (req.method !== "POST") {
    return new Response(JSON.stringify({ error: "Method not allowed" }), {
      status: 405,
      headers: { "Content-Type": "application/json" }
    });
  }

  try {
    const { query, selected_text, max_results = 5, temperature = 0.7 } = await req.json();
    if (!query) return new Response(JSON.stringify({ error: "Query is required" }), { status: 400, headers: { "Content-Type": "application/json" } });

    const searchResults = await searchDocuments(query, max_results);
    const contextParts = searchResults.map(res => res.text);
    const sources = searchResults.map(r => ({
      id: r.id,
      text: r.text.length > 200 ? r.text.substring(0,200)+"..." : r.text,
      chapter: r.chapter,
      section: r.section,
      relevance_score: r.score
    }));
    const context = contextParts.join("\n\n");

    const stream = new ReadableStream({
      async start(controller) {
        try {
          controller.enqueue(`data: ${JSON.stringify({ type: "sources", sources, query })}\n\n`);
          const finalPrompt = `Based on the following context from the Physical AI & Humanoid Robotics textbook, please answer the user's question.\n\nContext:\n${context}\n\nUser's question: ${query}\n\nProvide a clear, concise answer based on context, citing relevant sections when possible.`;

          const response = await fetch(`${COHERE_API_URL}/chat`, {
            method: "POST",
            headers: {
              "Authorization": `Bearer ${COHERE_API_KEY}`,
              "Content-Type": "application/json",
              "Accept": "text/event-stream"
            },
            body: JSON.stringify({ message: finalPrompt, model: "command-r-08-2024", temperature, stream: true })
          });

          if (!response.ok) throw new Error(`Cohere API error: ${response.status}`);

          const reader = response.body.getReader();
          const decoder = new TextDecoder();
          let fullAnswer = "";

          while (true) {
            const { done, value } = await reader.read();
            if (done) break;
            const chunk = decoder.decode(value, { stream: true });
            const lines = chunk.split('\n');
            for (const line of lines) {
              if (line.trim() && line.startsWith("data: ")) {
                const data = line.slice(6).trim();
                if (data === "[DONE]") continue;
                try {
                  const parsed = JSON.parse(data);
                  if (parsed.event_type === "text-generation" && parsed.text) {
                    fullAnswer += parsed.text;
                    controller.enqueue(`data: ${JSON.stringify({ type: "answer_chunk", content: parsed.text })}\n\n`);
                  } else if (parsed.event_type === "stream-end") break;
                } catch { continue; }
              }
            }
          }

          const validationResult = detectHallucination(fullAnswer, context, sources);
          controller.enqueue(`data: ${JSON.stringify({ type: "completion", answer: fullAnswer, validation: validationResult })}\n\n`);
          controller.close();
        } catch (error) {
          console.error("Streaming error:", error);
          controller.enqueue(`data: ${JSON.stringify({ type: "error", message: error.message })}\n\n`);
          controller.close();
        }
      }
    });

    return new Response(stream, {
      headers: { "Content-Type": "text/plain", "Cache-Control": "no-cache", "Connection": "keep-alive" }
    });

  } catch (error) {
    console.error("API error:", error);
    return new Response(JSON.stringify({ error: error.message }), { status: 500, headers: { "Content-Type": "application/json" } });
  }
}
