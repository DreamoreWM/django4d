(function($) {
    $(document).ready(function() {
        // Initialiser l'autocomplétion sur le champ adresse_intervention
        $("#id_adresse_intervention").autocomplete({
            source: function(request, response) {
                $.ajax({
                    url: "https://api-adresse.data.gouv.fr/search/",
                    dataType: "json",
                    data: {
                        q: request.term,  // Terme saisi par l'utilisateur
                        limit: 10,        // Limite de résultats
                    },
                    success: function(data) {
                        // Traiter les résultats de l'API
                        response($.map(data.features, function(item) {
                            return {
                                label: item.properties.label,  // Adresse complète
                                value: item.properties.label,  // Valeur à insérer dans le champ
                            };
                        }));
                    }
                });
            },
            minLength: 3,  // Nombre minimum de caractères avant de lancer une recherche
        });
    });
})(jQuery);