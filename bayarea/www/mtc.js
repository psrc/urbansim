
hudsonURL = 'http://paris.urbansim.org:8080/hudson/job/MTC_Model'

function createXMLHttpRequest() {
  var xmlHttp = false;
  if(window.ActiveXObject) {
    xmlhttp = new ActiveXObject('Microsoft.XMLHTTP');
  } else if(window.XMLHttpRequest) {
    xmlhttp = new XMLHttpRequest();
  } else {
    alert('Your browser is not supported.');
  }
  return xmlhttp;
}

function getBuildNumber(buildURL, callback) {
  // We must user our own XMLHttpRequest because we want to parse data as it
  // comes in.  The reason for this is that the raw console log is often HUGE,
  // so we want to abort after detecting the urbansim build number.
  var xmlhttp = createXMLHttpRequest();
  xmlhttp.onreadystatechange = function() {
	if (xmlhttp.readyState == 3 && xmlhttp.responseText.length > 128*1024) {
      // give up if the first 128kB of text don't have what we're looking for
	  xmlhttp.abort();
      if (callback != null) {
        callback(-1);
      }
    } else if (xmlhttp.readyState == 3) {
      // if this run was a new run, we'll see the line where the cache
      // directory was created.
	  var magicString = 'Cache directory for run ';
	  var i = xmlhttp.responseText.indexOf(magicString);
      if (i < 0) {
        // if this run was a re-launch, we rely on the HUDSON_RESTART_RUN
        // environment var
        magicString = 'HUDSON_RESTART_RUN=';
	    i = xmlhttp.responseText.indexOf(magicString);
        if (i < 0)
          return;
      }
	  i = i + magicString.length;
	  urbansimNumber = xmlhttp.responseText.substring(i, i + 20).split('\n')[0].split(' ')[0];
	  xmlhttp.abort();
	  console.log('Found urbansim run number ' + urbansimNumber);
      if (callback != null)
        callback(urbansimNumber);
	}
  };
  xmlhttp.open('GET', buildURL + '/consoleText', true);
  xmlhttp.send(null);
}

function getBuild(buildURL, callback) {
  getBuildNumber(buildURL, function (urbansimNumber) {
    url = buildURL + '/api/json';
    $.getJSON(url, null, function(build) {
      build.urbansimNumber = urbansimNumber;
      callback(build);
    });
  });
}

function addBuild(build) {
  var status = build.result;
  if (build.building)
    status = 'RUNNING';

  e = $('#run' + build.urbansimNumber + " .hudsonNumber");
  if (e.length != 0 && e.text() > build.number) {
	console.log("It appears that " + build.number + " is an older build for run " + build.urbansimNumber);
	return;
  }
  html = '<a href="' + build.url + 'console">Run #' + build.urbansimNumber + '</a>: ' +
	'<span class="hudsonNumber" style="display:none">' + build.number + '</span>' +
	'<span id="status">' + status + '</span>'
  if (e.length != 0)
	$('#run' + build.urbansimNumber).html(html);
  else
	$('#builds').append('<li id=run' + build.urbansimNumber + '>' + html + '<li>');
}

function getBuilds() {
  getBuild(hudsonURL + '/lastBuild', function(build) {
    addBuild(build);
    var newest = Math.max(build.number-1, 0);
    var oldest = Math.max(newest-20, 0);
    for (i=newest; i>oldest; i--) {
      getBuild(hudsonURL + '/' + i, addBuild);
    }
  });
}

$(function() {
  getBuilds();
});
