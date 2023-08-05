// this import should be first in order to load some required settings (like globals and reflect-metadata)
import {platformNativeScriptDynamic} from "nativescript-angular/platform";

import {PeekCoreConfigService} from "@synerty/peek-web-ns/index.nativescript";
PeekCoreConfigService.PLATFORM_TARGET = PeekCoreConfigService.PLATFORMS.MOBILE_NATIVE;


import "nativescript-websockets";
import "nativescript-localstorage";
import 'rxjs/add/operator/filter';
import 'moment';

// Set the URL for the vortex
import {VortexService} from "@synerty/vortexjs";
// let host = location.host.split(':')[0];
let host = '10.2.56.17';
VortexService.setVortexUrl(`ws://${host}:8001/vortexws`);
// VortexService.setVortexUrl(`http://${host}:8000/vortex`);

// Import some stuff that we need
import "@synerty/vortexjs";
// import "nativescript-angular";

// // Potentially enable angular prod mode
// import {enableProdMode} from "@angular/core";
// import {environment} from "../src/environments/environment";
//
// if (environment.production) {
//     enableProdMode();
// }



// This should be last
import {AppNsModule} from "./app.ns.module";
platformNativeScriptDynamic().bootstrapModule(AppNsModule);
