/*
 * veripeditus-web - Web frontend to the veripeditus server
 * Copyright (C) 2016, 2017  Dominik George <nik@naturalnet.de>
 * Copyright (C) 2017  Eike Tim Jesinghaus <eike@naturalnet.de>
 * Copyright (c) 2017  mirabilos <thorsten.glaser@teckids.org>
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Affero General Public License as published
 * by the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version, with the Game Cartridge Exception.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU Affero General Public License for more details.
 *
 * You should have received a copy of the GNU Affero General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */

// Utility code for logging
function log_debug(msg) {
    if (Veripeditus.debug) {
        console.log(msg);
    }
}

Veripeditus = {
    version: '1.0.0a3',
    views: [],
    services: [],
    registerView: function (view) {
        log_debug("Registering view " + view.name + ".");

        this.views.push(view);
        view.deactivate();
        if (!this.currentView) {
            this.currentView = view;
            view.activate();
        }
        var i = this.views.indexOf(this.currentView);
        i++;
        if (i == this.views.length) {
            i = 0;
        }
        $("#control-view img").attr("src", "img/ui/btn-" + this.views[i].name + ".svg");
        this.registerService(view);
    },
    registerService: function (service) {
        log_debug("Registering service " + service.name + ".");

        this.services.push(service);
    },
    nextView: function () {
        var i = this.views.indexOf(this.currentView);
        i++;
        if (i == this.views.length) {
            i = 0;
        }
        this.currentView.deactivate();
        this.currentView = this.views[i];
        this.currentView.activate();
        i++;
        if (i == this.views.length) {
            i = 0;
        }
        $("#control-view img").attr("src", "img/ui/btn-" + this.views[i].name + ".svg");
    },
    currentView: undefined,
    debug: false
};

if (window.URLSearchParams) {
    var search_param = '' + window.location.search;
    var params = new URLSearchParams(search_param.replace(/^\?/, ''));
    if (params.get("debug") == "true") {
        Veripeditus.debug = true;
    }
}
