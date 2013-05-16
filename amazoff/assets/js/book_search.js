$(function() {
    // var add_book= function( isbn, url ) {
    //     $.ajax({
    //         url: url,
    //         success: function( data ) {

    //             return false;
    //         }
    //     })
    // }
    $(".book").on('click', ".add_book", function() {
        $.ajax({
            url: this.href,
            success: function( data ) {
                console.log(this);
                return false;
            }
        }) ;
        return false;
    });

    // // 콘티에서 노래 삭제
    // var del_cart= function(element, url) {
    //     $.ajax({
    //         url: url,
    //         success: function( data ) {
    //             element.fadeOut('fast', function(){
    //                 $(this).remove();
    //             });
    //             return false;
    //         }
    //     });
    // };

    // $("#empty-message").text("검색 결과가 없습니다.");
    // $( "#song_search_for_add_q" ).val("");

    // $("#conti_order").on('click', ".song_del_from_conti", function() {
    //     a_song= $(this).parents(".a_song");
    //     a_song.effect("highlight", 500);

    //     del_cart( a_song, this.href );
    //     return false;
    // });
});