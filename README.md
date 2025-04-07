# Flappy Bird 74

Le jeu reprend le concept de Flappy bird. Ici les tuyaux sont remplacés par des arbres. Et le joueur ou la joueuse peut gagner des points en touchant des bulles de points.

## Technologies utilisées

- Pygame
- Watchdog

## Fonctionnalités (v1)

- Saut de l’oiseau
- Collision avec les arbres
- Ajout de points lorsqu'une bulle est touchée
- Mettre en pause / reprendre le jeu

## Ressources utilisées (v1)

- Images et décors (personnage, arbres, nuages, bulle de points, etc.) : Pygame
- Musique : [POL-magical-sun-short de Filippo Vicarelli](https://www.filippovicarelli.com/8bit-game-background-music)
- Sons : [Soundsnap](https://www.soundsnap.com/)

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