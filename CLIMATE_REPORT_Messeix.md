# Rapport Climatique de Messeix (Puy-de-Dôme, Massif Central, France)

**Rapport de renseignement climatique et plan d'adaptation agricole — Messeix (63)**

Date de production : octobre 2026 · Analyse fondée sur ERA5 (via Open-Meteo) et les stations Météo-France.

---

## 1. Résumé exécutif

Messeix, commune du haut plateau du Massif Central (~45,62° N, 2,54° E, ~800 m
d'altitude), connaît un climat océanique à variante montagnarde : hivers froids,
gelées fréquentes et abondantes, neige hivernale significative, étés courts mais
chauds.

Les données observées (ERA5, 1940–2026, ~87 ans) montrent un **réchauffement net,
robuste et statistiquement significatif** :

- **Température moyenne annuelle : +0,22 °C/décennie** (p ≈ 8×10⁻⁹), soit environ
  **+1,9 °C depuis 1940**. La hausse des minimales (+0,24 °C/déc) et des maximales
  (+0,23 °C/déc) est comparable.
- Le réchauffement est le plus marqué en **hiver (DJF : +0,35 °C/déc)** puis en
  **été (JJA : +0,25 °C/déc)**.
- Les **précipitations annuelles augmentent** modestement (+23 mm/déc, p ≈ 0,01),
  mais avec une forte variabilité interannuelle ; les changements saisonniers de
  précipitations ne sont pas robustes statistiquement (seuls MAM et SON le sont
  marginalement).
- **Anomalies décennales** par rapport à la normale 1961–1990 : +1,17 °C (années
  2010) et **+2,47 °C (années 2020)** — la dernière décennie est de loin la plus
  chaude du jeu de données.

Conséquences agroclimatiques (normale 1991–2020 vs 2016–2025) :

- **Gelées** : ~84 jours/an → **~59 jours/an** (réduction d'environ 25 jours).
- **Jours chauds (Tmax > 30 °C)** : ~1,4 j/an → **~5,8 j/an**.
- **Saison de croissance** (base 5 °C) : ~242 j → **~267 j**.
- **Degrés-jours de croissance (GDD5)** : ~1 753 → **~2 109 °C·j** (+20 %).
- **Indice de Huglin** : ~1 103 → **~1 373** (passage d'un niveau sub-marginal à
  marginal pour la vigne).
- **Indice d'aridité de De Martonne** : ~63 (climat humide, pas de contrainte
  hydrique annuelle majeure).

**Lecture pour l'agriculture** : une saison végétative plus longue et plus chaude
ouvre de nouvelles opportunités (arboriculture, vigne en limite thermique haute,
protéagineux), mais augmente le **risque de gelées tardives** (printemps plus
précoces) et le **stress hydrique estival** (canicules et déficits estivaux plus
fréquents malgré un bilan annuel humide). Le plan d'adaptation (Section 6) répond
à ces deux risques.

> **Séparation des informations** : les données observées (Sections 3–5) proviennent
> d'ERA5 et des stations Météo-France ; les recommandations (Section 6) relèvent du
> jugement d'experts fondé sur ces données. **Aucune donnée de projection climatique
> (scénarios RCP/SSP) n'a pu être récupérée dans cette analyse** (voir Section 7) :
> les projections ne sont donc **pas** chiffrées ici.

---

## 2. Données et méthodes

### 2.1 Localisation et référentiels

| Paramètre | Valeur | Référentiel |
|---|---|---|
| Commune | Messeix (63), Massif Central | — |
| Latitude / longitude (centroïde approx.) | ~45,62° N / 2,54° E | WGS84 (EPSG:4326) |
| Altitude de référence | ~800 m | Station Météo-France 63225001 |
| Grille de réanalyse | cellule ERA5 la plus proche (~0,25°) | EPSG:4326 |
| Projection locale (si besoin carto) | Lambert-93 | EPSG:2154 |

Ces coordonnées et l'altitude sont vérifiées et **codées en dur** dans les métadonnées
du notebook `climate_messeix.ipynb`.

### 2.2 Sources de données

1. **ERA5 (Copernicus, via API Open-Meteo)** — réanalyse atmosphérique, variables
   journalières : T2m (min/max/moy), précipitations, neige, ETP (FAO-56), vent,
   rayonnement. Étendue : **1940–2026** (série longue). Version : API Open-Meteo
   (miroir des champs ERA5). DOI de référence : Hersbach et al. (2023), ERA5.
2. **Météo-France — stations Climatologie (open data)** :
   - **MESSEIX (63225001)**, 45,6167° N, 2,5667° E, **800 m**, distance au centroïde
     **~2,1 km** — la station de référence la plus proche, **représentative** du site.
   - **TAUVES (63426001)**, 45,5447° N, 2,5957° E, **851 m**, ~9,4 km.
   - Normale climatologique utilisée pour la comparaison station : **TAUVES
     1991–2020** (série la plus complète sur la période).

### 2.3 Traitement et indices

- Climatologie mensuelle sur la normale **1991–2020** (ERA5 et station).
- Tendances : **OLS (moindres carrés)** + **Mann-Kendall avec pente de Sen** ;
  rapport des pentes Sen en °C/décennie et mm/décennie, avec **p-values** et
  intervalles de confiance. Seuil de significativité : p < 0,05.
- Anomalies décennales vs normale **1961–1990**.
- Indices agroclimatiques (annuels) : jours de gel (Tmin < 0 °C), jours chauds
  (Tmax > 30/35 °C), jours de fortes pluies (> 20 mm), longueur de saison de
  croissance (seuils 5 °C et 10 °C), **GDD** (base 5 °C et 10 °C), **indice de
  Huglin**, **indice de De Martonne**, **bilan hydrique (P − ETP)**, **SPI/SPEI à
  12 mois**, et **probabilité de gel par période de 10 jours** (risque de gelées
  tardives/précoces).

Toutes les valeurs chiffrées proviennent des sorties reproductibles du notebook
`climate_messeix.ipynb` (fichiers CSV dans `data/`).

---

## 3. Climatologie et normales (1991–2020)

### 3.1 Températures et précipitations mensuelles — station TAUVES (851 m)

| Mois | Tmean (°C) | Tmin (°C) | Tmax (°C) | Précip. (mm) |
|---|---|---|---|---|
| Jan | 1,64 | −1,09 | 5,43 | 105,4 |
| Fév | 1,58 | −1,40 | 6,24 | 95,5 |
| Mar | 4,82 | 1,17 | 10,08 | 89,4 |
| Avr | 8,56 | 3,27 | 12,95 | 111,6 |
| Mai | 11,50 | 6,63 | 16,91 | 112,2 |
| Jui | 15,52 | 10,12 | 20,98 | 98,7 |
| Jui | 17,51 | 11,90 | 23,02 | 97,9 |
| Aoû | 16,80 | 11,97 | 23,09 | 91,0 |
| Sep | 13,71 | 8,76 | 18,96 | 101,1 |
| Oct | 10,33 | 6,39 | 14,84 | 109,6 |
| Nov | 5,62 | 2,28 | 9,05 | 137,7 |
| Déc | 2,66 | −0,16 | 6,23 | 124,9 |

- **Température annuelle moyenne (station)** : **~9,2 °C**.
- **Précipitations annuelles (station)** : **~1 275 mm** — site nettement humide,
  avec un maximum en novembre (138 mm) et des mois d'été encore bien arrosés
  (~90–100 mm), ce qui tempère le stress hydrique.
- **Hivers froids** : Tmin de janvier/février ≈ **−1,1 à −1,4 °C** (gel quasi
  quotidien). **Étés doux** : Tmax de juillet/août ≈ **23,0–23,1 °C**.

*Figure : `figures/fig1_climatology.png`.*

### 3.2 Comparaison ERA5 / station

La précipitation annuelle ERA5 (~1 165 mm) est légèrement inférieure à celle de la
station TAUVES (~1 275 mm), écart attendu (~9 %) cohérent avec le biais connu d'ERA5
(sous-estimation en contexte montagnard de vallée, lissage des cumuls orographiques).
Les températures moyennes annuelles sont cohérentes (ERA5 ~8,6 °C vs station
~9,2 °C ; écart principalement attribuable à la différence d'altitude et à la
résolution de la grille). Le site étant à ~800 m, on applique un **gradient
altitudinal** (~0,6 °C/100 m) quand on transpose les valeurs de stations situées
plus bas. **TAUVES (851 m, ~9,4 km) est représentative du microclimat d'altitude
de Messeix** (même étage).

---

## 4. Tendances et évolution (1940–2026)

### 4.1 Températures (pente de Sen, °C/décennie)

| Variable | Pente Sen | p-value | IC 95 % |
|---|---|---|---|
| **Tmean annuelle** | **+0,222** | 8,1×10⁻⁹ | [0,16 ; 0,29] |
| Tmin annuelle | +0,236 | 6,9×10⁻¹¹ | [0,18 ; 0,29] |
| Tmax annuelle | +0,229 | 3,0×10⁻⁷ | [0,15 ; 0,32] |
| Précip. annuelle (mm/déc) | **+23,3** | 0,012 | [4,1 ; 40,1] |

**Tendance saisonnière de Tmean (°C/déc) :**

| Saison | Pente | p-value | Significatif ? |
|---|---|---|---|
| Hiver (DJF) | **+0,354** | 3×10⁻⁸ | Oui |
| Printemps (MAM) | +0,144 | 0,013 | Oui |
| Été (JJA) | **+0,245** | 9×10⁻⁶ | Oui |
| Automne (SON) | +0,171 | 1,3×10⁻⁴ | Oui |

**Lecture** : réchauffement **robuste toutes saisons**, maximal en **hiver**
(+0,35 °C/déc) — cohérent avec la réduction de l'enneigement et des gelées hivernales —
et soutenu en été. La tendance des précipitations annuelles est positive et
significative, mais les tendances **saisonnières de précipitations ne sont pas
robustes** (seuls MAM p≈0,07 et SON p≈0,04 sont marginalement significatifs ; DJF
et JJA non significatifs). **On ne conclut donc pas à un changement saisonnier de
pluviométrie.**

*Figures : `figures/fig2_trend_temperature.png`, `figures/fig3_trend_precip.png`.*

### 4.2 Anomalies décennales (réf. 1961–1990)

| Décennie | ΔT (°C) | ΔP (mm) |
|---|---|---|
| 1990s | +0,74 | −78 |
| 2000s | +0,80 | −112 |
| **2010s** | **+1,17** | −60 |
| **2020s** | **+2,47** | +65 |

La décennie 2020 (partielle, 2020–2026) présente une anomalie de **+2,47 °C**,
sans précédent dans la série, confirmant une **accélération récente** du
réchauffement. Les anomalies de précipitations décennales sont **incohérentes en
signe** (sèches dans les 1990–2010, humide dans les 2020) : on ne retient **aucune
tendance décennale fiable** de pluviométrie.

*Figure : `figures/fig4_decadal_anomaly.png`.*

---

## 5. Indicateurs agroclimatiques et bioclimatiques

### 5.1 Normale 1991–2020 vs récent (ERA5)

| Indicateur | Normale 1991–2020 | Récent 2016–2025 |
|---|---|---|
| Jours de gel / an | **83,9** | **58,5** |
| Jours chauds (Tmax > 30 °C) | 1,4 | **5,8** |
| Jours Tmax > 35 °C | 0,0 | ~0 |
| Saison de croissance (5 °C), jours | **242** | **267** |
| Saison de croissance (10 °C), jours | 157 | ~170 |
| GDD (base 5 °C) | **1 753** | **2 109** |
| GDD (base 10 °C) | 756 | ~950 |
| Indice de Huglin | **1 103** | **1 373** |
| Indice de De Martonne | 62,9 | 68,4 (non sec) |

**Interprétation** :
- **La saison de croissance s'allonge** (~+25 jours en 35 ans) et les **GDD
  augmentent fortement** (~+20 %), améliorant la viabilité des cultures à cycle
  long (maïs grain, soja, arboriculture, vigne en limite).
- **Le risque de gelées tardives demeure le facteur limitant n°1** : voir 5.4.
- L'indice de Huglin (~1 100 → ~1 370) reste **marginal pour la vigne** (zone
  froide), mais la tendance rend le **pinot/gamay en limite haute** de plus en
  plus envisageable sur les coteaux bien exposés (à confirmer par l'analyse des
  gels tardifs, qui restent pénalisants).
