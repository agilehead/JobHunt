//NOTES:
//1. 'nofx_' Prefix: Prefix methods to be used when JS Framework is not available with nofx_ (eg: nofx_addEventListener adds an event listener without mootools support)

function nofx_goodBrowser() {
    //IE6 is the bad browser. IE7 is 'mostly' ok.
    //IE8 FF Chrome Safari are good.
    if (BrowserDetect.browser == 'Explorer' && BrowserDetect.version < 7)
        return false;
    else
        return true;
}

//Cross Browser event handling mechanism (no framework)
function nofx_addEventListener(eventName, func) {
    if (window.addEventListener) window.addEventListener(eventName, func, false);
    else if (window.attachEvent) window.attachEvent('on' + eventName, func); //4 c of < g ;)
}

//Scroll to element (no framework)
function nofx_scrollToElement(elem) {
    var x = elem.offsetLeft;
    var y = elem.offsetTop > 20 ? elem.offsetTop - 20 : elem.offsetTop;

    //To keep IE happy!
    var strScroll = 'window.scrollTo(' + x + ',' + y + ')';
    window.setTimeout(strScroll, 1);

    //  This works in all browsers except IE6 (Huh!)
    //  window.scrollTo(x, y);
}

function goBack() {
    //if there is a flashId in the referrer, take it out.
    //These are a bunch of hacks!!!
    //var ref = document.referrer;
    //ref = ref.replace(/flashId=[a-zA-Z0-9_-]*/, 'bbRet=true');
    //window.location.href = ref;
    window.history.back(-1);
}

/* === AlertBox class ===
    NOTES: AlertBox cannot use mootools since it may be used in pages where mootools is not loaded.
    So, use DOM selector APIs, instead of $ and $$; Cannot use 'Class' either. */

function AlertBox(){
    this.flashMessages = [];
}

AlertBox.prototype.register = function(message) {
    this.flashMessages.push(message);
}

AlertBox.prototype.displayMessage = function(message) {
    //clear existing messages and display just this.
    this.flashMessages = [];
    this.flashMessages.push(message);
    this.activate();
}

AlertBox.prototype.clear = function() {
    //clear existing messages and display just this.
    this.flashMessages = [];
    this.hide();
}

AlertBox.prototype.hasMessages = function() {
    return this.flashMessages.length != 0;
}

AlertBox.prototype.activate = function() {
    alerts.initted = true; //if activate is called, it means alerts have been initted.

    var eBox = document.getElementById('alertBox');
    //Some pages may not have the alertBox
    //or there may not be any messages
    if (eBox == null || this.flashMessages.length == 0) {
	this.hide();
    } else {
	eBox.className = 'visible';
        eBox.innerHTML = '<ul id="alertBoxItems"></ul>';
        var eBoxItems = document.getElementById('alertBoxItems');
        var html = '';
        for (var i = 0; i < this.flashMessages.length; i++) {
            html += '<li>' + this.flashMessages[i] + '</li>';
        }
        this.flashMessages = []; //Once we show the messages, clear the list.
        eBoxItems.innerHTML = html;

        nofx_scrollToElement(eBox);
    }
}

AlertBox.prototype.hide = function() {
    var eBox = document.getElementById('alertBox');
    if (eBox != null)
	eBox.className = 'invisible';
}
/* === AlertBox class === */

/* === BrowserDetect class === */
var BrowserDetect = {
    init: function() {
        this.browser = this.searchString(this.dataBrowser) || "An unknown browser";
        this.version = this.searchVersion(navigator.userAgent)
			|| this.searchVersion(navigator.appVersion)
			|| "an unknown version";
        this.OS = this.searchString(this.dataOS) || "an unknown OS";
    },
    searchString: function(data) {
        for (var i = 0; i < data.length; i++) {
            var dataString = data[i].string;
            var dataProp = data[i].prop;
            this.versionSearchString = data[i].versionSearch || data[i].identity;
            if (dataString) {
                if (dataString.indexOf(data[i].subString) != -1)
                    return data[i].identity;
            }
            else if (dataProp)
                return data[i].identity;
        }
    },
    searchVersion: function(dataString) {
        var index = dataString.indexOf(this.versionSearchString);
        if (index == -1) return;
        return parseFloat(dataString.substring(index + this.versionSearchString.length + 1));
    },
    dataBrowser: [
		{
		    string: navigator.userAgent,
		    subString: "Chrome",
		    identity: "Chrome"
		},
		{ string: navigator.userAgent,
		    subString: "OmniWeb",
		    versionSearch: "OmniWeb/",
		    identity: "OmniWeb"
		},
		{
		    string: navigator.vendor,
		    subString: "Apple",
		    identity: "Safari",
		    versionSearch: "Version"
		},
		{
		    prop: window.opera,
		    identity: "Opera"
		},
		{
		    string: navigator.vendor,
		    subString: "iCab",
		    identity: "iCab"
		},
		{
		    string: navigator.vendor,
		    subString: "KDE",
		    identity: "Konqueror"
		},
		{
		    string: navigator.userAgent,
		    subString: "Firefox",
		    identity: "Firefox"
		},
		{
		    string: navigator.vendor,
		    subString: "Camino",
		    identity: "Camino"
		},
		{		// for newer Netscapes (6+)
		    string: navigator.userAgent,
		    subString: "Netscape",
		    identity: "Netscape"
		},
		{
		    string: navigator.userAgent,
		    subString: "MSIE",
		    identity: "Explorer",
		    versionSearch: "MSIE"
		},
		{
		    string: navigator.userAgent,
		    subString: "Gecko",
		    identity: "Mozilla",
		    versionSearch: "rv"
		},
		{ 		// for older Netscapes (4-)
		    string: navigator.userAgent,
		    subString: "Mozilla",
		    identity: "Netscape",
		    versionSearch: "Mozilla"
		}
	],
    dataOS: [
		{
		    string: navigator.platform,
		    subString: "Win",
		    identity: "Windows"
		},
		{
		    string: navigator.platform,
		    subString: "Mac",
		    identity: "Mac"
		},
		{
		    string: navigator.platform,
		    subString: "Linux",
		    identity: "Linux"
		}
	]

};
BrowserDetect.init();
/* === BrowserDetect class === */

var alerts = new AlertBox();
alerts.initted = false;

function __onStartup() {
	//if already initted then don't bother.
	if (!alerts.initted)
		alerts.activate();
}

//Fire onStartup when the page loads.
nofx_addEventListener('load', __onStartup, false);

///Common string functions
function trim(str, chars) {
    return ltrim(rtrim(str, chars), chars);
}

function ltrim(str, chars) {
    chars = chars || "\\s";
    return str.replace(new RegExp("^[" + chars + "]+", "g"), "");
}

function rtrim(str, chars) {
    chars = chars || "\\s";
    return str.replace(new RegExp("[" + chars + "]+$", "g"), "");
}