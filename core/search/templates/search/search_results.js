function collapseResults( group ) {
    var results = $( group ).find( 'ol' ).children( 'li' );
    if ( results.length > 5 ) {
        results.hide().slice( 0, 5 ).show();
        var link = $( '<a class="more_results btn" href="#">' + ( results.length - 5 ) + ' More results</a>' );
        link.click( function( e ) {
            e.preventDefault();
            results.slideDown();
            $( this ).hide();
        } );
        $( group ).append( link );
    }
}

{% if wiki_installed %}
    {% autoescape off %}
        $.getJSON( '{{ wiki_search_json_url }}', function( data ) {
            var results = data.query.search;
            var dataModel = 'Wiki';
            var wikiGroup = $( '.results-group[data-model="Wiki"]' );
            var wikiCount = wikiGroup.find( '#wiki_count_hook' );
            var wikiList = wikiGroup.find( '#wiki_results_hook' );

            if ( results.length > 0 ) {
                wikiCount.html( results.length );

                for ( var count = 0; count < results.length; count++ ) {
                    var link = results[count].title.replace( ' ', '_' );
                    var html = '<li><a href="/wiki/index.php/' + link + '">';
                    html += results[count].title;
                    html += '</a> <br/>';
                    html += results[count].snippet
                            .replace( /<(\/)?div.*?>/gm, '' )
                            .replace( /<(\/)?span.*?>/gm, "<$1b>" );
                    html += '</li>';
                    wikiList.append( html );
                }
                collapseResults( wikiGroup );
            } else {
                wikiGroup.hide();
            };
        } );
    {% endautoescape %}
{% endif %}
 
$( '.results-group' ).each( function( i ) {
   var dataModel = $( this ).attr( 'data-model' );

   if ( dataModel !== 'Wiki' ) {
       collapseResults( this );
   }
} );
