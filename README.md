# Uncivilisation
    **PAS DE CHAT GPT**

Si vous lisez ce Readme, vous avez échangé votre projet et avez récupéré le nôtre, nous voudrions que vous lisiez attentivement celui-ci, vous y trouverez les explications plus détaillées de certaines choses pour comprendre notre code.

Notre projet est un jeu qui se joue au tour par tour, dans un style en 2D. La carte est constituée d'hexagone qui sont placés en fonction de leur taille. Leur taille est de en largeur, 175 pixels, puis en longueur, 173 pixels. Pour la carte, nous avons décidé d'utiliser une matrice qui est remplie de dictionnaires pour chacun des hexagones, ces dictionnaires sont composés du biome de l'hexagone, et de ses coordonnées x et y. Dans ce dictionnaire, on aimerait bien mettre aussi toutes les spécifications que les biomes apportent (ressources, les bâtiments qu'ils contiennent...). Pour la génération des hexagones, nous utilisons la fonction génération_hexagone. Elle va mettre dans la matrice, colonne par colonne, les hexagones. Elle va le faire en fonction des variables longueur et largeur que vous pourrez modifier pour avoir plus d'hexagones.

Pour l'utilisation de notre code, vous auriez besoin des bibliothèques Python **pygame**

Nous avons plusieurs petits problèmes avec notre code : 
    - en premier, nous pouvons citer le fait que la matrice est lourde, mais le meilleur serais de pouvoir l'enregister dans un fichier (comme du json).
    - nous ne pouvons toujours pas nous déplacer dans la carte, ni la faire agrandir ou la diminuer.

Après avoir lu notre readme, nous vous avons mis une branche spéciale pour que vous puissiez modifier à votre guise notre code. Dans cette branche, vous avez tous les droits, y compris de modifier les fichiers qui sont nécessaires au code. Toutefois, merci de veiller à tous nous expliquer plus tard, pour le fonctionnement de votre code, pour nous faciliter la compréhension ainsi que l'utilisation de ce code.
