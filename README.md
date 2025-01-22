# Uncivilisation
Notre projet est un jeu qui se joue au tour par tour, dans un style un 2D. La carte est constituer d'hexagone qui sont placer en fonction de leurs taille. Leur taille est de en laargeur, 175 pixels puis en longeur, 173 pixels. Pour la carte, nous avons décider d'utiliser une matrice qui est remplie de dictionnaires pour chaqu'un des hexagones, ces dictionnaires sont composé du biome de l'hexagone, et de ,ces coordonnées x et y. Dans ce dictionnaire on aimerais bien mettre aussi toutes les spécifications que les biomes apporte (ressources, les batiments qu'il contient...). pour la génration des hexagones, nous utilisons la fonction génération_hexagone, elle va mettre dans la matrice, colone par colone les hexagones dans la matrice, elle va le faire en fonction des variables longeur et largeur que vous pourrez modifier pour avoir plus d'hexagones. 

Pour l'utilisation de notre code, vous aurais bessoin des bibliothèques python **pygame**

Nous avons plusieurs petits problèmes avec notre code : 
    - en premiers nous pouvons citer le fait que la matrice est lourde, mais 