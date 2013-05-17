$(function() {
    $(".book").on('click', ".add_book", function() {
        elem = $(this);
        $.ajax({
            url: this.href,
            success: function( data ) {
                elem.after("<span class='label'>이미 저장된 책입니다</span>");
                elem.remove();
                return false;
            }
        });

        return false;
    });
});