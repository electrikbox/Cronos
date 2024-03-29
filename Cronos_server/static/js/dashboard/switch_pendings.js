/**
 * This script handles the functionality of switching pending cron statuses on the dashboard page.
 * It makes an AJAX request to retrieve the pending cron data from the server and updates the UI accordingly.
 * The script uses jQuery for DOM manipulation and AJAX requests.
 *
 * @requires jQuery
 */

$(document).ready(function () {
  let intervalId;

  const access_token = localStorage.getItem('access_token');

  function refreshAccessToken() {
    const refreshToken = localStorage.getItem('refresh_token');

    if (!refreshToken) {
      console.error('No refresh token found in local storage');
      return;
    }

    $.ajax({
      url: '/api/token/refresh/',
      type: 'POST',
      data: { refresh: refreshToken },
      success: function (response) {
        const newAccessToken = response.access;
        localStorage.setItem('access_token', newAccessToken);
        console.log('New access token obtained:', newAccessToken);
      },
      error: function (xhr, status, error) {
        alert('Please login again');
        window.location.href = "/accounts/logout/?next=/dashboard/"; // <------- redirect to login page
      }
    });
  }

  /**
   * Validates and updates the status of a pending cron
   * @param {number} index - The index of the pending cron to validate
   */
  function validate(index) {
    const pendingDiv = $(`.pending:eq(${index})`);
    const paragraph = pendingDiv.find('p');
    pendingDiv.addClass('active').removeClass('pending');
    paragraph.text('Active');
  }

  /**
   * Rejects the specified crons based on the filtered response
   * Removes the corresponding cron elements from the DOM
   *
   * Delete cron from dashboard if it can't be executed on the user's computer
   *
   * @param {Array<number>} crons - The array of cron IDs to reject
   * @param {Array<Object>} filteredResponse - The filtered response containing cron objects
   * @returns {void}
   */
  function reject(crons, filteredResponse) {
    const notFoundCrons = crons.filter(cronId => !filteredResponse.some(cron => cron.id === cronId));
    notFoundCrons.forEach(cronId => {
      const pendingDiv = $(`.pending[data-cron-id='${cronId}']`);
      const cronFull = pendingDiv.closest('.cron-full');
      alert(`Command from cron ${cronId} can't be executed\non your computer. It will be deleted`);
      cronFull.remove();
    });
  }

  /**
   * Switches the pending status of crons by making an AJAX request to the server
   * If a cron is validated, its corresponding HTML element is updated to show "Active"
   * If there are no more pending crons, the interval for checking pending status is cleared
   */
  function switchPendingStatus() {

    $.ajax({
      url: `/api/crons/`,
      type: 'GET',
      headers: {
        'Authorization': `Bearer ${access_token}`
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
        alert('Please login again');
        window.location.href = "/accounts/logout/?next=/dashboard/"; // <------- redirect to login page
      }
    });
  }

  /**
   * Checks if there are any pending elements on the page and starts a timer to switch their status
   */
  function checkPendingsOnPage() {
    if ($('.pending').length > 0) {
      intervalId = setInterval(switchPendingStatus, 5000); // <------- check every 5 seconds
    }
  }

  /**
   * Retrieves the IDs of the pending crons
   * @returns {Array<number>} An array of cron IDs
   */
  function getPendingsCrons() {
    const selectedCronIds = [];
    $('.pending').each(function () {
      const cronId = $(this).closest('.cron-full').find('.pause-cron').data('cron-id');
      selectedCronIds.push(cronId);
    });
    return selectedCronIds;
  }

  setTimeout(checkPendingsOnPage, 500); // <------- stop after 0.5 seconds
});
