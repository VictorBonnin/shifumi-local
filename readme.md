Ce projet permet de jouer au jeu du shifumi (pierre, papier, ciseaux), de manière locale, avec un serveur. Le serveur utilise kafka ainsi que Zookeeper, qui sont lancés à partir d'un dockerfile.

Voici les étapes pour lancer le projet :

étape 1 : 
lancer le dockercompose :  docker-compose up --build

étape 2 :
lancer les 2 instances de jeu dans des terminaux différents : python ui.py

2tape 3 (facultative) :
regarder le sdifférents résultats dans le json : curl http://localhost:5000/result
