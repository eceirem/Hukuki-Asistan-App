# ⚖️ Hukukî Asistan (Legal Assistant AI)

**"Türk Hukukunda Derin Öğrenme Tabanlı Gerekçeli Emsal Karar Tespiti ve Özetleme Sistemi"**

Hukukî Asistan, hukuk profesyonellerinin emsal karar arama süreçlerini hızlandırmak amacıyla, geleneksel anahtar kelime eşleşmesi yerine **"Retrieve & Re-rank"** (Getir ve Yeniden Sırala) prensibine dayalı hibrit bir derin öğrenme mimarisi sunan modern bir legal-tech platformudur.

---

## 🚀 Proje Hakkında
Geleneksel hukuk bilgi sistemleri, kelimelerin morfolojik varyasyonlarını bağlamsal olarak yakalamakta yetersiz kalmaktadır. Bu proje, **Sosyal Medya Hukuku** alanına odaklanarak 1000 adet nitelikli mahkeme kararını anlamlı segmentlere (Olay, Gerekçe, Hüküm) ayırır ve kullanıcı sorgularıyla en doğru emsali milisaniyeler içinde eşleştirir.

### Temel Özellikler
*   🔍 **Semantik Emsal Arama:** BM25L ve vektör tabanlı FAISS kütüphanesini birleştiren hibrit erişim mimarisi.
*   📄 **Vision LLM Veri İşleme:** Taranmış PDF belgelerini Amazon Nova-2-Lite teknolojisi ile yapılandırılmış JSON formatına dönüştürme.
*   🧠 **Deep Learning Modelleri:** BERTurk-Legal ve XLM-R modellerinin **LoRA** (Low-Rank Adaptation) tekniği ile alan adaptasyonu.
*   ✨ **Modern UI/UX:** Tailwind v4 ile geliştirilmiş, kullanıcı odaklı ve yüksek performanslı arayüz.

---

## 🏗️ Teknik Mimari ve Veri Hattı
Sistem, uçtan uca bir veri işleme hattı (Pipeline) üzerinden çalışır:
*   **Dönüşüm (Transformation):** PDF belgeleri Vision LLM ile temiz metne çevrilir ve "Vaka, Hukuki Gerekçe, Hüküm" hiyerarşisinde segmente edilir.
*   **Vektörleştirme (Vectorization):** Metin parçaları BERT tabanlı bi-encoder modelleriyle yüksek boyutlu vektörlere dönüştürülür.
*   **İndeksleme (Indexing):** Vektörler, hızlı benzerlik araması (Similarity Search) için **FAISS** veritabanında indekslenir.
*   **Erişim (Retrieval):** Kullanıcı sorgusu önce BM25L ile filtrelenir, ardından eğitilmiş modellerle yeniden sıralanarak (Re-rank) en iyi sonuçlar sunulur.

---

## 🎨 Arayüz Tasarımı (UI/UX)
Sistem, hukuk profesyonellerinin çalışma alışkanlıkları ve odaklanma ihtiyaçları gözetilerek tasarlanmıştır:
*   **Minimalist Tasarım:** Karmaşıklıktan uzak, sade ve bilgi odaklı bir görsel dil benimsenmiştir.
*   **Bütünsel Deneyim:** Gece (Dark) ve gündüz (Light) kullanımına uygun, göz yormayan dinamik tema seçenekleri sunulmaktadır.
*   **Erişilebilirlik:** Modern web standartlarında, tüm cihazlarda kesintisiz çalışan duyarlı (responsive) bir yapı kurgulanmıştır.

---

## 🛠️ Kurulum ve Çalıştırma

Uygulama Frontend (Vue.js) ve Backend (Flask) olmak üzere iki ana bileşenden oluşmaktadır.

### 1. Frontend (Vue.js)
Geliştirme sunucusunu başlatmak için:
```bash
cd frontend
```
```bash
npm install
```
```bash
npm run dev
```
### 2. Backend (Flask)
API servisini ve arama motorunu çalıştırmak için:
```bash
cd backend
```
```bash
pip install -r requirements.txt
```
```bash
python app.py
```
## 👥 Ekip ve Danışman
### Geliştiriciler: Ece İrem Şişer & Derda Sina Günay

### Danışman: Prof. Dr. Refik Samet

### Kurum: Ankara Üniversitesi Mühendislik Fakültesi, Bilgisayar Mühendisliği Bölümü

---
*Bu proje, Ankara Üniversitesi Bilgisayar Mühendisliği Bölümü BLM 4061-I/II Proje dersi kapsamında geliştirilmektedir.*
