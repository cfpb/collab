function collapseResults( group ) {
    var openGroup = sessionStorage.getItem( 'openGroup' );
    var dataModel = group.attr( 'data-model' );

    if ( dataModel == openGroup ) {
        return;
    }
    
    var results = group.find( 'ol' ).children( 'li' );
    if ( dataModel !== openGroup && (
         ( dataModel == 'Staff Directory' && results.length > 20 ) ||
         ( dataModel != 'Staff Directory' && results.length > 5 )
    ) ) {
        if ( dataModel == 'Staff Directory' ) {
            results.hide().slice( 0, 20 ).show();
            if ( results.length > 100 ) {
                var numMore = 80;
            } else {
                var numMore = results.length - 20;
            }
        } else {
            results.hide().slice( 0, 5 ).show();
            if ( results.length > 50 ) {
                var numMore = 45;
            } else {
                var numMore = results.length - 5;
            }
        }
        var link = $( '<a class="more_results btn" href="#">' + numMore + ' more results</a>' );
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
        $.getJSON( "{{ wiki_search_json_url }}", function( data ) {
            var results = data.query.search;
            var totalResults = data.query.searchinfo.totalhits;
            var dataModel = 'Wiki';
            var wikiGroup = $( '.results-group[data-model="Wiki"]' );
            var wikiCount = wikiGroup.find( '#wiki_count_hook' );
            var wikiList = wikiGroup.find( '#wiki_results_hook' );
            var noResult = $( '.no-results-message' );

            if ( results.length > 0 ) {
                if (totalResults > results.length) {
                    wikiCount.html( 'showing first 50 results of ' + totalResults );
                } else {
                    wikiCount.html( results.length );
                }
                wikiGroup.show();

                for ( var count = 0; count < results.length; count++ ) {
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
                noResult.show();
            };
        } );
    {% endautoescape %}
{% endif %}
 
$( '.results-group' ).each( function( i ) {
   var dataModel = $( this ).attr( 'data-model' );

   if ( dataModel !== 'Wiki' ) {
       collapseResults( $( this ) );
   }
} );
