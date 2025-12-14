# Déploiement avec Apache - Guide Complet

## 📋 Prérequis

- Un serveur Linux (Ubuntu/Debian recommandé)
- Accès root ou sudo
- Un nom de domaine pointant vers votre serveur (optionnel mais recommandé)

## 🚀 Installation et Configuration

### Étape 1 : Installer Apache et les modules nécessaires

```bash
# Mettre à jour le système
sudo apt update && sudo apt upgrade -y

# Installer Apache
sudo apt install apache2 -y

# Activer les modules nécessaires
sudo a2enmod proxy
sudo a2enmod proxy_http
sudo a2enmod ssl
sudo a2enmod rewrite
sudo a2enmod headers

# Redémarrer Apache
sudo systemctl restart apache2
```

### Étape 2 : Installer Docker et Docker Compose

```bash
# Installer Docker
sudo apt install docker.io docker-compose -y

# Démarrer Docker
sudo systemctl start docker
sudo systemctl enable docker

# Ajouter votre utilisateur au groupe docker
sudo usermod -aG docker $USER
newgrp docker
```

### Étape 3 : Déployer l'application Docker

```bash
# Aller dans le dossier du projet
cd /home/sebabte/canc

# Construire et démarrer l'application
docker-compose build
docker-compose up -d

# Vérifier que l'application fonctionne
curl http://localhost:5000
```

### Étape 4 : Configurer Apache comme Reverse Proxy

```bash
# Copier le fichier de configuration
sudo cp deployment/apache-vhost.conf /etc/apache2/sites-available/skincheck.conf

# Éditer le fichier pour remplacer "votre-domaine.com" par votre vrai domaine
sudo nano /etc/apache2/sites-available/skincheck.conf
# Remplacer toutes les occurrences de "votre-domaine.com"

# Activer le site
sudo a2ensite skincheck.conf

# Désactiver le site par défaut (optionnel)
sudo a2dissite 000-default.conf

# Tester la configuration
sudo apache2ctl configtest

# Recharger Apache
sudo systemctl reload apache2
```

### Étape 5 : Configurer le Firewall

```bash
# Installer UFW si pas déjà installé
sudo apt install ufw -y

# Autoriser SSH (IMPORTANT avant d'activer le firewall!)
sudo ufw allow 22/tcp

# Autoriser HTTP et HTTPS
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# Activer le firewall
sudo ufw enable

# Vérifier le statut
sudo ufw status
```

### Étape 6 : Configurer SSL avec Let's Encrypt (HTTPS)

```bash
# Installer Certbot
sudo apt install certbot python3-certbot-apache -y

# Obtenir un certificat SSL (remplacer par votre domaine)
sudo certbot --apache -d votre-domaine.com -d www.votre-domaine.com

# Suivre les instructions interactives:
# - Entrer votre email
# - Accepter les conditions
# - Choisir de rediriger HTTP vers HTTPS (recommandé)

# Le certificat se renouvellera automatiquement
# Tester le renouvellement automatique:
sudo certbot renew --dry-run
```

## 🌐 Accès Sans Nom de Domaine (IP uniquement)

Si vous n'avez pas de nom de domaine, vous pouvez utiliser l'IP directement :

### Configuration Apache simplifiée

Créer `/etc/apache2/sites-available/skincheck.conf` :

```apache
<VirtualHost *:80>
    ServerName votre-ip-publique
    
    ErrorLog ${APACHE_LOG_DIR}/skincheck-error.log
    CustomLog ${APACHE_LOG_DIR}/skincheck-access.log combined
    
    # Reverse Proxy
    ProxyPreserveHost On
    ProxyPass / http://127.0.0.1:5000/
    ProxyPassReverse / http://127.0.0.1:5000/
    
    # Headers de sécurité
    Header always set X-Frame-Options "SAMEORIGIN"
    Header always set X-Content-Type-Options "nosniff"
    
    # Limite uploads
    LimitRequestBody 10485760
    
    # Timeout
    ProxyTimeout 300
</VirtualHost>
```

Puis :
```bash
sudo a2ensite skincheck.conf
sudo systemctl reload apache2
```

Accès via : `http://VOTRE_IP_PUBLIQUE`

## 🔧 Commandes Utiles

### Gestion Apache

