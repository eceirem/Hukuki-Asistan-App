# Hukuki Asistan Uygulaması (Hukuki-Asistan-App) ⚖️

**"Türk Hukukunda Derin Öğrenme Tabanlı Gerekçeli Emsal Karar Tespiti ve Özetleme Sistemi — Arayüz ve Servis Katmanı"**

![Conference](https://img.shields.io/badge/Conference-ITTA%202026%20%28Strong%20Accept%29-blue)
![Award](https://img.shields.io/badge/Award-Bili%C5%9Fim%20Vadisi%201st%20Place-orange)
![Workshop](https://img.shields.io/badge/Workshop-TBB%20Compliant-purple)
![License](https://img.shields.io/badge/License-MIT-yellow)
![Vue.js](https://img.shields.io/badge/Frontend-Vue.js%203-green)
![Python](https://img.shields.io/badge/Python-3.12-blue)
![Flask](https://img.shields.io/badge/Backend-Flask-lightgrey)
![Tailwind](https://img.shields.io/badge/UI-Tailwind%20v4-blueviolet)

---

Bu repo, **Ankara Üniversitesi Mühendislik Fakültesi Bilgisayar Mühendisliği Bölümü** son sınıf mezuniyet projesi (BLM 4061-A / BLM 4062 Bilgisayar Mühendisliği Tasarımı) kapsamında geliştirilen **Hukuki Asistan** ekosisteminin kullanıcı arayüzü (Vue.js Frontend) ve API servis (Flask Backend) katmanlarını barındıran ana uygulama reposudur. Modelle ilgili diğer bağlantılar [Ekosistem Bağlantıları ve Navigasyon](#ekosistem-bağlantıları-ve-navigasyon) kısmında belirtilmiştir.

Sistem, hukuk profesyonellerinin emsal karar arama süreçlerini hızlandırmak amacıyla, geleneksel anahtar kelime eşleşmesi yerine **"Retrieve & Re-rank"** (Getir ve Yeniden Sırala) prensibine dayalı hibrit bir derin öğrenme mimarisini canlı bir web platformu olarak sunmaktadır.

---

## 🔗 Ekosistem Bağlantıları ve Navigasyon

Hukuki Asistan ekosistemini oluşturan diğer tüm modüllere, model ağırlıklarına ve derin ar-ge kodlarına aşağıdaki kurumsal bağlantılar üzerinden erişebilirsiniz:

* 🧠 **Hukuki Asistan Çekirdek Model & Kod Reposu (Adım 1-5 Not Defterleri):** [`Hukuki-Asistan Core ML`](https://github.com/eceiremsiser/Hukuki-Asistan)
* 🤗 **Hugging Face Model Hub (Fine-Tune Edilmiş Şampiyon Ağırlıklar):** [`EceIremSiser/berturk-legal-chunk-retriever`](https://huggingface.co/EceIremSiser/berturk-legal-chunk-retriever)
* 📊 **Akademik Proje Sunum Dosyası (PDF):** [`presentation/Hukuki_Asistan_Final_Presentation.pdf`](./presentation/Hukuki_Asistan_Final_Presentation.pdf)

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

#### Geliştiriciler: 
* Ece İrem Şişer & Derda Sina Günay

#### Danışman: 
* Prof. Dr. Refik Samet

#### Kurum: 
* Ankara Üniversitesi Mühendislik Fakültesi, Bilgisayar Mühendisliği Bölümü

---
*Bu proje, Ankara Üniversitesi Bilgisayar Mühendisliği Bölümü BLM 4061-I/II Proje dersi kapsamında geliştirilmektedir.*
