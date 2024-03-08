/**
 * This script handles the functionality of switching pending cron statuses on the dashboard page.
 * It makes an AJAX request to retrieve the pending cron data from the server and updates the UI accordingly.
 * The script uses jQuery for DOM manipulation and AJAX requests.
 *
 * @requires jQuery
 */

$(document).ready(function () {
  let intervalId;

  /**
   * Validates and updates the status of a pending item.
   * @param {number} index - The index of the pending item to validate.
   */
  function validate(index) {
    const pendingDiv = $(`.pending:eq(${index})`);
    const paragraph = pendingDiv.find('p');
    pendingDiv.addClass('active').removeClass('pending');
    paragraph.text('Active');
  }

  /**
   * Rejects the specified crons based on the filtered response.
   * Removes the corresponding cron elements from the DOM.
   *
   * @param {Array<number>} crons - The array of cron IDs to reject.
   * @param {Array<Object>} filteredResponse - The filtered response containing cron objects.
   * @returns {void}
   */
  function reject(crons, filteredResponse) {
    const notFoundCrons = crons.filter(cronId => !filteredResponse.some(cron => cron.id === cronId));
    notFoundCrons.forEach(cronId => {
      const pendingDiv = $(`.pending[data-cron-id='${cronId}']`);
      const cronFull = pendingDiv.closest('.cron-full');
      alert(`Command from cron ${cronId} can't be executed\non your computer. It will be deleted.`);
      cronFull.remove();
    });
  }

  /**
   * Switches the pending status of crons by making an AJAX request to the server.
   * If a cron is validated, its corresponding HTML element is updated to show "Active".
   * If there are no more pending crons, the interval for checking pending status is cleared.
   */
  function switchPendingStatus() {
    const cookies = document.cookie.split('; ');
    const accessToken = cookies[4].split(':')[2];
    const accessTokenWithoutLastThree = accessToken.substring(2, accessToken.length - 3);

    $.ajax({
      url: `/api/crons/`,
      type: 'GET',
      headers: {
        'Authorization': `Bearer ${accessTokenWithoutLastThree}`
      },
      success: function (response) {
        const crons = getPendingsCrons();
        const filteredResponse = response.filter(cron => crons.includes(cron.id));
        let hasPending = false;
        filteredResponse.forEach((cron, index) => {
          if (cron.validated) {
            validate(index);
          } else {
            hasPending = true;
          }
        });
        if (crons.some(cronId => !filteredResponse.some(cron => cron.id === cronId))) {
          reject(crons, filteredResponse);
          window.location.href = "/dashboard";
        }
        if (!hasPending) {
          clearInterval(intervalId);
        }
      },
      error: function (xhr) {
        console.error('Failed to get users status:', xhr.status, xhr.responseText);
      }
    });
  }

  /**
   * Checks if there are any pending elements on the page and starts a timer to switch their status.
   */
  function checkPendingsOnPage() {
    if ($('.pending').length > 0) {
      intervalId = setInterval(switchPendingStatus, 5000);
    }
  }

  /**
   * Retrieves the IDs of the pending crons.
   * @returns {Array<number>} An array of cron IDs.
   */
  function getPendingsCrons() {
    const selectedCronIds = [];
    $('.pending').each(function () {
      const cronId = $(this).closest('.cron-full').find('.pause-cron').data('cron-id');
      selectedCronIds.push(cronId);
    });
    return selectedCronIds;
  }

  setTimeout(checkPendingsOnPage, 500);
});
