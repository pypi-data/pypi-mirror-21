/* global Sortable maxWinners urlResults */
/* exported addChoice deleteChoice submitPoll toggleExpand */

const message = document.querySelector('#message-toast');

/*
 * Enable dragging choices around
 */
Sortable.create(document.getElementById('source-box'), {
  animation: 150,
  handle: '.active-option',
  group: {
    name: 'ballot',
  },
  sort: false,
});

Sortable.create(document.getElementById('dest-box'), {
  animation: 150,
  handle: '.active-option',
  group: {
    name: 'ballot',
    put: function(to) {
      if (typeof maxWinners != 'undefined') {
        return to.el.children.length < maxWinners;
      } else {
        return true;
      }
    },
  },
  sort: true,
});

/**
 * Toggle the expanded status of a candidate
 * @param {Element} element - The element to toggle
 */
function toggleExpand(element) {
  let expand = $(element).hasClass('selected-option');
  $('.option').removeClass('selected-option');
  if(!expand) {
    $(element).addClass('selected-option');
  }
}

/**
 * Collect the choices and submit them to the backend
 */
function submitPoll() {
  let ballot = [];
  let csrfToken = $.cookie('csrftoken');
  let i = 0;
  $('#dest-box').find('input').each(function() {
    ballot[i++] = $(this).val();
  });
  let data = {
    'csrfmiddlewaretoken': csrfToken,
    'data': JSON.stringify(ballot),
  };
  $.post($(location).attr('href'), data, function(response) {
    window.location.href = urlResults;
  })
    .fail(function(jqXHR) {
      if (jqXHR.status == 400) {
        message.MaterialSnackbar.showSnackbar({message: jqXHR.responseText});
      } else {
        message.MaterialSnackbar.showSnackbar({message: 'An error occured.'});
      }
    });
}
