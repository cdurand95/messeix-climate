# Messeix Climate — Rapport climatique & plan d'adaptation agricole

Analyse climatique quantitative de la commune de **Messeix** (Puy-de-Dôme, Massif
Central, France, ~45,62° N, 2,54° E, ~800 m), fondée sur les données **ERA5**
(réanalyse, via Open-Meteo, 1940–2026) et les stations **Météo-France** (MESSEIX
63225001 et TAUVES 63426001), traduite en **plan d'adaptation agricole** pour les
prochaines décennies.

## Livrables

| Fichier | Description |
|---|---|
| `CLIMATE_REPORT_Messeix.md` | **Rapport final** (en français) : résumé exécutif, méthodes, résultats (climatologie, tendances, indicateurs agroclimatiques), limites, et plan d'adaptation agricole. |
| `climate_messeix.ipynb` | Notebook reproductible contenant tous les téléchargements de données, traitements, calculs de tendances/indices et figures. |
| `build_notebook.py` | Script qui génère le notebook. |
| `fetch_era5.py` | Script de téléchargement des séries ERA5 (via API Open-Meteo). |
| `environment.yml` | Environnement conda (versions des packages épinglées). |
| `data/` | Données brutes et sorties (séries ERA5, stations Météo-France, climatologies, tendances, indices, SPI/SPEI). |
| `figures/` | 9 figures PNG (climatologie, tendances T/P, anomalies décennales, saison de croissance, GDD, bilan hydrique, risque de gel, SPI/SPEI). |

## Principaux résultats (synthèse)

- **Réchauffement robuste** : Tmean **+0,22 °C/décennie** (1940–2026, p ≈ 8×10⁻⁹),
  maximal en hiver (DJF +0,35 °C/déc). Anomalie décennale 2020s : **+2,47 °C**
  vs 1961–1990.
- **Précipitations** : +23 mm/déc à l'échelle annuelle, mais **pas de changement
  saisonnier robuste**.
- **Agroclimatique** : gelées **84 → 59 j/an**, saison de croissance (5 °C)
  **242 → 267 j**, GDD5 **1 753 → 2 109 °C·j**, Indice de Huglin **1 103 → 1 373**.
  Fenêtre sans gel : ~fin mai → début octobre.
- **Sécheresse** : SPEI 12 mois en baisse récente (stress hydrique aggravé par
  l'augmentation de l'ETP), malgré un bilan hydrique annuel excédentaire.

Le rapport sépare strictement **données observées** (ERA5 + stations),
**recommandations** (jugement d'expert) et note explicitement l'**absence de
données de projection** RCP/SSP dans cette analyse (non chiffrées).

## Reproducibilité

1. Créer l'environnement :
   ```bash
   conda env create -f environment.yml
   conda activate messeix-climate
   ```
2. (Re)construire et exécuter le notebook :
   ```bash
   python build_notebook.py   # génère climate_messeix.ipynb
   jupyter nbconvert --to notebook --execute climate_messeix.ipynb
   ```
3. Chaque chiffre du rapport est traçable vers une cellule exécutée du notebook.

> Toute affirmation quantitative du rapport renvoie à une cellule reproductible et
> à une source citée (ERA5 et/ou Météo-France). Aucune valeur n'est inventée.

## Sources

- **ERA5** : Hersbach, H. et al. (2023), *ERA5 hourly data on single levels from
  1940 to present*, Copernicus Climate Change Service (C3S) Climate Data Store,
  DOI : 10.24381/cds.adbb2d47 (accès via API Open-Meteo).
- **Météo-France** : données Climatologie open data, stations 63225001 (MESSEIX)
  et 63426001 (TAUVES).
