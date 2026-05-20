"""Explainable-AI (XAI) service — natural-language retrieval explanations.

Gated by ``settings.ENABLE_LLM_XAI``.  When the flag is OFF (the default), the
search pipeline simply surfaces the best-matching chunk text verbatim and this
module is never invoked.  When the flag is ON, the search route awaits
:func:`generate_xai_explanation` once per retrieved case to obtain a
human-readable answer to "Neden bu karar getirildi?".

Provider
────────
Hugging Face ``InferenceClient`` (``huggingface_hub`` SDK).  ``_call_llm`` is a
plain synchronous function; the async public interface dispatches it through
``asyncio.to_thread`` so the FastAPI event loop is never blocked.

Configure in ``.env``:
    HF_TOKEN = hf_...
    ENABLE_LLM_XAI = True
"""

from __future__ import annotations

import asyncio
import logging
import os
import re

from huggingface_hub import InferenceClient

logger = logging.getLogger(__name__)


# No `:fastest` suffix — that suffix triggers a 400 from the HF router.
_MODEL = "ytu-ce-cosmos/Turkish-Gemma-9b-T1"

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


def _call_llm(prompt: str) -> str:
    """Synchronous call to the HF Inference API via ``huggingface_hub``.

    Creates a fresh ``InferenceClient`` per call (lightweight and stateless).
    All errors are caught and logged so the caller always receives a string.
    """
    try:
        client = InferenceClient(api_key=os.environ.get("HF_TOKEN"))
        completion = client.chat.completions.create(
            model=_MODEL,
            messages=[
                {"role": "system", "content": _SYSTEM_MESSAGE},
                {"role": "user", "content": prompt},
            ],
            temperature=0.1,
            max_tokens=500,
        )
        raw = completion.choices[0].message.content.strip()
        # Belt-and-suspenders: strip any leaked thought tags even if the system
        # message succeeded in suppressing most of them.
        return re.sub(r"<.*?>", "", raw).strip()

    except Exception as exc:  # noqa: BLE001
        logger.exception("LLM XAI call failed: %s", exc)
        return ""


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
    return await asyncio.to_thread(_call_llm, prompt)
