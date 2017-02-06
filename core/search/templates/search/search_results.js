function collapseResults( group ) {
    var openGroup = sessionStorage.getItem( 'openGroup' );
    var dataModel = group.attr( 'data-model' );

    if ( dataModel == openGroup ) {
        return;
    }
    
    var results = group.find( 'ol' ).children( 'li' );
    if ( results.length > 5 && dataModel !== openGroup ) {
        results.hide().slice( 0, 5 ).show();
        var link = $( '<a class="more_results btn" href="#">' + ( results.length - 5 ) + ' more results</a>' );
        link.click( function( e ) {
            e.preventDefault();
            results.slideDown();
            $( this ).hide();
            sessionStorage.setItem( 'openGroup', dataModel );
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
            var noResult = $( '.no-results-message' );

            if ( results.length > 0 ) {
                noResult.remove();
                wikiCount.html( results.length );
                
                var suggestedData = results[0];
                var suggestedLink = suggestedData.title.replace( ' ', '_' );
                var suggestedContent = suggestedData.snippet.replace( /<(\/)?div.*?>/gm, '' );
                var suggestedHTML = '<div class="suggested-result">';
                    suggestedHTML += '<h4>Suggested result</h4>';
                    suggestedHTML += '<a href="/wiki/index.php/' + suggestedLink + '">';
                    suggestedHTML += suggestedData.title + '</a>';
                    suggestedHTML += '<p>' + suggestedContent + '</p></div>';
                wikiList.prepend( suggestedHTML );

                for ( var count = 1; count < results.length; count++ ) {
                    var resultData = results[count];
                    var resultLink = resultData.title.replace( ' ', '_' );
                    var resultContent = resultData.snippet.replace( /<(\/)?div.*?>/gm, '' );
                    var resultHTML = '<li><a href="/wiki/index.php/' + resultLink + '">';
                        resultHTML += resultData.title + '</a>';
                        resultHTML += '<p>' + resultContent + '</p></li>';
                    wikiList.append( resultHTML );
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
