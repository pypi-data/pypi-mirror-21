import {NgModule, NgModuleFactoryLoader, NO_ERRORS_SCHEMA} from "@angular/core";
import {CommonModule} from "@angular/common";
import {NativeScriptModule} from "nativescript-angular/platform";
import {NativeScriptFormsModule} from "nativescript-angular/forms";
import {NativeScriptRouterModule} from "nativescript-angular";
// @synerty
import {
    DeviceInfoNsService,
    DeviceInfoService,
    PeekModuleFactory
} from "@synerty/peek-web-ns/index.nativescript";
import {PeekModuleFactoryLoader} from "./module-loader.ns.factory";
import {
    TupleDataObservableNameService,
    TupleDataObserverService,
    TupleDataOfflineObserverService,
    TupleOfflineStorageNameService,
    TupleOfflineStorageService,
    WebSqlFactoryService
} from "@synerty/vortexjs";
import {WebSqlNativeScriptFactoryService} from "@synerty/vortexjs/index-nativescript";
// Routes
import {staticRoutes} from "./app/app.routes";
// Providers
import {peekRootServices} from "./app/app.services";
// Components
import {AppComponent} from "./app/app.component";
import {MainHomeComponent} from "./app/main-home/main-home.component";
import {MainTitleComponent} from "./app/main-title/main-title.component";
import {UnknownRouteComponent} from "./app/unknown-route/unknown-route.component";
import {pluginRootModules} from "./plugin-root-modules";
import {pluginRootServices} from "./plugin-root-services";

// Add FontAwesome
import {TNSFontIconModule, TNSFontIconService} from "nativescript-ngx-fonticon";
// turn debug on
TNSFontIconService.debug = false;

@NgModule({
    declarations: [AppComponent,
        MainTitleComponent,
        MainHomeComponent,
        UnknownRouteComponent],
    bootstrap: [AppComponent],
    imports: [
        CommonModule,
        NativeScriptModule,
        NativeScriptFormsModule,
        NativeScriptRouterModule,
        PeekModuleFactory.RouterModule.forRoot(staticRoutes),
        ...pluginRootModules,
        TNSFontIconModule.forRoot({
            'fa': './assets/font-awesome.min.css'
        })
    ],
    schemas: [NO_ERRORS_SCHEMA],
    providers: [
        {provide: NgModuleFactoryLoader, useClass: PeekModuleFactoryLoader},
        {provide: WebSqlFactoryService, useClass: WebSqlNativeScriptFactoryService},
        ...peekRootServices,
        ...pluginRootServices,

        // Use the TupleDataObserver services, with offline storage
        {
            provide: TupleDataObservableNameService,
            useValue: new TupleDataObservableNameService(
                "peek_client", {"plugin": "peek_client"})
        }, {
            provide: TupleOfflineStorageNameService,
            useValue: new TupleOfflineStorageNameService("peek_client")
        },
        // These have NAME dependencies
        TupleDataObserverService,
        TupleOfflineStorageService,
        TupleDataOfflineObserverService,
        // Device Info
        {
            provide: DeviceInfoService,
            useClass: DeviceInfoNsService
        },
    ]
})
export class AppNsModule {

}
