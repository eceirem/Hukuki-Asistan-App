const MOCK_CASES = [
  {
    id: '2022_551',
    match_score: 94,
    metadata: {
      court_name: 'İstanbul Bölge Adliye Mahkemesi 16. Hukuk Dairesi',
      esas_no: '2021/1168',
      karar_no: '2024/1919',
      case_subject: 'İhtiyati Tedbir',
    },
    segments: {
      facts_text:
        'İddialar, vekilin müvekkilinin ticari markalarını kullanmak için internet sitelerinde reklam ve tanıtım faaliyetleri yapmasıdır. Davacı taraf, sosyal medya mecralarında sahte hesaplar üzerinden reklam verildiğini ve tüketicinin yanıltıldığını ileri sürmüştür.',
      reasoning_text:
        'Mahkeme, HMK 389 ve 390 maddeleri çerçevesinde ihtiyati tedbir koşullarını değerlendirmiş; uyuşmazlığın esası hakkında delillerin toplanmasının gerekli olduğu, telafisi güç zarar iddiasının somutlaştırılamadığı gerekçesiyle tedbir taleplerini reddetmiştir.',
      verdict_text:
        'Dair, dosya üzerinde yapılan inceleme sonucu oy birliği ile kesin olarak karar verildi.',
    },
    summary_for_human:
      'Mahkeme, istinaf ve ihtiyati tedbir taleplerini HMK 389-390 kapsamında değerlendirmiş ve somut koşulların oluşmadığı gerekçesiyle reddetmiştir.',
    xai_explanation:
      "Sorgunuzdaki haksız rekabet ve reklam iddiaları, kararın gerekçe bölümündeki 'ticari marka/yanıltıcı tanıtım' bağlamıyla %94 oranında anlamsal eşleşme sağlamıştır.",
  },
  {
    id: '2023_1042',
    match_score: 91,
    metadata: {
      court_name: 'İstanbul Anadolu 3. Fikri ve Sınai Haklar Hukuk Mahkemesi',
      esas_no: '2023/412',
      karar_no: '2024/88',
      case_subject: 'Marka Taklidi',
    },
    segments: {
      facts_text:
        'Davacı, sosyal medya reklamlarında kullanılan logonun kendi tescilli markasının ayırt edici unsurlarını taşıdığını, tüketicinin işletmeler arasında bağlantı kurduğunu iddia etmiştir.',
      reasoning_text:
        'Mahkeme, markasal kullanım, karıştırılma ihtimali ve haksız yararlanma kriterlerini değerlendirmiş; reklamlardaki işaretin markanın asli unsurunu çağrıştırdığı ve iltibas riskini artırdığı sonucuna varmıştır.',
      verdict_text:
        'Davalının ilgili paylaşımları durdurmasına, ihlale konu içeriklerin kaldırılmasına ve tazminata hükmedilmiştir.',
    },
    summary_for_human:
      'Sosyal medya reklamlarında logo/işaret kullanımı nedeniyle karıştırılma ihtimali bulunduğu kabul edilmiş; ihlalin durdurulması ve tazminat kararı verilmiştir.',
    xai_explanation:
      "Sorgunuzdaki 'logo kopyalanması' ifadesi, kararda tartışılan 'markanın ayırt edici unsurlarının taklidi' değerlendirmesiyle yüksek benzerlik göstermiştir.",
  },
  {
    id: '2021_778',
    match_score: 88,
    metadata: {
      court_name: 'Yargıtay 11. Hukuk Dairesi',
      esas_no: '2020/2190',
      karar_no: '2021/778',
      case_subject: 'Haksız Rekabet',
    },
    segments: {
      facts_text:
        'Taraflar aynı sektörde faaliyet göstermekte olup davalı, sosyal medya üzerinden karşılaştırmalı ve yanıltıcı reklam yayınlamakla suçlanmıştır.',
      reasoning_text:
        'Daire, TTK haksız rekabet hükümleri kapsamında reklamın dürüstlük kuralına aykırılık ölçütlerini değerlendirmiş; ispat yükü ve somutlaştırma bakımından ilk derece kararının gerekçesini yeterli bulmuştur.',
      verdict_text:
        'Temyiz itirazlarının reddi ile hükmün onanmasına karar verilmiştir.',
    },
    summary_for_human:
      'Yanıltıcı/karşılaştırmalı reklamın dürüstlük kuralına aykırı olduğu kabul edilerek haksız rekabet tespiti yönünden hüküm onanmıştır.',
    xai_explanation:
      "Sorgunuzdaki 'haksız rekabet' anahtar kavramı, karardaki TTK değerlendirmesiyle doğrudan örtüşmüş ve semantik skor yükselmiştir.",
  },
  {
    id: '2024_312',
    match_score: 86,
    metadata: {
      court_name: 'Ankara 5. Sulh Ceza Hakimliği',
      esas_no: '2024/312',
      karar_no: '2024/312',
      case_subject: 'Erişimin Engellenmesi',
    },
    segments: {
      facts_text:
        'Başvurucu, sosyal medya platformunda kişilik haklarına saldırı teşkil eden paylaşımlar nedeniyle URL bazında erişimin engellenmesini talep etmiştir.',
      reasoning_text:
        'Hakimlik, 5651 sayılı Kanun kapsamında URL bazlı tedbirin ölçülülük ve gereklilik kriterlerini incelemiş; içeriklerin kişilik haklarına açık saldırı oluşturduğu değerlendirmesiyle erişimin engellenmesine hükmetmiştir.',
      verdict_text:
        'Belirtilen URL’lere erişimin engellenmesine karar verilmiştir.',
    },
    summary_for_human:
      'Kişilik haklarına açık saldırı içeren paylaşımlar için 5651 kapsamında URL bazlı erişim engeli kararı verilmiştir.',
    xai_explanation:
      "Sorgunuzdaki 'erişimin engellenmesi' talebi, kararın 5651/URL bazlı tedbir değerlendirmesiyle yüksek anlamsal yakınlık göstermiştir.",
  },
  {
    id: '2022_219',
    match_score: 84,
    metadata: {
      court_name: 'İstanbul 12. Asliye Hukuk Mahkemesi',
      esas_no: '2021/902',
      karar_no: '2022/219',
      case_subject: 'Kişilik Haklarına Saldırı',
    },
    segments: {
      facts_text:
        'Davacı, sosyal medya paylaşımında kendisine yönelik küçük düşürücü ifadeler kullanıldığını, iş çevresinde itibar kaybı yaşadığını iddia etmiştir.',
      reasoning_text:
        'Mahkeme, ifade özgürlüğü ile kişilik haklarının dengelenmesi kapsamında; paylaşımın kamu yararı taşımadığı ve kişiyi hedef aldığı kanaatiyle manevi tazminat koşullarının oluştuğunu kabul etmiştir.',
      verdict_text:
        'Manevi tazminata ve ilgili içeriğin kaldırılmasına karar verilmiştir.',
    },
    summary_for_human:
      'İfade özgürlüğü-k kişilik hakkı dengesi kurularak; hedef gösteren paylaşım nedeniyle manevi tazminata hükmedilmiştir.',
    xai_explanation:
      "Sorgunuzdaki 'kişilik haklarına saldırı' ifadesi, kararın dengeleme analizinde ana eksen olduğundan semantik eşleşmeyi güçlendirmiştir.",
  },
  {
    id: '2020_145',
    match_score: 82,
    metadata: {
      court_name: 'İstanbul 25. Asliye Ceza Mahkemesi',
      esas_no: '2019/640',
      karar_no: '2020/145',
      case_subject: 'Hakaret ve İftira',
    },
    segments: {
      facts_text:
        'Sanık, sosyal medya üzerinden müştekiye yönelik “dolandırıcı” gibi ithamlar içeren mesajlar paylaşmıştır.',
      reasoning_text:
        'Mahkeme, sözlerin somut isnat niteliği taşıdığı, aleniyet unsurunun sosyal medya paylaşımı ile gerçekleştiği ve ifadelerin eleştiri sınırlarını aştığı gerekçesiyle mahkumiyet kararı vermiştir.',
      verdict_text:
        'Sanığın mahkumiyetine karar verilmiştir.',
    },
    summary_for_human:
      'Sosyal medya paylaşımıyla aleniyet oluştuğu kabul edilerek, eleştiri sınırlarını aşan ifadeler nedeniyle mahkumiyet kararı verilmiştir.',
    xai_explanation:
      "Sorgunuzdaki 'hakaret/iftira' teması, kararda tartışılan aleniyet ve eleştiri sınırları analizine semantik olarak yakın bulunmuştur.",
  },
  {
    id: '2024_67',
    match_score: 79,
    metadata: {
      court_name: 'İzmir 2. Fikri ve Sınai Haklar Hukuk Mahkemesi',
      esas_no: '2024/67',
      karar_no: '2024/112',
      case_subject: 'Telif Hakkı İhlali',
    },
    segments: {
      facts_text:
        'Davacı, sosyal medya hesabında paylaştığı fotoğrafın izinsiz olarak başka bir sayfa tarafından yeniden yayımlandığını ileri sürmüştür.',
      reasoning_text:
        'Mahkeme, eser niteliği, hak sahipliği ve izinsiz kullanım unsurlarını değerlendirmiş; ekran görüntüsü ve platform kayıtlarıyla ihlalin ispatlandığı kanaatine varmıştır.',
      verdict_text:
        'İhlalin tespitine ve maddi/manevi tazminata karar verilmiştir.',
    },
    summary_for_human:
      'Sosyal medya içeriğinin izinsiz yeniden paylaşımı telif ihlali sayılmış; tespit ve tazminata hükmedilmiştir.',
    xai_explanation:
      "Sorgunuzdaki 'telif hakkı ihlali' ifadesi, kararda yer alan izinsiz yeniden yayım değerlendirmesiyle anlamca örtüşmüştür.",
  },
]

function sleep(ms) {
  return new Promise((r) => setTimeout(r, ms))
}

/**
 * @param {{ query: string, k: number | 'all' }} params
 */
export async function mockSearchCases(params) {
  const query = (params?.query ?? '').trim().toLowerCase()
  const k = params?.k ?? 7

  await sleep(450)

  const filtered = MOCK_CASES.filter((c) => {
    if (!query) return true
    const haystack = [
      c.metadata.court_name,
      c.metadata.esas_no,
      c.metadata.karar_no,
      c.metadata.case_subject,
      c.summary_for_human,
      c.segments.facts_text,
      c.segments.reasoning_text,
      c.segments.verdict_text,
    ]
      .join(' ')
      .toLowerCase()

    return haystack.includes(query)
  })

  const sorted = [...filtered].sort((a, b) => b.match_score - a.match_score)

  if (k === 'all') return sorted
  return sorted.slice(0, Math.max(0, Number(k) || 0))
}

export { MOCK_CASES }

