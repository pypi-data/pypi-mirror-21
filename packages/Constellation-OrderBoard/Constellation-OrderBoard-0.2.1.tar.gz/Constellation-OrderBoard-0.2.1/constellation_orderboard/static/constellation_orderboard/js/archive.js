/* global Handlebars componentHandler board_id url_api_v1_board_archived_cards
url_api_v1_card_unarchive */
/* exported restoreItem */

var message = document.querySelector('#message-toast');

/* Global board state */
var archive_data;

/* Template for Handlebars to execute */
var source = $('#handlebars-board').html();

$(document).ready(function(){
  /* Start templating */
  getboard_data();
});

/* Call APIs to get the JSON board_data */
function getboard_data() {
  /* Get the list of stages */
  var url = url_api_v1_board_archived_cards.replace(0, board_id);
  $.getJSON(url, function(cards){
    archive_data = {cards: []};
    for (var i = 0, len = cards.length; i < len; i++) {
      archive_data.cards.push({
        name: cards[i].fields.name,
        id: cards[i].pk,
        notes: cards[i].fields.notes,
        quantity: cards[i].fields.quantity,
      });
    }
    renderTemplate(archive_data);
  })
    .fail(function(jqXHR) {
      if (jqXHR.status == 404) {
        message.MaterialSnackbar.showSnackbar({message: jqXHR.responseText});
      } else {
        message.MaterialSnackbar.showSnackbar({message: 'An error occured.'});
      }
    });
}

/* render compiled handlebars template */
function renderTemplate(archive_data){
  var template = Handlebars.compile(source);
  $('#board').html(template(archive_data));
  /* Make MDL re-register progress-bars and the like */
  componentHandler.upgradeDom();
}

/* Remove a card from the board */
function restoreItem(id) {
  $('#card_' + id + '_progress').show();
  $.get(url_api_v1_card_unarchive.replace(0, id), function(){
    var card_index = archive_data.cards.findIndex(function(element){
      return element.id == id;
    });
    archive_data.cards.splice(card_index, 1);
    $('#card_' + id).effect('scale', {percent: 0}, 100, function(){
      renderTemplate(archive_data);
    });
  })
    .fail(function(jqXHR) {
      if (jqXHR.status == 500) {
        message.MaterialSnackbar.showSnackbar({message: jqXHR.responseText});
      } else {
        message.MaterialSnackbar.showSnackbar({message: 'An error occured.'});
      }
    });
}
