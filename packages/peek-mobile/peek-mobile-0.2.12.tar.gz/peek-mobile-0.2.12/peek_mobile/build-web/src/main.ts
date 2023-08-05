import {platformBrowserDynamic} from "@angular/platform-browser-dynamic";

// Potentially enable angular prod mode
import {enableProdMode} from "@angular/core";
import {environment} from "environments/environment";

if (environment.production) {
    enableProdMode();
}

import {AppWebModule} from "./app.web.module";
platformBrowserDynamic().bootstrapModule(AppWebModule);


// This should be last
import {VortexService} from "@synerty/vortexjs";
let host = location.host.split(':')[0];
VortexService.setVortexUrl(`ws://${host}:8001/vortexws`);
