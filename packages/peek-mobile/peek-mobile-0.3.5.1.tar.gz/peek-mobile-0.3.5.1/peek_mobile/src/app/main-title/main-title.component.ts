import {OnInit, OnDestroy} from "@angular/core";
import {ActivatedRoute} from "@angular/router";
import {Component} from "@angular/core";
import {TitleService, TitleBarLink} from "@synerty/peek-mobile-util";
import {VortexStatusService} from "@synerty/vortexjs";

@Component({
    selector: "peek-main-title",
    templateUrl: "main-title.component.web.html",
    moduleId: module.id
})
export class MainTitleComponent implements OnInit, OnDestroy {

    private subscriptions: any[] = [];

    private leftLinks = [];
    private rightLinks = [];

    title: string = "Peek";
    vortexIsOnline:boolean= false;

    constructor(vortexStatusService:VortexStatusService, titleService: TitleService) {
        this.leftLinks = titleService.leftLinksSnapshot;
        this.rightLinks = titleService.rightLinksSnapshot;

        this.subscriptions.push(
            titleService.title.subscribe(title => this.title = title));

        this.subscriptions.push(
            titleService.leftLinks.subscribe(links => this.leftLinks = links));

        this.subscriptions.push(
            titleService.rightLinks.subscribe(links => this.rightLinks = links));

        this.subscriptions.push(
            vortexStatusService.isOnline.subscribe(v => this.vortexIsOnline = v));

    }

    ngOnInit() {
    }

    ngOnDestroy() {
        while (this.subscriptions.length > 0)
            this.subscriptions.pop().unsubscribe();
    }

    // ------------------------------
    // Display methods

    linkTitle(title:TitleBarLink) {
        if (title.badgeCount == null) {
            return title.text;
        }

        if (title.left) {
            return `${title.text} (${title.badgeCount})`;
        }

        return `(${title.badgeCount}) ${title.text}`;

    }
}

