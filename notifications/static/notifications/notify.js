var notify_badge_class;
var notify_menu_class;
var notify_api_url;
var notify_fetch_count;
var notify_unread_url;
var notify_mark_all_unread_url;
var notify_refresh_period = 15000;
var consecutive_misfires = 0;
var registered_functions = [];

var options = {
    weekday: "long",
    year: "numeric",
    month: "long",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit"
};

function parseISOString(s) {
    var b = s.split(/\D+/);
    return new Date(Date.UTC(b[0], --b[1], b[2], b[3], b[4], b[5], b[6]));
}

function fill_notification_badge(data) {
    var badges = document.getElementsByClassName(notify_badge_class);
    if (badges) {
        for (var i = 0; i < badges.length; i++) {
            if (data.unread_count > 0) {
                badges[i].innerHTML = data.unread_count;
            } else {
                badges[i].innerHTML = '';
            }
        }
    }
}

function fill_notification_list(data) {
    var menus = document.getElementsByClassName(notify_menu_class);
    if (menus) {
        var messages = data.all_list.map(function (item) {
            var message = "";
            let str = "";
            let _time = "";
            if (typeof item.verb !== 'undefined') {
                message = message + " " + item.verb;
            }
            if (typeof item.target !== 'undefined') {
                message = message + " " + item.target;
            }
            if (typeof item.timestamp !== 'undefined') {
                _time = parseISOString(item.timestamp).toLocaleDateString("vi", options);
            }
            str = `<a class="dropdown-item d-flex align-items-center" href="javascript:;">`;
            str += `<div class="mr-3"><div class="icon-circle bg-primary-2"><i class="fas fa-rss text-white"></i></div></div>`;
            str += `<div>`;
            str += `<div class="small text-gray-500">` + _time + `</div>`;
            str += message;
            str += `</div>`;
            return str;
        }).join('')

        for (var i = 0; i < menus.length; i++) {
            menus[i].innerHTML = messages;
        }
    }
}

function register_notifier(func) {
    registered_functions.push(func);
}

function fetch_api_data() {
    if (registered_functions.length > 0) {
        //only fetch data if a function is setup
        var r = new XMLHttpRequest();
        r.addEventListener('readystatechange', function (event) {
            if (this.readyState === 4) {
                if (this.status === 200) {
                    consecutive_misfires = 0;
                    var data = JSON.parse(r.responseText);
                    registered_functions.forEach(function (func) {
                        func(data);
                    });
                } else {
                    consecutive_misfires++;
                }
            }
        })
        r.open("GET", notify_api_url + '?max=' + notify_fetch_count, true);
        r.send();
    }
    if (consecutive_misfires < 10) {
        setTimeout(fetch_api_data, notify_refresh_period);
    } else {
        var badges = document.getElementsByClassName(notify_badge_class);
        if (badges) {
            for (var i = 0; i < badges.length; i++) {
                badges[i].innerHTML = "!";
                badges[i].title = "Connection lost!"
            }
        }
    }
}

setTimeout(fetch_api_data, 1000);
