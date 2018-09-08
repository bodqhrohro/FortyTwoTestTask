$(function() {
    var $requestsIframe = $('#requests')
    var requestsIframe = $requestsIframe.get(0)

    // update the requests iframe every 10 seconds
    var UPDATE_INTERVAL = 10
    var originalRequestsIframeLocation = requestsIframe.src
    window.setInterval(function() {
        requestsIframe.contentWindow.location = originalRequestsIframeLocation + '?from=' + Date.now()
    }, UPDATE_INTERVAL * 1000)

    // listen to visited pages counter
    var originalTitle = document.title
    window.addEventListener('message', function(e) {
        // security check
        var iframeLocation = requestsIframe.contentWindow.location
        if (
            e.origin === iframeLocation.protocol + '//' + iframeLocation.host &&
            e.data.type === 'new_requests_count'
        ) {
            if (e.data.value) {
                document.title = '(' + e.data.value + ') ' + originalTitle
            } else {
                document.title = originalTitle
            }
        }
    }, false)
})
