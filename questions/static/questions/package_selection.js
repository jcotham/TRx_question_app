
var currently_selected_item;


// Should be executed anytime user navigates away from page
// and wishes their changes should be saved
function save_order(target_url) {
	var used_ids = []


	// is the following definitely in the right order?
	// maybe not, because of javascript asynchronous functions.
	// Is there an each method for only the first match?
	// Or some method that implies only one match exists?
	$('#stack li').each(function(i){
		if ($(this).attr('chain_id') !== undefined) {
			used_ids.push( $(this).attr('chain_id') )
		}
	});

	// Couldn't get the following to work. Should have
	// been sorted, though.
//	user_ids = $('#stack').sortable('serialize')

	var dict = {"used_ids": used_ids}

	$.ajax({
		data: dict,
		type: 'POST',
		url: target_url,
	});

	return false; // to prevent page redirection
}


// Hackish, and doesn't really separate controller from view.
// Would be better if unselected color and selected color were
// stored in variables that were referenced by both the css and this
function update_selected(new_selected) {
	if (currently_selected_item !== undefined && currently_selected_item !== new_selected) {
		currently_selected_item.style.backgroundColor = 'grey';
	}

	currently_selected_item = new_selected;
	currently_selected_item.style.backgroundColor = 'green';
}


function redirect_to_edit_page(target_url, form_source) {
	if (currently_selected_item !== undefined) {
		form_source.action = target_url+(currently_selected_item.attributes["chain_id"].value)
		console.log(form_source.action);
		return true;
	} else {
		return false;
	}

	/*
	if (currently_selected_item !== undefined) {
		$.ajax({
			type: 'GET',
			url: target_url+(currently_selected_item.attributes["chain_id"].value)
		});
	}
	*/
}

/*
// Saves used_chains whenever something changes
$('#stack').sortable({
    axis: 'y',
    stop: function (event, ui) {
        var data = $(this).sortable('serialize');

        // POST to server using $.post or $.ajax
        $.ajax({
            data: data,
            type: 'POST',
            url: '/your/url/here'
        });
    }
});
*/


