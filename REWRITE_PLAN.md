# Plan de réécriture

Ce projet contient actuellement des binaires Windows (
`build/`, `dist/`, `ffmpeg.exe`). Pour faciliter l'usage multiplateforme,
la réécriture proposée consiste à :

1. Supprimer les exécutables Windows du dépôt et ignorer les dossiers
   générés via `.gitignore`.
2. Utiliser `os.path` pour la gestion des chemins afin de rester
   indépendant du système d'exploitation.
3. Fournir un fichier `requirements.txt` et des instructions
   d'installation basées sur `pip` et `python`.
4. S'assurer que `ffmpeg` est installé sur la machine hôte et accessible
   via la variable `PATH`.

Les fichiers de ce dépôt ont été adaptés en conséquence et les étapes
ci-dessus permettent de faire fonctionner l'application sur Linux,
macOS et Windows sans dépendre de composants spécifiques à Windows.
