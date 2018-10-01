/*
 * wrap one level of promise & add credentials
 */

function fetchtext(url, func) {
  return (fetch(url, {credentials: 'include'})
  .then(function(response) {
    return response.text()
  }));
};
