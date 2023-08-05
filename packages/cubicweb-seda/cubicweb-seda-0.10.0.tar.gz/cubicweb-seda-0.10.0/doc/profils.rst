Gestion des identifiants et références
---------------------------------------

Les identifiants spécifiés dans l'interface utilisateur sur les objets-données
et les unités d'archives sont reportés via un attribut `seda:profid` sur
l'élément correspond dans le XSD généré ([1]_). La valeur de cette attribut est
ensuite utilisée comme valeur par défaut des éléments référençant cet élement.

Ce mécanisme permet de gérer des identifiants pour des élements XSD qui ne sont
pas encore créés (puisqu'ils le seront à la création du bordereau), ce qui est
nécessaire pour pouvoir ensuite les référencer, la norme SEDA 2 faisant
largement usage de telles références. Il est à noter qu'il est donc à la
responsabilité de l'outil qui génère le bordereau de gérer les définitions de
références ainsi créées en substituant dans les éléments référençes la valeur de
l'identifiant qu'il a attribué à l'élement portant le `seda:profid`
correspondant.

Ceci n'étant pas un mécanisme standard du XSD, la cohérence des références entre
le bordereau et le profil ne sera pas vérifiée par les outils de validation XSD
classiques.


.. [1] le préfix `seda` étant associé à l'espace de nom
   "fr:gouv:culture:archivesdefrance:seda:v2.0"


Export RelaxNG des versions 0.2 et 1
------------------------------------

Les schémas des versions 0.2 et 1 de la norme SEDA utilisent des types personnalisés venant de
différents espaces de nom (par exemple
`fr:gouv:culture:archivesdefrance:seda:v1.0:QualifiedDataType:1`,
`urn:un:unece:uncefact:data:standard:UnqualifiedDataType:10`, etc.). Ces types ne sont
malheureusement pas utilisables dans un schéma RelaxNG, uniquement XSD. Pour palier à ce problème,
les éléments utilisant ces types sont exportés en tant que simple chaîne de caractères "xsd:string",
en supposant que les transferts seront validés contre le profil *et* contre le schéma XSD de la
norme. La même stratégie était utilisée par Agape V1.

La norme 2 du SEDA n'utilise plus ces types et n'est donc pas exposée à ce problème.
