from collections import defaultdict, deque
import heapq
from typing import Dict, List, Set, Tuple, Optional
import matplotlib.pyplot as plt
from IPython.display import display, Image
import networkx as nx


class Istasyon:
    def __init__(self, idx: str, ad: str, hat: str):
        self.idx = idx
        self.ad = ad
        self.hat = hat
        self.komsular: List[Tuple['Istasyon', int]] = []  # (istasyon, süre) tuple'ları

    def komsu_ekle(self, istasyon: 'Istasyon', sure: int):
        self.komsular.append((istasyon, sure))

class MetroAgi:
    def __init__(self):
        self.istasyonlar: Dict[str, Istasyon] = {}
        self.hatlar: Dict[str, List[Istasyon]] = defaultdict(list)

    def istasyon_ekle(self, idx: str, ad: str, hat: str) -> None:
        if id not in self.istasyonlar:
            istasyon = Istasyon(idx, ad, hat)
            self.istasyonlar[idx] = istasyon
            self.hatlar[hat].append(istasyon)

    def baglanti_ekle(self, istasyon1_id: str, istasyon2_id: str, sure: int) -> None:
        istasyon1 = self.istasyonlar[istasyon1_id]
        istasyon2 = self.istasyonlar[istasyon2_id]
        istasyon1.komsu_ekle(istasyon2, sure)
        istasyon2.komsu_ekle(istasyon1, sure)

    def en_az_aktarma_bul(self, baslangic_id: str, hedef_id: str) -> Optional[List[Istasyon]]:
        # Başlangıç ve hedef istasyonların varlığını kontrol etme
        if baslangic_id not in self.istasyonlar or hedef_id not in self.istasyonlar:
            return None
       
        baslangic = self.istasyonlar[baslangic_id]
        hedef = self.istasyonlar[hedef_id]
        ziyaret_edildi = set()

        kuyruk = deque([(baslangic, [baslangic])])

        while kuyruk:
            mevcut, yol= kuyruk.popleft()

            if mevcut == hedef: # Anlık istasyon ile hedef koşulu
                return yol
         
            if mevcut not in ziyaret_edildi: # ziyaret_edildi içinde mevcut yok ise mevcut ekleme
                ziyaret_edildi.add(mevcut)

                for komsu, _ in mevcut.komsular:
                    if komsu not in ziyaret_edildi:
                        kuyruk.append((komsu, yol + [komsu]))
                    
        return None
   
    def en_hizli_rota_bul(self, baslangic_id: str, hedef_id: str) -> Optional[Tuple[List[Istasyon], int]]:
        # Başlangıç ve hedef istasyonların varlığını kontrol etme
        if baslangic_id not in self.istasyonlar or hedef_id not in self.istasyonlar:
            return None
        
        baslangic = self.istasyonlar[baslangic_id]
        hedef = self.istasyonlar[hedef_id]
        
        # Öncelikli kuyruk (Heap)
        pq = [(0, id(baslangic), baslangic, [baslangic])]
        ziyaret_edildi = {}
        # While döngüsü
        while pq:
            gecen_sure, _, mevcut, yol = heapq.heappop(pq)

            if mevcut == baslangic and not yol:
                yol = [baslangic]

            if mevcut in ziyaret_edildi and ziyaret_edildi[mevcut] <= gecen_sure:
                continue

            ziyaret_edildi[mevcut] = gecen_sure  # Şu anki istasyona ulaşma süresini kaydet

            if mevcut == hedef: # Anlık istasyon ile hedef koşulu
                return (yol, gecen_sure)

            # Komşuları ekleyerek aramayı genişlet
            for komsu, sure in mevcut.komsular:
                if komsu not in ziyaret_edildi or ziyaret_edildi[komsu] > gecen_sure + sure:
                    heapq.heappush(pq, (gecen_sure + sure, id(komsu), komsu, yol + [komsu]))
                    
        return None
        
    # Metro Ağı Graf modelleme fonksiyonu
    def graf_modelleme(self):
        G = nx.Graph()
        for istasyon_id, istasyon in self.istasyonlar.items():
            G.add_node(istasyon_id, label=istasyon.ad)
            for komsu, _ in istasyon.komsular:
                G.add_edge(istasyon_id, komsu.idx, hat=istasyon.hat)
        return G

