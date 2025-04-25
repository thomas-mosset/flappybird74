# Flappy Bird 74 (v2)

Le jeu reprend le concept de Flappy bird. Le joueur ou la joueuse peut gagner des points en touchant des pièces, et doit esquiver des tuyaux.

## Technologies utilisées

- Pygame
- Watchdog

## Fonctionnalités (v2)

- Saut de l’oiseau
- Collision avec les tuyaux
- Ajout de points lorsqu'une pièce est touchée
- Mettre en pause / reprendre le jeu
- Navigation entre les différents menus
- Musique ON / OFF

## Ressources utilisées (v2)

- Personnage : Pygame
- Images et décors (tuyaux, nuages, pièces, montagne, etc.) : Canva
- Musique : [POL-magical-sun-short de Filippo Vicarelli](https://www.filippovicarelli.com/8bit-game-background-music)
- Sons : [Soundsnap](https://www.soundsnap.com/)
- Font : Press Start 2P de CodeMan38

## Démo (v1)

[![Démo du jeu (v1)](https://markdown-videos-api.jorgenkh.no/youtube/B4nhvpC_mMQ)](https://youtu.be/B4nhvpC_mMQ)

## Démo (v2)

[![Démo du jeu (v2)](https://markdown-videos-api.jorgenkh.no/youtube/Hz4l7dubO_0)](https://youtu.be/Hz4l7dubO_0)

## Lancer le jeu

Cloner le repo, puis lancer les commandes suivantes :

```sh
Pip install pygame
```

Puis :

```sh
python flappy.py
```

Si utilisation de Watchdog (permet de surveiller les changements dans le fichier pour refresh le jeu automatiquement) :

```sh
watchmedo auto-restart --patterns="*.py" --recursive -- python flappy.py
```
