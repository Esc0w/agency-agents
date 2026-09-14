# Agency Agents — adaptation française

Cette branche `FR` propose une version française des **279 fiches d’agents**, réparties dans les **18 divisions** du dépôt. Les agents répondent en français par défaut ; une demande explicite ou la langue attendue d’un livrable peut modifier ce choix.

Les missions, les consignes, les traits de personnalité, les méthodes de travail et les modèles de livrables textuels sont traduits. Les spécialisations et les références géographiques d’origine sont conservées : un agent consacré au marché chinois ou à une réglementation américaine garde ce périmètre.

## Choisir un agent

Le [catalogue français](CATALOGUE.fr.md) donne les intitulés français, les identifiants d’origine et les liens vers les fiches. Le [lexique des intitulés](scripts/i18n/agent-names-fr.json) permet de retrouver les deux versions d’un nom.

Les fichiers restent dans les dossiers habituels, par exemple :

- [Développeur frontend](engineering/engineering-frontend-developer.md)
- [Rédacteur technique](engineering/engineering-technical-writer.md)
- [Concepteur narratif](game-development/narrative-designer.md)
- [Guide du marché français du conseil](specialized/specialized-french-consulting-market.md)
- [Auditeur d’accessibilité](testing/testing-accessibility-auditor.md)

## Utilisation et installation

Pour une utilisation manuelle, copiez le contenu de la fiche souhaitée dans votre outil. Pour les intégrations, exécutez les scripts depuis cette branche afin de générer les versions françaises.

Dans Git Bash sous Windows, ou dans un terminal Bash sous Linux/macOS :

```bash
git switch FR

# Générer les agents pour l’outil choisi.
./scripts/convert.sh --tool codex

# Installer ces agents dans la configuration de l’outil.
./scripts/install.sh --tool codex
```

Pour Claude Code, les fiches sources peuvent être installées directement :

```bash
./scripts/install.sh --tool claude-code
```

Les noms techniques restent ceux du dépôt d’origine. Exemple de demande :

> Utilise l’agent Frontend Developer pour examiner cette interface. Réponds en français et explique les améliorations prioritaires.

Les options et les autres outils pris en charge sont décrits dans le [guide des intégrations](integrations/README.md). Une installation effectuée depuis une autre branche utilise le contenu de cette autre branche.

## Choix de traduction

- Les champs techniques YAML, notamment `name`, les chemins et les noms de fichiers restent inchangés, afin de conserver les identifiants d’installation.
- Les champs `description` et `vibe`, les titres et le texte des fiches sont en français.
- Le code exécutable, les commandes, les noms d’API, les liens et les schémas techniques sont préservés. Les modèles de rapports en Markdown et les blocs de texte non exécutables sont traduits.
- Les noms de produits, les acronymes et les termes techniques usuels comme *frontend*, *backend* ou *responsive* sont conservés lorsque cela améliore la précision.
- Les références juridiques, les devises, les seuils et les chiffres ne sont pas remplacés par des équivalents français. Cette adaptation linguistique ne constitue pas une actualisation de ces informations.

La préparation combine une traduction automatique locale et une relecture ciblée des intitulés, des formulations récurrentes et des anomalies détectées. Elle ne constitue pas une révision experte exhaustive de chaque domaine métier.

## Vérification et mises à jour

La révision anglaise de référence est enregistrée dans [fr-source.json](scripts/i18n/fr-source.json). Les contrôles comparent les fiches françaises à cette révision, indépendamment de l’évolution ultérieure de `main`.

```bash
# Python 3.11+ et PyYAML sont nécessaires pour les contrôles Python.
python3 scripts/test-localization-fr.py
bash scripts/test-french-section-routing.sh
bash scripts/lint-agents.sh
bash scripts/check-divisions.sh
```

Les conversions OpenClaw reconnaissent les titres français pour conserver la séparation entre identité/règles et opérations. Après une modification des fiches, régénérez les intégrations concernées avec `scripts/convert.sh`.

La licence [MIT](LICENSE) du dépôt d’origine reste applicable.
