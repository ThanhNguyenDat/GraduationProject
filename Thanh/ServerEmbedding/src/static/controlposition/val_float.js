check_float = function (obj) {
  var re = /^-?\d*(\.\d+)?$/;
  if (!re.test(obj.value)) {
      alert("Please enter a number");
      obj.value = "";
  }
}