```bash
# Redémarrer Apache
sudo systemctl restart apache2

# Recharger la configuration (sans interruption)
sudo systemctl reload apache2

# Voir les logs en temps réel
sudo tail -f /var/log/apache2/skincheck-error.log
sudo tail -f /var/log/apache2/skincheck-access.log

# Tester la configuration
sudo apache2ctl configtest

# Voir les sites activés
sudo apache2ctl -S
```

### Gestion Docker

```bash
# Voir les logs de l'application
docker-compose logs -f

# Redémarrer l'application
docker-compose restart

# Mettre à jour après modification du code
docker-compose down
docker-compose build
docker-compose up -d
```

## 📊 Vérification

### 1. Vérifier que Docker fonctionne
```bash
docker-compose ps
# Devrait montrer le conteneur "web" en état "Up"

curl http://localhost:5000
# Devrait retourner du HTML
```

### 2. Vérifier qu'Apache fonctionne
```bash
sudo systemctl status apache2
# Devrait être "active (running)"

sudo apache2ctl -S
# Devrait lister votre VirtualHost
```

### 3. Tester l'accès externe
Depuis un autre ordinateur ou votre téléphone :
- Ouvrir `http://votre-domaine.com` ou `http://VOTRE_IP`
- Vous devriez voir l'application SkinCheck

## 🔒 Sécurité Recommandée

### 1. Limiter l'accès SSH
```bash
# Éditer la config SSH
sudo nano /etc/ssh/sshd_config

# Changer le port (optionnel)
Port 2222

# Désactiver login root
PermitRootLogin no

# Redémarrer SSH
sudo systemctl restart sshd
```

### 2. Installer Fail2Ban
```bash
# Installer
sudo apt install fail2ban -y

# Activer
sudo systemctl enable fail2ban
sudo systemctl start fail2ban
```

### 3. Mettre à jour régulièrement
```bash
# Mettre à jour le système
sudo apt update && sudo apt upgrade -y

# Redémarrer si nécessaire
sudo reboot
```

## 🐛 Dépannage

### Apache ne démarre pas
```bash
# Voir les erreurs
sudo systemctl status apache2
sudo journalctl -xe

# Vérifier la configuration
sudo apache2ctl configtest
```

### Erreur 502 Bad Gateway
```bash
# Vérifier que Docker tourne
docker-compose ps

# Vérifier les logs Docker
docker-compose logs

# Vérifier qu'Apache peut accéder à localhost:5000
curl http://localhost:5000
```

### L'application n'est pas accessible de l'extérieur
```bash
# Vérifier le firewall
sudo ufw status

# Vérifier qu'Apache écoute sur le bon port
sudo netstat -tlnp | grep apache

# Vérifier que votre domaine pointe vers le bon IP
dig votre-domaine.com
```

### Certificat SSL ne fonctionne pas
```bash
# Vérifier les certificats
sudo certbot certificates

# Renouveler manuellement
sudo certbot renew

# Vérifier la configuration Apache
sudo apache2ctl -S
```

## 📈 Optimisation Performance

### 1. Activer la compression
```bash
sudo a2enmod deflate
sudo systemctl reload apache2
```

### 2. Activer le cache
```bash
sudo a2enmod cache
sudo a2enmod cache_disk
sudo systemctl reload apache2
```

### 3. Limiter les ressources Docker
Éditer `docker-compose.yml` :
```yaml
services:
  web:
    deploy:
      resources:
        limits:
          memory: 4G
          cpus: '2'
```

## 🎯 Résumé des Commandes Essentielles

```bash
# Démarrer tout
docker-compose up -d
sudo systemctl start apache2

# Arrêter tout
docker-compose down
sudo systemctl stop apache2

# Redémarrer après modification
docker-compose restart
sudo systemctl reload apache2

# Voir les logs
docker-compose logs -f
sudo tail -f /var/log/apache2/skincheck-error.log

# Vérifier le statut
docker-compose ps
sudo systemctl status apache2
```

## 💡 Conseils

1. **Sauvegardez régulièrement** vos données et configurations
2. **Surveillez les logs** pour détecter les problèmes
3. **Mettez à jour** régulièrement le système et les applications
4. **Testez** toujours les modifications sur un environnement de test d'abord
5. **Documentez** vos changements de configuration

## 📞 Support

En cas de problème, vérifiez dans cet ordre :
1. Les logs Docker : `docker-compose logs`
2. Les logs Apache : `sudo tail -f /var/log/apache2/skincheck-error.log`
3. La configuration Apache : `sudo apache2ctl configtest`
4. Le firewall : `sudo ufw status`
5. La connectivité réseau : `ping votre-domaine.com`
