# Messeix — Climat & agriculture

Bienvenue sur le site de synthèse du **Rapport Climatique de Messeix**
(Puy-de-Dôme, Massif Central, France). Ce site regroupe les livrables du projet :

- un **rapport climatique** fondé sur les données ERA5 (Open-Meteo) et les
  stations Météo-France, traduisant l'évolution observée (1940–2026) du climat
  local en un plan d'adaptation agricole ;
- un **guide de sélection** des légumes et arbres fruitiers adaptés aux
  contraintes mesurées du site (hivers froids, gel tardif, étés frais et brefs) ;
- les **figures** et l'ensemble des données et notebooks reproductibles.

## Documents

| Document | Contenu |
| --- | --- |
| [Rapport climatique](CLIMATE_REPORT_Messeix.md) | Données & méthodes, climatologie 1991–2020, tendances 1940–2026, indicateurs agroclimatiques, bilan hydrique, risque de gel, plan d'adaptation, limites & incertitudes, annexes de traçabilité. |
| [Guide légumes & arbres](PLANT_GUIDE_Messeix.md) | Choix de végétaux (légumes, petits fruits, arbres fruitiers, noix/châtaigne, agroforesterie) priorisés selon les contraintes climatiques mesurées. |

## Points clés (résumé)

- **Réchauffement** : +0,22 °C/décennie sur la température moyenne annuelle
  (ERA5 1940–2026, p ≈ 8e-9), plus marqué en hiver (+0,35 °C/décennie).
- **Saison de végétation allongée** : dernière gelée plus tardive/fin plus
  précoce selon les seuils, GDD en hausse.
- **Étés plus chauds** mais restant frais : Tmax ~23 °C en juillet, jours
  >35 °C quasi inexistants en normale.
- **Eau** : ~1 275 mm/an, avec déficit estival et risque de sécheresse
  (SPEI12 = −1,35 en octobre 2026).
- **Recommandations** classées par robustesse sous les scénarios chaud-sec et
  chaud-humide.

> Aucune donnée de projection (RCP/SSP) n'était accessible ; les recommandations
> reposent sur les tendances observées et sont clairement séparées des données
> et des projections.

## Reproductibilité

Données brutes (`data/`), notebook `climate_messeix.ipynb`, scripts
(`fetch_era5.py`, `build_notebook.py`) et `environment.yml` sont disponibles à la
racine du dépôt.
