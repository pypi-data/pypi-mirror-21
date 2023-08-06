import {Component} from "@angular/core";
import {Router} from "@angular/router";
import {chatBaseUrl} from "@peek/peek_plugin_chat/_private";

@Component({
    selector: 'plugin-chat',
    templateUrl: 'chat.component.mweb.html',
    moduleId: module.id
})
export class ChatComponent {

    constructor(private router: Router) {

    }

    chatMsgClicked() {
        this.router.navigate([chatBaseUrl, 'chats']);
    }

}