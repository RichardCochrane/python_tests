function toggle_contact_display(data) {
    var contact_display_visible = $('#contact_display').data.active === true,
        same_contact_requested = $('#contact_display').data.active_contact === data.codename;
    if (contact_display_visible && same_contact_requested) {
        $('#contact_display').data.active = false;
        $('#contact_display').data.active_contact = '';
        $('#contact_display').addClass('hidden');
        $('#contact_list').css('width', '100%');
    } else {
        var contact_display = $('#contact_display');
        contact_display.find('.title').text(data.codename);
        contact_display.find('.full_name').text(data.full_name);
        contact_display.find('.powers').text(data.powers);

        $('#contact_display').data.active = true;
        $('#contact_display').data.active_contact = data.codename;
        $('#contact_display').removeClass('hidden');
        $('#contact_list').css('width', '60%');
    }
}

$(function() {
    $('.highlight_card').on('click', function() {
        toggle_contact_display($(this).data());
    });
});