- **L'indice de De Martonne (> 60)** indique un **climat humide** à l'échelle
  annuelle : la contrainte n'est **pas un déficit annuel** mais un **déficit
  estival ponctuel** (canicules) et une **variabilité interannuelle** forte.

*Figures : `figures/fig5_growing_season.png`, `figures/fig6_gdd.png`.*

### 5.2 Bilan hydrique et évapotranspiration

Le bilan hydrique climatique (P − ETP, FAO-56) montre un **excédent annuel net**
(climat humide), mais un **déficit estival marqué** en juillet-août, accentués lors
des étés caniculaires récents. La réserve utile des sols d'altitude (sols volcaniques
superficiels sur le plateau) est limitée ; le déficit estival devient donc **le
facteur de stress dominant** pour les cultures d'été et les prairies.

*Figure : `figures/fig7_water_balance.png`.*

### 5.3 Sécheresse (SPI / SPEI 12 mois)

Les indices **SPI et SPEI à 12 mois** (calculés sur toute la série) montrent des
épisodes secs récurrents et une tendance des **SPEI vers des valeurs plus négatives
dans les années récentes** (sécheresses 2011, 2015, 2022). Le SPEI (qui intègre la
demande évaporative) détecte une **aggravation du stress hydrique** que le SPI
(pluie seule) ne capte pas : l'augmentation de l'ETP due au réchauffement accentue
les déficits, même à pluviométrie constante.

