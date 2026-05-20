"""Seed script — populates the `cases` table with realistic Turkish legal cases.

Run with:
    uv run python -m app.db.seed

Behaviour:
  - Calls init_db() first to guarantee tables and the FTS trigger exist.
  - Skips seeding if any cases are already present (idempotent).
  - Generates 768-dim BERT embeddings for `olay_vect` and `gerekce_vect`
    via asyncio.to_thread so the event loop is not blocked.
"""

from __future__ import annotations

import asyncio
import logging
from datetime import date

from sqlalchemy import func, select

from app.db.database import AsyncSessionLocal
from app.db.init import init_db
from app.models.case import Case
from app.services.nlp_service import NLPService

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-7s  %(name)s — %(message)s",
)
logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Raw case data
# ---------------------------------------------------------------------------

_SEED_DATA: list[dict] = [
    {
        "esas_no": "2023/1547",
        "karar_no": "2023/3892",
        "mahkeme": "Yargıtay 9. Hukuk Dairesi",
        "dava_konusu": "İşçi alacakları — kıdem ve ihbar tazminatı",
        "dava_tarihi": date(2023, 3, 12),
        "karar_tarihi": date(2023, 9, 4),
        "olay": (
            "Davacı işçi, davalı şirkette 11 yıl boyunca tekstil operatörü olarak "
            "çalışmıştır. İş akdi, işveren tarafından ekonomik nedenler gerekçesiyle "
            "ihbar öneli tanınmadan feshedilmiştir. Davacı kıdem tazminatı, ihbar "
            "tazminatı ve birikmiş fazla mesai alacaklarının ödenmediğini ileri sürerek "
            "dava açmıştır."
        ),
        "gerekce": (
            "4857 sayılı İş Kanunu'nun 17. maddesi uyarınca iş sözleşmesinin işveren "
            "tarafından feshedilmesi durumunda ihbar öneline uyulması zorunludur. "
            "Davacının 11 yıllık kıdemi dikkate alındığında sekiz haftalık ihbar öneli "
            "hakkı doğmaktadır. Kıdem tazminatı hesabında son brüt ücret esas alınmalı; "
            "her tam çalışma yılı için otuz günlük ücret tutarında ödeme yapılmalıdır. "
            "Fazla mesai alacaklarının ispat yükü işçide olup, tanık beyanları ve "
            "bordro kayıtlarıyla desteklenmesi gerekmektedir."
        ),
        "karar": (
            "Mahkemece davanın kabulüne karar verilmiş; kıdem tazminatı 148.500 TL, "
            "ihbar tazminatı 27.000 TL ve fazla mesai alacağı 12.300 TL olarak "
            "hesaplanmıştır. Hüküm, Yargıtay 9. Hukuk Dairesi tarafından onanmıştır."
        ),
        "sum_human": (
            "11 yıllık işçinin iş akdinin geçersiz feshinde kıdem ve ihbar tazminatına "
            "hükmedilmiştir."
        ),
    },
    {
        "esas_no": "2022/8814",
        "karar_no": "2023/1203",
        "mahkeme": "İstanbul Bölge Adliye Mahkemesi 17. Hukuk Dairesi",
        "dava_konusu": "Tüketici hukuku — ayıplı araç iadesi ve bedel iadesi",
        "dava_tarihi": date(2022, 11, 22),
        "karar_tarihi": date(2023, 4, 17),
        "olay": (
            "Davacı tüketici, sıfır kilometre olarak satın aldığı otomobilin teslim "
            "gününden itibaren vites kutusu ve diferansiyel sisteminde tekrarlayan "
            "arızalar yaşandığını bildirmiştir. Yetkili servis tarafından dört kez "
            "onarım yapılmış; ancak arızalar giderilememitir. Davacı, 6502 sayılı "
            "Tüketicinin Korunması Hakkında Kanun kapsamında aracın iadesi ve "
            "ödediği bedelin faiziyle birlikte iadesini talep etmiştir."
        ),
        "gerekce": (
            "6502 sayılı TKHK'nın 11. maddesi, tüketiciye malın ayıplı çıkması "
            "halinde sözleşmeden dönme, bedel indirimi veya ücretsiz onarım seçim "
            "haklarını tanımaktadır. Aynı arızanın yetkili serviste dört kez onarıma "
            "konu olması ve giderilememiş olması, kanunda öngörülen 'önemli ayıp' "
            "kriterini karşılamaktadır. Bu koşulların oluşması halinde tüketici "
            "sözleşmeden dönebilir ve ödediği bedelin tamamının iadesini talep "
            "edebilir. Satıcı ve üretici bu talebe karşı müteselsil sorumludur."
        ),
        "karar": (
            "Tüketici hakem heyeti kararının iptali istemiyle açılan dava reddedilmiş; "
            "araç bedeli 485.000 TL, yasal faiziyle birlikte davalı satıcıya rücuen "
            "iade hükmü kurulmuştur. İstinaf talebinin reddine karar verilmiştir."
        ),
        "sum_human": (
            "Dört kez servise giren sıfır araçta önemli ayıp tespit edilmiş; "
            "tüketicinin sözleşmeden dönme hakkı doğrultusunda bedel iadesi yapılmıştır."
        ),
    },
    {
        "esas_no": "2023/4421",
        "karar_no": "2023/7756",
        "mahkeme": "Ankara 3. Asliye Hukuk Mahkemesi",
        "dava_konusu": "Trafik kazası — maddi ve manevi tazminat",
        "dava_tarihi": date(2023, 1, 9),
        "karar_tarihi": date(2023, 10, 30),
        "olay": (
            "Davalı, kırmızı ışık ihlali yaparak kavşağa girmiş ve seyir halindeki "
            "davacının aracına çarpmıştır. Kazada davacı sürücü omurga kırığı geçirmiş "
            "ve üç ay iş göremez hale gelmiştir. Trafik sigortası şirketi zorunlu "
            "trafik sigortası limitini ödemekle birlikte, bu miktar gerçek zararın çok "
            "altında kalmıştır. Davacı, aşkın zarar ile çektiği acı ve ıstırap için "
            "maddi ve manevi tazminat talep etmiştir."
        ),
        "gerekce": (
            "2918 sayılı Karayolları Trafik Kanunu'nun 85. maddesi uyarınca motorlu "
            "araç işleteninin kaza sonucu doğan zararlardan kusur aranmaksızın sorumlu "
            "olduğu ilkesi geçerlidir. Kaza tespit tutanağı ve güvenlik kamerası "
            "kayıtlarıyla kusur oranı %100 davalıya yüklenmiştir. Bedensel zarar "
            "tazminatının hesabında aktüer bilirkişi raporu esas alınmalıdır. Manevi "
            "tazminat takdirinde kazanın ağırlığı, mağdurun yaşı ve maruz kaldığı "
            "acının yoğunluğu gözetilmelidir."
        ),
        "karar": (
            "Davacı lehine 95.000 TL maddi tazminat ve 40.000 TL manevi tazminata "
            "hükmedilmiştir. Sigorta şirketinin ödediği limit bedeli bu miktardan "
            "mahsup edilmiştir. Fazlaya ilişkin talep reddedilmiştir."
        ),
        "sum_human": (
            "Kırmızı ışık ihlali sonucu yaralanan davacıya maddi ve manevi tazminat "
            "hükmedilmiş; davalının tam kusurlu olduğu saptanmıştır."
        ),
    },
]


