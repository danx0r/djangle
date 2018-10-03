/*
 * wrap one level of promise & add credentials
 */

function fetchtext(url, method, data) {
  var params = {credentials: 'include'};
  if (method) {
    params.method = method;
    params.body = data;
  }
  console.log(params)
  return (fetch(url, params)
  .then(function(response) {
    return response.text()
  }));
};
