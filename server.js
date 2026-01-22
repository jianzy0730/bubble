/**
 * Minimal backend for composing comforting prompts and calling LLM providers.
 * - Providers: OpenAI (default) + Google Gemini.
 * - Persona + mood are stitched into a prompt; no opinionated persona defaults.
 * - Minimax TTS placeholder route is provided for future wiring.
 *
 * Env keys to set before running:
 *   OPENAI_API_KEY=...
 *   OPENAI_MODEL=gpt-4o-mini            # or any chat model
 *   OPENAI_BASE_URL=https://api.openai.com/v1 (optional override, e.g., proxies)
 *   GOOGLE_API_KEY=...
 *   GOOGLE_MODEL=gemini-1.5-pro-latest
 *   PORT=3000
 */

const express = require("express");
const cors = require("cors");

const app = express();
const port = process.env.PORT || 3000;

app.use(cors());
app.use(express.json({ limit: "1mb" }));
app.use(express.static(__dirname)); // serve index.html/settings.html directly

/**
 * Build a prompt from persona + mood + optional situational context.
 * Everything is placeholder friendly so users can drop in their own flavor text.
 */
function buildPrompt({ persona = {}, mood, context }) {
  const name = persona.name || "<fill persona name>";
  const role = persona.role || "<fill persona role>";
  const tone = persona.tone || "<fill tone (gentle/warm/etc.)>";
  const style = persona.style || "<fill style (concise/storytelling/etc.)>";
  const boundaries =
    persona.boundaries ||
    "Keep it brief (80-150 chars), supportive, and avoid medical or legal advice.";
  const background =
    persona.background || "<add background/personality seeds or leave blank>";

  return [
    `You are ${name}, ${role}.`,
    `Tone: ${tone}. Style: ${style}.`,
    `Background: ${background}.`,
    boundaries,
    `User mood/state: ${mood || "<no mood provided>"}.`,
    context ? `Recent events: ${context}.` : "No extra events provided.",
    "Craft a short, empathetic reply that acknowledges the mood and offers comfort.",
  ].join("\n");
}

async function callOpenAI({ prompt, apiKey, model, baseUrl }) {
  if (!apiKey) throw new Error("Missing OPENAI_API_KEY");
  const endpoint = `${baseUrl || "https://api.openai.com/v1"}/chat/completions`;
  const body = {
    model: model || "gpt-4o-mini",
    temperature: 0.7,
    messages: [
      { role: "system", content: "You are a supportive companion. Keep replies concise and kind." },
      { role: "user", content: prompt },
    ],
  };

  const res = await fetch(endpoint, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${apiKey}`,
    },
    body: JSON.stringify(body),
  });

  if (!res.ok) {
    const errorBody = await res.text();
    throw new Error(`OpenAI request failed: ${res.status} ${errorBody}`);
  }

  const data = await res.json();
  return data?.choices?.[0]?.message?.content?.trim();
}

async function callGoogle({ prompt, apiKey, model }) {
  if (!apiKey) throw new Error("Missing GOOGLE_API_KEY");
  const endpoint = `https://generativelanguage.googleapis.com/v1beta/models/${model || "gemini-1.5-pro-latest"}:generateContent?key=${apiKey}`;
  const body = {
    contents: [{ parts: [{ text: prompt }] }],
    generationConfig: { temperature: 0.7 },
  };

  const res = await fetch(endpoint, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });

  if (!res.ok) {
    const errorBody = await res.text();
    throw new Error(`Google request failed: ${res.status} ${errorBody}`);
  }

  const data = await res.json();
  return data?.candidates?.[0]?.content?.parts?.[0]?.text?.trim();
}

app.post("/api/comfort", async (req, res) => {
  try {
    const { mood, persona, context, provider = "openai", clientConfig = {} } = req.body || {};
    if (!mood) return res.status(400).json({ error: "mood is required" });

    const prompt = buildPrompt({ persona, mood, context });

    let text;
    if (provider === "google") {
      text = await callGoogle({
        prompt,
        apiKey: clientConfig.googleKey || process.env.GOOGLE_API_KEY,
        model: clientConfig.googleModel || process.env.GOOGLE_MODEL,
      });
    } else {
      text = await callOpenAI({
        prompt,
        apiKey: clientConfig.openaiKey || process.env.OPENAI_API_KEY,
        model: clientConfig.openaiModel || process.env.OPENAI_MODEL,
        baseUrl: clientConfig.openaiBaseUrl || process.env.OPENAI_BASE_URL,
      });
    }

    res.json({ provider, text, prompt });
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: err.message || "LLM call failed" });
  }
});

/**
 * Minimax TTS (sync HTTP, non-streaming).
 * Expects JSON: { text, voiceId?, model?, apiKey?, outputFormat? }
 */
app.post("/api/tts/minimax", async (req, res) => {
  try {
    const { text, voiceId, model, apiKey, outputFormat } = req.body || {};
    if (!text) return res.status(400).json({ error: "text is required" });

    const key = apiKey || process.env.MINIMAX_API_KEY;
    if (!key) return res.status(400).json({ error: "Missing Minimax API key" });

    const endpoint = process.env.MINIMAX_BASE_URL || "https://api-bj.minimaxi.com/v1/t2a_v2";
    const body = {
      model: model || "speech-01-hd",
      text,
      stream: false,
      output_format: outputFormat || "url", // request short-lived URL to avoid hex decoding on client
    };
    if (voiceId) body.voice_setting = { voice_id: voiceId };

    const ttsRes = await fetch(endpoint, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${key}`,
      },
      body: JSON.stringify(body),
    });

    const ttsJson = await ttsRes.json().catch(() => ({}));
    if (!ttsRes.ok) {
      const errMsg = ttsJson?.base_resp?.status_msg || ttsJson?.error || ttsRes.statusText;
      return res.status(ttsRes.status).json({ error: `Minimax TTS failed: ${errMsg}` });
    }

    // base_resp/status_code handling
    const baseResp = ttsJson.base_resp || ttsJson.baseResp;
    if (baseResp && baseResp.status_code && Number(baseResp.status_code) !== 0) {
      return res.status(500).json({ error: baseResp.status_msg || "Minimax TTS error" });
    }

    const data = ttsJson.data || {};
    const audioUrl =
      data.audio_url ||
      data.url ||
      (typeof data.audio === "string" && data.audio.startsWith("http") ? data.audio : null);

    // Some responses return hex; convert if needed so the frontend can play it.
    let audioBase64 = null;
    if (!audioUrl && typeof data.audio === "string") {
      const hex = data.audio.trim();
      const looksHex = /^[0-9a-fA-F]+$/.test(hex);
      if (looksHex && hex.length % 2 === 0) {
        audioBase64 = Buffer.from(hex, "hex").toString("base64");
      }
    }

    if (!audioUrl && !audioBase64) {
      return res.status(500).json({ error: "Minimax TTS succeeded but returned no audio" });
    }

    res.json({
      audioUrl,
      audioBase64,
      mimeType: audioBase64 ? "audio/mpeg" : undefined,
      traceId: data.trace_id || ttsJson.trace_id,
      raw: process.env.NODE_ENV === "development" ? ttsJson : undefined,
    });
  } catch (err) {
    console.error("Minimax TTS error", err);
    res.status(500).json({ error: err.message || "Minimax TTS failed" });
  }
});

app.get("/api/health", (_req, res) => {
  res.json({ ok: true, providerReady: !!(process.env.OPENAI_API_KEY || process.env.GOOGLE_API_KEY) });
});

app.listen(port, () => {
  console.log(`Comfort backend listening on http://localhost:${port}`);
});
