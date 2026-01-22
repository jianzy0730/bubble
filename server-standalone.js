/**
 * Dependency-free HTTP server (Node >=18) serving static files + LLM proxy.
 * No npm install required; run: node server-standalone.js
 */
const http = require("http");
const fs = require("fs");
const path = require("path");
const url = require("url");

const port = process.env.PORT || 3000;
const root = __dirname;

const mime = {
  ".html": "text/html; charset=utf-8",
  ".js": "application/javascript; charset=utf-8",
  ".css": "text/css; charset=utf-8",
  ".json": "application/json; charset=utf-8",
  ".ico": "image/x-icon",
  ".svg": "image/svg+xml",
  ".png": "image/png",
  ".jpg": "image/jpeg",
  ".jpeg": "image/jpeg",
};

function withCors(headers = {}) {
  return {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET,POST,OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type,Authorization",
    ...headers,
  };
}

function send(res, status, body, headers = {}) {
  const payload = typeof body === "string" ? body : JSON.stringify(body);
  const finalHeaders = withCors({
    "Content-Type": headers["Content-Type"] || "application/json; charset=utf-8",
    ...headers,
  });
  res.writeHead(status, finalHeaders);
  res.end(payload);
}

function serveStatic(req, res, pathname) {
  const safePath = pathname === "/" ? "/index.html" : pathname;
  const filePath = path.normalize(path.join(root, safePath));
  if (!filePath.startsWith(root)) return send(res, 403, { error: "Forbidden" });
  fs.readFile(filePath, (err, data) => {
    if (err) {
      if (err.code === "ENOENT") return send(res, 404, { error: "Not found" });
      return send(res, 500, { error: "Read error" });
    }
    const ext = path.extname(filePath);
    res.writeHead(200, withCors({ "Content-Type": mime[ext] || "application/octet-stream" }));
    res.end(data);
  });
}

function parseBody(req) {
  return new Promise((resolve, reject) => {
    let data = "";
    req.on("data", (chunk) => {
      data += chunk;
      if (data.length > 1_000_000) {
        req.destroy();
        reject(new Error("Payload too large"));
      }
    });
    req.on("end", () => {
      try {
        resolve(data ? JSON.parse(data) : {});
      } catch (e) {
        reject(new Error("Invalid JSON"));
      }
    });
    req.on("error", reject);
  });
}

function buildPrompt({ persona = {}, mood, context }) {
  const name = persona.name || "<fill persona name>";
  const role = persona.role || "<fill persona role>";
  const tone = persona.tone || "<fill tone>";
  const style = persona.style || "<fill style>";
  const boundaries =
    persona.boundaries ||
    "Keep it brief (80-150 chars), supportive, and avoid medical or legal advice.";
  const background = persona.background || "<add background or leave blank>";

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
  if (!res.ok) throw new Error(`OpenAI request failed: ${res.status} ${await res.text()}`);
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
  if (!res.ok) throw new Error(`Google request failed: ${res.status} ${await res.text()}`);
  const data = await res.json();
  return data?.candidates?.[0]?.content?.parts?.[0]?.text?.trim();
}

const server = http.createServer(async (req, res) => {
  const { pathname } = url.parse(req.url);

  if (req.method === "OPTIONS") {
    res.writeHead(200, withCors());
    res.end();
    return;
  }

  if (pathname === "/api/comfort" && req.method === "POST") {
    try {
      const { mood, persona, context, provider = "openai", clientConfig = {} } = await parseBody(req);
      if (!mood) return send(res, 400, { error: "mood is required" });

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
      return send(res, 200, { provider, text, prompt });
    } catch (err) {
      return send(res, 500, { error: err.message || "LLM call failed" });
    }
  }

  if (pathname === "/api/tts/minimax" && req.method === "POST") {
    const body = await parseBody(req).catch(() => ({}));
    if (!body.text) return send(res, 400, { error: "text is required" });

    const key = body.apiKey || process.env.MINIMAX_API_KEY;
    if (!key) return send(res, 400, { error: "Missing Minimax API key" });

    try {
      const endpoint = process.env.MINIMAX_BASE_URL || "https://api-bj.minimaxi.com/v1/t2a_v2";
      const payload = {
        model: body.model || "speech-01-hd",
        text: body.text,
        stream: false,
        output_format: body.outputFormat || "url",
      };
      if (body.voiceId) payload.voice_setting = { voice_id: body.voiceId };

      const ttsRes = await fetch(endpoint, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${key}`,
        },
        body: JSON.stringify(payload),
      });

      const ttsJson = await ttsRes.json().catch(() => ({}));
      if (!ttsRes.ok) {
        const errMsg = ttsJson?.base_resp?.status_msg || ttsJson?.error || ttsRes.statusText;
        return send(res, ttsRes.status, { error: `Minimax TTS failed: ${errMsg}` });
      }

      const baseResp = ttsJson.base_resp || ttsJson.baseResp;
      if (baseResp && baseResp.status_code && Number(baseResp.status_code) !== 0) {
        return send(res, 500, { error: baseResp.status_msg || "Minimax TTS error" });
      }

      const data = ttsJson.data || {};
      const audioUrl =
        data.audio_url ||
        data.url ||
        (typeof data.audio === "string" && data.audio.startsWith("http") ? data.audio : null);

      let audioBase64 = null;
      if (!audioUrl && typeof data.audio === "string") {
        const hex = data.audio.trim();
        const looksHex = /^[0-9a-fA-F]+$/.test(hex);
        if (looksHex && hex.length % 2 === 0) {
          audioBase64 = Buffer.from(hex, "hex").toString("base64");
        }
      }

      if (!audioUrl && !audioBase64) {
        return send(res, 500, { error: "Minimax TTS succeeded but returned no audio" });
      }

      return send(res, 200, {
        audioUrl,
        audioBase64,
        mimeType: audioBase64 ? "audio/mpeg" : undefined,
        traceId: data.trace_id || ttsJson.trace_id,
        raw: process.env.NODE_ENV === "development" ? ttsJson : undefined,
      });
    } catch (err) {
      return send(res, 500, { error: err.message || "Minimax TTS failed" });
    }
  }

  if (pathname === "/api/health" && req.method === "GET") {
    return send(res, 200, {
      ok: true,
      providerReady: !!(process.env.OPENAI_API_KEY || process.env.GOOGLE_API_KEY),
    });
  }

  return serveStatic(req, res, pathname);
});

server.listen(port, () => {
  console.log(`Standalone server running at http://localhost:${port}`);
});
