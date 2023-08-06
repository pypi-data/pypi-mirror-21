import {Component, OnInit} from "@angular/core";
import {ComponentLifecycleEventEmitter, Tuple, VortexService} from "@synerty/vortexjs";
import {
    dashboardRoute,
    environmentRoute,
    settingRoute,
    updateRoute
} from "../app-routing.module";
import {homeLinks} from "../../plugin-home-links";


class UserTuple extends Tuple {
    constructor() {
        super('peek_server.PeekAdmNavbarUserTuple');
    }

    supportExceeded: boolean = false;
    demoExceeded: boolean = true;
    countsExceeded: boolean = true;
    username: string = "None";
}


@Component({
    selector: 'app-navbar',
    templateUrl: './navbar.component.html',
    styleUrls: ['./navbar.component.css']
})
export class NavbarComponent extends ComponentLifecycleEventEmitter implements OnInit {

    // -------------- Load User Details
    private readonly userDataFilt = {
        plugin: 'peek_server',
        key: "nav.adm.user.data"
    };

    dashboardPath: string = dashboardRoute.path;
    settingPath: string = settingRoute.path;
    environmentPath: string = environmentRoute.path;
    updatePath: string = updateRoute.path;

    user: UserTuple = new UserTuple();

    // ----------- Load Plugin Menu Items
    // Make it public because AppRouterModule uses it as well
    pluginsMenuData = homeLinks;


    constructor(private vortexService: VortexService) {
        super();
    }

    ngOnInit() {

        this.vortexService.createTupleLoader(this, this.userDataFilt)
            .observable.subscribe(tuples => this.user = <UserTuple>tuples[0]);

    }


}