# Örnek Kullanım
if __name__ == "__main__":
    metro = MetroAgi()
    
    # İstasyonlar ekleme
    # Kırmızı Hat
    metro.istasyon_ekle("K1", "Kızılay", "Kırmızı Hat")
    metro.istasyon_ekle("K2", "Ulus", "Kırmızı Hat")
    metro.istasyon_ekle("K3", "Demetevler", "Kırmızı Hat")
    metro.istasyon_ekle("K4", "OSB", "Kırmızı Hat")
    
    # Mavi Hat
    metro.istasyon_ekle("M1", "AŞTİ", "Mavi Hat")
    metro.istasyon_ekle("M2", "Kızılay", "Mavi Hat")  # Aktarma noktası
    metro.istasyon_ekle("M3", "Sıhhiye", "Mavi Hat")
    metro.istasyon_ekle("M4", "Gar", "Mavi Hat")
    
    # Turuncu Hat
    metro.istasyon_ekle("T1", "Batıkent", "Turuncu Hat")
    metro.istasyon_ekle("T2", "Demetevler", "Turuncu Hat")  # Aktarma noktası
    metro.istasyon_ekle("T3", "Gar", "Turuncu Hat")  # Aktarma noktası
    metro.istasyon_ekle("T4", "Keçiören", "Turuncu Hat")
    
    # Bağlantılar ekleme
    # Kırmızı Hat bağlantıları
    metro.baglanti_ekle("K1", "K2", 4)  # Kızılay -> Ulus
    metro.baglanti_ekle("K2", "K3", 6)  # Ulus -> Demetevler
    metro.baglanti_ekle("K3", "K4", 8)  # Demetevler -> OSB
    
    # Mavi Hat bağlantıları
    metro.baglanti_ekle("M1", "M2", 5)  # AŞTİ -> Kızılay
    metro.baglanti_ekle("M2", "M3", 3)  # Kızılay -> Sıhhiye
    metro.baglanti_ekle("M3", "M4", 4)  # Sıhhiye -> Gar
    
    # Turuncu Hat bağlantıları
    metro.baglanti_ekle("T1", "T2", 7)  # Batıkent -> Demetevler
    metro.baglanti_ekle("T2", "T3", 9)  # Demetevler -> Gar
    metro.baglanti_ekle("T3", "T4", 5)  # Gar -> Keçiören
    
    # Hat aktarma bağlantıları (aynı istasyon farklı hatlar)
    metro.baglanti_ekle("K1", "M2", 2)  # Kızılay aktarma
    metro.baglanti_ekle("K3", "T2", 3)  # Demetevler aktarma
    metro.baglanti_ekle("M4", "T3", 2)  # Gar aktarma

    # Metro Ağı Graf modelleme
    # Renkleri hatlara tanımlama
    hat_renkleri = {
        "Kırmızı Hat": "red",
        "Mavi Hat": "blue",
        "Turuncu Hat": "orange"
    }
    def graf_modelleme(metro_ag, start, end, path=[]):
        path = path + [start] 
        if start == end: 
            return [path] 
        paths = [] 
        for komsu, _ in start.komsular: 
            if komsu not in path: 
                newpaths = graf_modelleme(metro_ag, komsu, end, path) 
                for newpath in newpaths: 
                    paths.append(newpath) 
        return paths 

    G = metro.graf_modelleme()

    plt.figure(figsize=(12, 10))
    pos = nx.spring_layout(G)

    # Kenar renklendirme
    edge_colors = []
    for u, v, data in G.edges(data=True):
        hat = data['hat']
        color = hat_renkleri.get(hat, 'black')  # Hat rengi
        edge_colors.append(color)

    nx.draw_networkx_nodes(G, pos, node_size=2000, node_color="lightblue")
    nx.draw_networkx_edges(G, pos, width=2, edge_color=edge_colors)

    nx.draw_networkx_labels(G, pos, font_size=12, font_color='black', font_weight="bold")

    plt.title("Metro Ağı Graf Modeli")
    plt.axis('off')  # Eksen kaldırma
    plt.show()

    # Test senaryoları
    print("\n=== Test Senaryoları ===")
    
    # Senaryo 1: AŞTİ'den OSB'ye
    print("\n1. AŞTİ'den OSB'ye:")
    rota = metro.en_az_aktarma_bul("M1", "K4")
    if rota:
        print("En az aktarmalı rota:", " -> ".join(i.ad for i in rota))
    
    sonuc = metro.en_hizli_rota_bul("M1", "K4")
    if sonuc:
        rota, sure = sonuc
        print(f"En hızlı rota ({sure} dakika):", " -> ".join(i.ad for i in rota))
    
    # Senaryo 2: Batıkent'ten Keçiören'e
    print("\n2. Batıkent'ten Keçiören'e:")
    rota = metro.en_az_aktarma_bul("T1", "T4")
    if rota:
        print("En az aktarmalı rota:", " -> ".join(i.ad for i in rota))
    
    sonuc = metro.en_hizli_rota_bul("T1", "T4")
    if sonuc:
        rota, sure = sonuc
        print(f"En hızlı rota ({sure} dakika):", " -> ".join(i.ad for i in rota))
    
    # Senaryo 3: Keçiören'den AŞTİ'ye
    print("\n3. Keçiören'den AŞTİ'ye:")
    rota = metro.en_az_aktarma_bul("T4", "M1")
    if rota:
        print("En az aktarmalı rota:", " -> ".join(i.ad for i in rota))
    
    sonuc = metro.en_hizli_rota_bul("T4", "M1")
    if sonuc:
        rota, sure = sonuc
        print(f"En hızlı rota ({sure} dakika):", " -> ".join(i.ad for i in rota)) 

    # Senaryo 4: Batıkent'ten Kızılay'a
    print("\n4. Batıkent'ten Kızılay'a:")
    rota = metro.en_az_aktarma_bul("T1","M2")
    if rota:
        print("En az aktarmalı rota:", " -> ".join(i.ad for i in rota))
    
    sonuc = metro.en_hizli_rota_bul("T1","M2")
    if sonuc:
        rota, sure = sonuc
        print(f"En hızlı rota {sure} dakika:", " -> ".join(i.ad for i in rota))
    
    # Senaryo 5: Kızılay'dan Keçiören'e
    print("\n5. Kızılay'dan Keçiören'e:")
    rota = metro.en_az_aktarma_bul("K1","T4")
    if rota:
        print("En az aktarmalı rota:", " -> ".join(i.ad for i in rota))
    
    sonuc = metro.en_hizli_rota_bul("K1","T4")
    if sonuc:
         rota, sure = sonuc
         print(f"En hızlı rota {sure} dakika:", " -> ".join(i.ad for i in rota))

