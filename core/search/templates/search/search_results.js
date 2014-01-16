{% if wiki_installed %}
    {% autoescape off %}
        $.getJSON('{{ wiki_search_json_url }}', function(data) {
            results = data.query.search;

            if (results.length > 0) {
                $("#wiki_count_hook").html(results.length);

                var count = 0;

                for (count = 0; count < results.length; count++) {
                    var link = results[count].title.replace(' ', '_');
                    var html = '<li><a href="/wiki/index.php/' + link + '">';
                    html += results[count].title;
                    html += '</a> <br/>';
                    html += results[count].snippet
                            .replace(/<(\/)?div.*?>/gm, '')
                            .replace(/<(\/)?span.*?>/gm, "<$1b>");
                    html += '</li>';
                    $("#wiki_results_hook").append(html);
                }
                collapse_results()
            } else {
                $('.results-group[data-model="Wiki"]').hide();
                $('#filterWiki').parent('li').hide();
            };
        });
    {% endautoescape %}
{% endif %}

function collapse_results() {
    $('.results-group').each(function(i) {
        var results = $(this).find("ol").children("li");
        if (results.length > 2) {
            results.hide().slice(0, 2).show();
            var link = $("<a class=\"more_results btn\" href=\"#\">" + (results.length - 2) + " More results</a>");
            link.click(function(e) {
                e.preventDefault();
                results.slideDown();
                $(this).hide();
            });
            $(this).children(".more_results").remove();
            $(this).append(link);
        }
        
    });
}


$('.search-checkbox').change(function() {
    $('.results-group[data-model="' + $(this).val() + '"]').slideToggle();
})

collapse_results()
