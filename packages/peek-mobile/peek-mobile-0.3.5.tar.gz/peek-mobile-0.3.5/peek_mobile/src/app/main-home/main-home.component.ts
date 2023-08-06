import {Component} from "@angular/core";
import {OnInit} from "@angular/core";
import {
    ComponentLifecycleEventEmitter,
    Tuple,
    TupleDataOfflineObserverService,
    TupleSelector
} from "@synerty/vortexjs";
import {TitleService} from "@synerty/peek-mobile-util";
import {homeLinks} from "../../plugin-home-links";



@Component({
    selector: "peek-main-home",
    templateUrl: 'main-home.component.web.html',
    styleUrls: ['main-home.component.web.css'],
    moduleId: module.id
})
export class MainHomeComponent extends ComponentLifecycleEventEmitter implements OnInit {

    appDetails = homeLinks;

    constructor(tupleDataObserver: TupleDataOfflineObserverService, titleService: TitleService) {
        super();
        titleService.setTitle("Peek Home");

    }

    ngOnInit() {
    }

}
