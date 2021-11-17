console.log("Detect Broser.js attached successfully")

var ua = detect.parse(navigator.userAgent);
var browser = ua.browser.family;
console.log(browser)
if (browser.includes("Safari")) {
    alert("Safari can not handle our awesomeness, if you can, use Google Chrome, Firefox or Microsoft Edge")
}