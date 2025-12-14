# 🚀 Déploiement Public - SkinCheck

Guide rapide pour rendre votre application accessible publiquement avec Apache.

## Option Recommandée : VPS avec Apache

### Résumé Rapide

1. **Louer un VPS** (5-10€/mois) : OVH, DigitalOcean, Hetzner, etc.
2. **Installer Apache et Docker** sur le serveur
3. **Déployer l'application** avec Docker
4. **Configurer Apache** comme reverse proxy
5. **Activer HTTPS** avec Let's Encrypt

### Guide Complet

📖 Voir [deployment/apache-deployment.md](deployment/apache-deployment.md) pour les instructions détaillées.

## 🎯 Démarrage Rapide (Si vous avez déjà un serveur)

### 1. Installer les prérequis

```bash
# Installer Apache
sudo apt update
sudo apt install apache2 docker.io docker-compose -y

# Activer les modules Apache
sudo a2enmod proxy proxy_http ssl rewrite headers
sudo systemctl restart apache2
```

### 2. Déployer l'application

```bash
cd /home/sebabte/canc
docker-compose up -d
```

### 3. Configurer Apache

```bash
# Copier la configuration
sudo cp deployment/apache-vhost.conf /etc/apache2/sites-available/skincheck.conf

# Éditer pour remplacer "votre-domaine.com" par votre domaine ou IP
sudo nano /etc/apache2/sites-available/skincheck.conf

# Activer le site
sudo a2ensite skincheck.conf
sudo systemctl reload apache2
```

### 4. Configurer le firewall

```bash
sudo ufw allow 22/tcp   # SSH
sudo ufw allow 80/tcp   # HTTP
sudo ufw allow 443/tcp  # HTTPS
sudo ufw enable
```

### 5. Activer HTTPS (si vous avez un domaine)

```bash
sudo apt install certbot python3-certbot-apache -y
sudo certbot --apache -d votre-domaine.com
```

✅ **C'est fait !** Votre application est maintenant accessible publiquement.

## 🌐 Accès

- **Avec domaine** : `https://votre-domaine.com`
- **Sans domaine** : `http://VOTRE_IP_PUBLIQUE`

## 📋 Autres Options

### Option 1 : Réseau Local Uniquement

Si vous voulez juste partager sur votre réseau local (WiFi) :

```bash
# Modifier docker-compose.yml
ports:
  - "0.0.0.0:5000:5000"

# Redémarrer
docker-compose restart
```

Accès : `http://[VOTRE_IP_LOCALE]:5000` depuis n'importe quel appareil sur votre réseau.

### Option 2 : Tunnel ngrok (Temporaire)

Pour un accès Internet rapide et temporaire :

```bash
# Installer ngrok
curl -s https://ngrok-agent.s3.amazonaws.com/ngrok.asc | sudo tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null
echo "deb https://ngrok-agent.s3.amazonaws.com buster main" | sudo tee /etc/apt/sources.list.d/ngrok.list
sudo apt update && sudo apt install ngrok

# Créer un compte sur https://ngrok.com et obtenir votre token
ngrok config add-authtoken VOTRE_TOKEN

# Démarrer le tunnel
ngrok http 5000
```

Vous obtiendrez une URL publique comme `https://abc123.ngrok.io`

## 🔒 Sécurité

> [!WARNING]
> Avant de rendre l'application publique, considérez :
> - Ajouter une authentification (login/password)
> - Activer HTTPS (obligatoire pour les données médicales)
> - Limiter les uploads de fichiers
> - Configurer un firewall

## 📞 Besoin d'Aide ?

- **Guide complet Apache** : [deployment/apache-deployment.md](deployment/apache-deployment.md)
- **Configuration Apache** : [deployment/apache-vhost.conf](deployment/apache-vhost.conf)
- **Dépannage** : Vérifiez les logs avec `docker-compose logs -f` et `sudo tail -f /var/log/apache2/skincheck-error.log`

## 💰 Coûts Estimés

| Option | Coût | Complexité | Permanent |
|--------|------|------------|-----------|
| Réseau Local | Gratuit | ⭐ | Oui |
| ngrok | Gratuit/5$/mois | ⭐ | Non (URL change) |
| VPS (OVH) | 5€/mois | ⭐⭐ | Oui |
| VPS (DigitalOcean) | 6$/mois | ⭐⭐ | Oui |
| Cloud (Heroku) | 7$/mois | ⭐⭐⭐ | Oui |

## 🎓 Recommandation

Pour une application médicale professionnelle, je recommande :
1. **VPS avec Apache** (ce guide)
2. **Nom de domaine** (~10€/an)
3. **HTTPS avec Let's Encrypt** (gratuit)
4. **Authentification** (à implémenter)

**Coût total** : ~5-10€/mois + 10€/an pour le domaine
