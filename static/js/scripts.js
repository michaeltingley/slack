hljs.initHighlightingOnLoad();

var currentHighlightTag = null;

/**
 * Resets the selected highlight item and all highlights of currentHighlightTag.
 */
function clearHighlighting() {
  updateHighlighting('');
  $('.' + currentHighlightTag + '-tag-item').removeClass('selected-tag');
}

/**
 * Sets the selected highlight item and highlighting instances of the
 * currentHighlightTag.
 */
function updateHighlighting(color) {
  $('.tag-' + currentHighlightTag).css('background-color', color);
  $('.' + currentHighlightTag + '-tag-item').addClass('selected-tag');
}

/**
 * Restores the page state to be as if no requests had been made.
 */
function clearAll() {
  clearHighlighting();
  $('#tag-items').empty();
  $('#error').hide();
  $('#formatted_html').hide();
  $("#fetch_url_spinner").hide();
}

/**
 * Creates an html <li /> to represent a clickable tag item.
 * @param  {string} tag   Name of the tag
 * @param  {count}  count Number of occurrences of the tag
 * @param  {string} color Color to use when highlighting the tag
 */
function createTagItem(tag, count, color) {
  return $('<li />', {
    html: $('<a />', {
      class: 'tag-item ' + tag + '-tag-item',
      text: tag + ': ' + count,
      click: function() {
        clearHighlighting();
        if (currentHighlightTag == tag) {
          currentHighlightTag = null;
        } else {
          currentHighlightTag = tag;
          updateHighlighting(color);
        }
      }
    })
  });
}

/**
 * Callback when a parsed webpage is fetched from the server. Displays the
 * source and renders its clickable tag items.
 */
function onFetchedFormattedHtml(response) {
  clearAll();
  $('#formatted_html')
      .html(response.formatted_html)
      .show()
      .each(function(i, block) {
        hljs.highlightBlock(block);
      });

  $.each(response.tag_to_count, function(tag, count) {
    $('#tag-items').append(createTagItem(tag, count, 'lightblue'));
  });
}

/**
 * Callback when the server fetch for the parsed webpage fails. Displays an
 * error explaining what went wrong.
 */
function onFailedToFetchFormattedHtml(error) {
  clearAll();
  $('#error')
      .html('<strong>Error.</strong> ' + error.responseText)
      .show()
      .delay(12000)
      .fadeOut();
}

// Register the AJAX callback to perform the webpage fetch when the fetch_form
// is submitted.
$(function() {
  $('#fetch_form').submit(function(event) {
    event.preventDefault();
    clearAll();
    $("#fetch_url_spinner").show();
    $.ajax({
      type: 'POST',
      url: '/parse_url',
      data: $('#fetch_form').serialize(),
      success: onFetchedFormattedHtml,
      error: onFailedToFetchFormattedHtml
    });
  });

  $('.right-sidebar a').click(function() {
    $("#fetch_url").val($(this).text());
    $("#fetch_form").submit();
  });
});
