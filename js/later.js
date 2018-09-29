function later(url, func) {
  var f1=fetch("/criv1/version", {credentials: 'include'})
  console.log("f1:", f1)
  f1.then(function(response) {
    var t1=response.text()
    console.log("t1:", t1)
    t1.then(func);
  });
};
