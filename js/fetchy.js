/*
 * wrap one level of promise & add credentials
 */

function fetchtext(url) {
  return (fetch(url, {credentials: 'include'})
  .then(function(response) {
    return response.text()
  }));
};