# ---------------------------------------------------------------------------
# Seeding logic
# ---------------------------------------------------------------------------

async def seed() -> None:
    await init_db()

    nlp = NLPService()

    async with AsyncSessionLocal() as session:
        existing_count = await session.scalar(select(func.count()).select_from(Case))
        if existing_count and existing_count > 0:
            logger.info("Database already contains %d case(s) — skipping seed.", existing_count)
            return

        logger.info("Generating embeddings and inserting %d seed cases …", len(_SEED_DATA))

        cases: list[Case] = []
        for data in _SEED_DATA:
            olay_vect    = await nlp.aembed(data["olay"])
            gerekce_vect = await nlp.aembed(data["gerekce"])

            cases.append(
                Case(
                    esas_no=data["esas_no"],
                    karar_no=data["karar_no"],
                    mahkeme=data["mahkeme"],
                    dava_konusu=data["dava_konusu"],
                    dava_tarihi=data["dava_tarihi"],
                    karar_tarihi=data["karar_tarihi"],
                    olay=data["olay"],
                    gerekce=data["gerekce"],
                    karar=data["karar"],
                    sum_human=data.get("sum_human"),
                    olay_vect=olay_vect,
                    gerekce_vect=gerekce_vect,
                )
            )

        session.add_all(cases)
        await session.commit()

    logger.info("✓ Seeded %d legal cases successfully.", len(cases))


if __name__ == "__main__":
    asyncio.run(seed())