*Figure : `figures/fig9_drought_spei.png`.*

### 5.4 Risque de gel — fenêtres de gel

Probabilité de gel (Tmin < 0 °C) par période de 10 jours (normale 1991–2020) :

| Période (jour de l'année) | Période calendaire | Prob. de gel |
|---|---|---|
| 1–10 | début janvier | 0,87 |
| 41–50 | mi-février | 0,97 |
| 81–90 | fin mars | 0,87 |
| 101–110 | mi-avril | 0,60 |
| 111–120 | fin avril | **0,30** |
| 121–130 | début mai | **0,20** |
| 131–140 | mi-mai | **0,07** |
| 141–150 | fin mai | **0,00** |
| … | juin–septembre | **0,00** |
| 281–290 | début octobre | 0,07 |
| 291–300 | mi-octobre | 0,27 |
| 301–310 | fin octobre | 0,37 |
| 311–320 | début novembre | 0,60 |

**Fenêtre sans gel (probabilité nulle) : ~141 à 280, soit approximativement
fin mai → début octobre.** C'est la **fenêtre de sécurité** pour les cultures
sensibles au gel (vergers, vigne, potager). Le risque de gel reste **non
négligeable (~20–30 %) jusqu'à fin avril/début mai**, ce qui est critique : un
printemps plus précoce (végétation avancée) peut exposer les jeunes pousses à des
gels tardifs.

*Figure : `figures/fig8_frost_risk.png`.*

---

## 6. Plan d'adaptation agricole (recommandations fondées sur les données)

> Les recommandations sont un **jugement d'expert** s'appuyant sur les tendances
> observées (Sections 4–5). Elles sont classées par **robustesse** face aux deux
> trajectoires plausibles — **chaud-humide** (tendance récente) et **chaud-sec**
> (risque si le déficit estival s'aggrave).

### 6.1 Choix des cultures et variétés

**Recommandations robustes (dans les deux trajectoires) :**
- **Variétés précoces et à cycle plus long** tirant parti de la saison allongée
  (+25 j) et des GDD en hausse : maïs grain/semence précoce, soja, tournesol sur
  les meilleures terres.
- **Sélectionner des variétés à forte tolérance au gel printanier** (l'augmentation
  des gels tardifs après redoux est le risque clé). Privilégier des **porte-greffes
  et variétés rustiques** pour l'arboriculture.
- **Arboriculture fruitière** (pommiers/poiriers rustiques, et à terme cerisiers
  tardifs) : viable dans la fenêtre sans gel, mais à planter sur les **coteaux
  exposés** (drainage des écoulements d'air froid vers les bas-fonds gelifs).
- **Vigne (pinot noir, gamay) en limite thermique haute** : l'indice de Huglin
  (~1 370) rend la viticulture **marginalement possible** sur les meilleurs
  terroirs bien exposés, mais le **gel printanier reste un frein majeur** — à
  réserver aux sites protégés et avec protection antigel.

**Recommandations sensibles à la trajectoire (à arbitrer selon l'évolution du
déficit estival) :**
- Les **protéagineux de printemps** (pois, féverole) et les **cultures de semences**
  sont attractifs (débouchés + climat frais), mais vulnérables au stress estival en
  trajectoire sèche : les réserver aux parcelles irrigables ou à sols profonds.

### 6.2 Eau et irrigation

- **Maintenir et développer le stockage d'eau** (bassines, retenues collinaires)
  : le bilan annuel est excédentaire, mais le **déficit estival est le facteur
  limitant** et devrait s'accentuer avec l'augmentation de l'ETP.
- **Prioriser l'irrigation localisée (goutte-à-goutte)** sur les cultures à forte
  valeur ajoutée (arboriculture, semences), pas l'irrigation généralisée des
  prairies.
- **Conservation de l'eau du sol** : paillage, couverts végétaux, **semis direct /
  travail réduit du sol**, apports de matière organique pour accroître la réserve
  utile des sols superficiels.
- **Choisir des variétés résistantes à la sécheresse** (tolérance à la chaleur et
  au déficit hydrique) en parallèle de la résistance au gel.

### 6.3 Gestion du risque de gel

Étant donné un printemps plus précoce (avancement du débourrement) couplé à un
risque de gel jusqu'à fin avril/mai :
- **Semis/plantation décalés** pour éviter les fenêtres de gel tardif.
- **Protection active contre le gel** : aspersion antigel, chauffage/brûleurs, voiles
  d'hivernage, **retard de taille** et taille raisonnée pour différer le débourrement.
- **Porte-greffes rustiques et variétés à débourrement tardif** pour l'arboriculture.
- **Sites de plantation sur les pentes exposées au sud/est**, à l'abri des coulées
  d'air froid (bas-fonds = zones gelives à éviter pour les cultures sensibles).

### 6.4 Élevage et prairies

- **Hivers plus doux** (DJF +0,35 °C/déc) : réduction des besoins en fourrage
  d'hiver et de la mortalité au froid, mais risque de **gel-dégel** sur les
  prairies et de **pathologies** nouvelles.
- **Étés plus chauds et secs** : **stress thermique du bétail** (accès à l'ombre
  et à l'eau) et **baisse de productivité des prairies** en juillet-août → sécuriser
  les **stocks fourragers** (fauche précoce, dérobées, silo) et **diversifier les
  espèces prairiales** (mélanges résistants à la sécheresse).
- Envisager un **décalage/adaptation des calendriers de pâturage** et une gestion
  adaptative des prairies selon l'année.

### 6.5 Diversification et gestion du risque

- **Rotations climato-résilientes** et diversification des cultures pour amortir
  les aléas (gel, sécheresse, excès d'eau).
- **Agroforesterie** (arbres de service/bois, haies) : microclimat, rétention
  d'eau, brise-vent, protection contre le stress thermique des cultures et du bétail.
- **Assurance récolte et cadrage économique du risque** (notamment gel et
  sécheresse) : outil essentiel car ces deux aléas **peuvent coexister dans une
  même année** (gel tardif au printemps + sécheresse estivale).

### 6.6 Synthèse de robustesse

| Recommandation | Trajectoire chaud-humide | Trajectoire chaud-sec |
|---|---|---|
| Variétés précoces / cycle long | ✔ Robuste | ✔ Robuste |
| Tolérance au gel printanier | ✔ Robuste | ✔ Robuste |
| Arboretum / arboriculture (coteaux) | ✔ Robuste | ✔ Robuste |
| Vigne en limite haute | ⚠ Sensible (gel) | ⚠ Sensible (gel + sec) |
| Protéagineux de printemps | ✔ | ⚠ (irrigation requise) |
| Stockage d'eau / irrigation localisée | ✔ | ✔ **Indispensable** |
| Gestion active du gel | ✔ Robuste | ✔ Robuste |
| Diversification / agroforesterie / assurance | ✔ Robuste | ✔ Robuste |

**Décisions sensibles à la trajectoire** : développement de la vigne et des cultures
d'été intensives (dépendent de l'évolution du déficit estival et de la capacité
d'irrigation). **Décisions robustes dans tous les cas** : choix variétal précoce et
tolérant au gel, gestion active du risque de gel, stockage d'eau, diversification
et agroforesterie.

---

## 7. Limites et incertitudes (caveats)

1. **Source ERA5 via Open-Meteo** : les champs sont une **réanalyse** (miroir ERA5)
   et non des observations au sol ; biais connus en contexte montagnard —
   **sous-estimation de la pluviométrie orographique** (écart ~9 % vs station) et
   lissage des températures de vallée. L'altitude effective de la cellule peut
   différer de celle de la commune (~800 m).
2. **Station de référence** : TAUVES (851 m) est bien représentative de l'étage
   d'altitude, mais à ~9 km ; l'écart résiduel avec le microclimat exact de Messeix
   reste un facteur d'incertitude (gradient ~0,6 °C/100 m appliqué).
3. **Tendances** : les tendances de température sont **statistiquement
   significatives** et robustes ; les tendances de précipitations **ne le sont pas
   au niveau saisonnier** et ne doivent pas être surinterprétées.
4. **Anomalie décennale 2020s** : la décennie est **partielle** (2020–2026) et
   l'anomalie +2,47 °C est indicative d'une accélération, à confirmer avec les
   années à venir.
5. **Absence de données de projection** : **aucun scénario RCP/SSP (DRIAS /
   EURO-CORDEX) n'a pu être récupéré** dans cette analyse. **Aucune valeur projetée
   n'est donc fournie** — les recommandations reposent exclusivement sur les
   tendances observées et sont qualifiées en conséquence. Une extension future avec
   les projections DRIAS (SSP2-4.5, SSP5-8.5) est recommandée pour affiner le plan
   à l'horizon 2050–2100.
6. **Indicateurs bioclimatiques** (Huglin, De Martonne, SPI/SPEI) sont des indices
   standard, calculés sur ERA5 : ils servent de **repères relatifs** et non de
   valeurs absolues de terrain.

---

## 8. Annexes et traçabilité

- **Notebook complet** : `climate_messeix.ipynb` (chaque cellule exécutée ;
  chaque chiffre du rapport y est tracé).
- **Scripts** : `fetch_era5.py`, `build_notebook.py` ; **environnement** :
  `environment.yml` (versions des packages épinglées).
- **Données brutes** : `data/` (séries ERA5 journalières, stations Météo-France,
  climatologies, indices, tendances).
- **Figures** : `figures/fig1..fig9_*.png` (climatologie, tendances T/P, anomalies
  décennales, saison de croissance, GDD, bilan hydrique, risque de gel, SPI/SPEI).
- **Sources** : ERA5 — Hersbach, H. et al. (2023), *ERA5 hourly data on single
  levels from 1940 to present*, Copernicus Climate Change Service (C3S) Climate
  Data Store, DOI : 10.24381/cds.adbb2d47. Météo-France — données Climatologie
  open data, stations 63225001 (MESSEIX) et 63426001 (TAUVES).
