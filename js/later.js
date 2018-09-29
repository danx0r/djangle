function later(url, func) {
  fetch(url, {credentials: 'include'})
  .then(function(response) {
    response.text()
    .then(func);
  });
};
