function open_contact_detail(card) {
    var powers_list,
        data = card.data(),
        powers = data.powers.split(','),
        contact_display = $('#contact_display');

    contact_display.find('.title').text(data.code_name);
    contact_display.find('.full_name .detail').text(data.full_name);

    powers_list = '<ul class="powers">';
    for (var power_index in powers) {
        powers_list += '<li>' + powers[power_index] + '</li>';
    }
    powers_list += '</ul>';

    contact_display.find('.powers .detail').html(powers_list);
    contact_display.find('.big_avatar').html(card.find('.big_avatar').html());

    if (data.email !== '') {
        contact_display.find('button.email').removeClass('hidden');
    } else {
        contact_display.find('button.email').addClass('hidden');
    }

    if (data.telephone_number !== '') {
        contact_display.find('button.telephone_number').removeClass('hidden');
    } else {
        contact_display.find('button.telephone_number').addClass('hidden');
    }

    $('#contact_display').data.active = true;
    $('#contact_display').data.active_contact = data.code_name;
    $('#contact_update_link').attr('href', data.update_url);
    $('#contact_delete_link').attr('href', data.delete_url);
    $('#contact_display').removeClass('hidden');
    $('#contact_list').css('width', '60%');
    $('#power_grade_overlay').css('width', data.grade + '%');
}

function close_contact_detail() {
    $('#contact_display').data.active = false;
    $('#contact_display').data.active_contact = '';
    $('#contact_display').addClass('hidden');
    $('#contact_list').css('width', '100%');
}

function toggle_contact_display(card) {
    var data = card.data(),
        contact_display_visible = $('#contact_display').data.active === true,
        same_contact_requested = $('#contact_display').data.active_contact === data.code_name;
    if (contact_display_visible && same_contact_requested) {
        close_contact_detail();
    } else {
        open_contact_detail(card);
    }
}

$(function() {
    $('.highlight_card').on('click', function() {
        toggle_contact_display($(this));
    });
});
