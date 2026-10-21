# IT Equipment Loan

Projet de module Odoo 19 pour gérer le prêt de matériel informatique. Le nom
technique prévu pour le module est `it_equipment_loan`. Le développement du
module n'a pas encore commencé.

## Environnement de développement

L'environnement Docker Compose fournit :

- Odoo, accessible sur le port défini par `ODOO_PORT` dans `.env` ;
- PostgreSQL, accessible depuis pgAdmin sur le réseau Docker ;
- pgAdmin, accessible dans un navigateur à l'adresse
  [http://localhost:5050](http://localhost:5050) ;
- Mailpit, accessible à l'adresse [http://localhost:8025](http://localhost:8025).

Le mode développeur serveur Odoo est activé au démarrage avec `--dev=all`.
Pour activer les outils développeur dans l'interface web, ouvrez Odoo avec
`?debug=1` (ou activez le mode développeur dans les paramètres Odoo).

### Accès à pgAdmin

Connectez-vous à pgAdmin avec :

- Adresse : `admin@localhost`
- Mot de passe : la valeur de `POSTGRES_PASSWORD` dans `.env`

Ajoutez ensuite un serveur PostgreSQL dans pgAdmin :

- **Host name/address** : `db`
- **Port** : `5432`
- **Maintenance database** : la valeur de `POSTGRES_DB` dans `.env`
- **Username** : la valeur de `POSTGRES_USER` dans `.env`
- **Password** : la valeur de `POSTGRES_PASSWORD` dans `.env`

Le nom d'hôte `db` est celui utilisé entre conteneurs Docker. PostgreSQL n'est
pas exposé directement sur un port de l'hôte : utilisez pgAdmin pour consulter
et gérer la base depuis le navigateur.

## Démarrage

Créez/configurez le fichier `.env` à partir des variables nécessaires au
compose, puis lancez les services :

```bash
docker compose up -d
```

Pour consulter les commandes courantes (mise à jour du module, logs, arrêt),
voir [commande.md](./commande.md).
