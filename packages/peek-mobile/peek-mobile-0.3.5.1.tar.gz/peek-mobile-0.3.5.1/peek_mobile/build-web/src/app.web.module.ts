// Angular
import {BrowserModule} from "@angular/platform-browser";
import {BrowserAnimationsModule} from "@angular/platform-browser/animations";

import {NgModule} from "@angular/core";
import {HttpModule} from "@angular/http";
import {RouterModule} from "@angular/router";
// @synerty
import {Ng2BalloonMsgModule} from "@synerty/ng2-balloon-msg/index.web";
import {
    DeviceInfoService,
    DeviceInfoWebService,
    PeekModuleFactory
} from "@synerty/peek-mobile-util/index.web";
import {
    TupleDataObservableNameService,
    TupleDataObserverService,
    TupleDataOfflineObserverService,
    TupleOfflineStorageNameService,
    TupleOfflineStorageService,
    WebSqlFactoryService
} from "@synerty/vortexjs";
import {WebSqlBrowserFactoryService} from "@synerty/vortexjs/index-browser";
// Routes
import {staticRoutes} from "./app/app.routes";
import {peekRootServices} from "./app/app.services";
// This app
import {AppComponent} from "./app/app.component";
import {MainHomeComponent} from "./app/main-home/main-home.component";
import {MainTitleComponent} from "./app/main-title/main-title.component";
import {UnknownRouteComponent} from "./app/unknown-route/unknown-route.component";
import {pluginRootModules} from "./plugin-root-modules";
import {pluginRootServices} from "./plugin-root-services";

export function tupleDataObservableNameServiceFactory() {
    return new TupleDataObservableNameService("peek_client", {"plugin": "peek_client"});
}

export function tupleOfflineStorageNameServiceFactory() {
    return new TupleOfflineStorageNameService("peek_client");
}


@NgModule({
    declarations: [AppComponent,
        MainTitleComponent,
        MainHomeComponent,
        UnknownRouteComponent],
    bootstrap: [AppComponent],
    imports: [
        RouterModule,
        PeekModuleFactory.RouterModule.forRoot(staticRoutes),
        BrowserModule,
        BrowserAnimationsModule,
        ...PeekModuleFactory.FormsModules,
        HttpModule,
        Ng2BalloonMsgModule,
        ...pluginRootModules
    ],
    providers: [
        {provide: WebSqlFactoryService, useClass: WebSqlBrowserFactoryService},
        ...peekRootServices,
        ...pluginRootServices,

        // Use the TupleDataObserver services, with offline storage
        {
            provide: TupleDataObservableNameService,
            useFactory: tupleDataObservableNameServiceFactory
        }, {
            provide: TupleOfflineStorageNameService,
            useFactory: tupleOfflineStorageNameServiceFactory
        },
        // These have NAME dependencies
        TupleDataObserverService,
        TupleOfflineStorageService,
        TupleDataOfflineObserverService,
        // Device Info
        {
            provide: DeviceInfoService,
            useClass: DeviceInfoWebService
        },
    ]
})
export class AppWebModule {

}
