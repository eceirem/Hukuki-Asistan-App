"""Explainable-AI (XAI) service — natural-language retrieval explanations.

Gated by ``settings.ENABLE_LLM_XAI``.  When the flag is OFF (the default), the
search pipeline simply surfaces the best-matching chunk text verbatim and this
module is never invoked.  When the flag is ON, the search route awaits
:func:`generate_xai_explanation` for the top-1 retrieved case to obtain a
human-readable answer to "Neden bu karar getirildi?".

Provider
────────
OpenRouter API (OpenAI-compatible) via the official ``openai`` Python SDK
(``AsyncOpenAI``).  The SDK handles base-URL resolution correctly and keeps
the FastAPI event loop unblocked.

Configure in ``.env``:
    LLM_API_URL=https://openrouter.ai/api/v1
    LLM_API_TOKEN=sk-or-v1-...
    LLM_MODEL_NAME=meta-llama/llama-3.2-3b-instruct:free
    ENABLE_LLM_XAI=True
"""

from __future__ import annotations

import logging
import re

from openai import AsyncOpenAI

from app.core.config import settings

logger = logging.getLogger(__name__)

client = AsyncOpenAI(
    base_url=settings.LLM_API_URL,
    api_key=settings.LLM_API_TOKEN,
)

_SYSTEM_MESSAGE = (
    "Sen katı bir hukuki asistansın. "
    "Sadece nihai açıklamayı ver. "
    "Düşünme sürecini, iç sesini veya <unused0> gibi etiketleri kesinlikle "
    "yanıta dahil etme."
)

_USER_TEMPLATE = """\
Aşağıda bir Türk hukuk arama motorunun kullanıcıya sunmak üzere seçtiği \
bir mahkeme kararı parçası ile orijinal sorgu yer almaktadır.

Görevin: 1-2 kısa Türkçe cümleyle, bu kararın neden kullanıcının sorgusuyla \
ilgili olduğunu açıkla. Hukuki yorum yapma, sadece içerik ile sorgu \
arasındaki ilişkiyi belirt.

KULLANICI SORGUSU:
{query}

EN İYİ EŞLEŞEN PARÇA:
{chunk}

AÇIKLAMA:"""

# Matches any XML/HTML-like tag — catches <unused0>, </s>, <think>, …
_TAG_RE = re.compile(r"<.*?>", re.DOTALL)


async def generate_xai_explanation(query: str, matched_chunk: str) -> str:
    """Produce a 1–2 sentence Turkish explanation of why a case was retrieved.

    Args:
        query:          Original user query as typed in the search bar.
        matched_chunk:  Verbatim text of the best-matching chunk produced by
                        Stage 2 (dense rerank) of the hybrid search.

    Returns:
        A short natural-language explanation suitable for direct display in
        the "Neden bu karar getirildi?" panel.  Returns an empty string on
        any failure so search results are never blocked by XAI errors.
    """
    if not query or not matched_chunk:
        return ""

    prompt = _USER_TEMPLATE.format(query=query.strip(), chunk=matched_chunk.strip())

    try:
        completion = await client.chat.completions.create(
            model="meta-llama/llama-3.2-3b-instruct",
            messages=[
                {"role": "system", "content": _SYSTEM_MESSAGE},
                {"role": "user", "content": prompt},
            ],
            temperature=0.1,
            max_tokens=500,
            extra_headers={
                "HTTP-Referer": "http://localhost:5173",
                "X-OpenRouter-Title": "Hukuki Asistan",
            },
        )
        raw: str = completion.choices[0].message.content.strip()
        return _TAG_RE.sub("", raw).strip()

    except Exception as exc:  # noqa: BLE001
        logger.exception("LLM XAI call failed: %s", exc)
        return ""
