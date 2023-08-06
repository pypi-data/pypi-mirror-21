import {Component} from "@angular/core";
import {Router} from "@angular/router";
import {TitleService} from "@synerty/peek-mobile-util";
import {Ng2BalloonMsgService} from "@synerty/ng2-balloon-msg";
import {
    chatBaseUrl,
    ChatTuple,
    ChatUserTuple,
    CreateChatActionTuple
} from "@peek/peek_plugin_chat/_private";

import {UserService} from "@peek/peek_plugin_user";

import {
    ComponentLifecycleEventEmitter,
    TupleActionPushService,
    TupleDataObserverService,
    TupleSelector
} from "@synerty/vortexjs";
import {NewChatDialogData} from "./new-chat/new-chat.component";

@Component({
    selector: 'plugin-chat-chat-list',
    templateUrl: 'chat-list.component.mweb.html',
    moduleId: module.id
})
export class ChatListComponent extends ComponentLifecycleEventEmitter {

    chats: Array<ChatTuple> = [];

    newChatDialogData: NewChatDialogData = null;
    private userId: string;

    constructor(private balloonMsg: Ng2BalloonMsgService,
                private actionService: TupleActionPushService,
                private tupleDataObserver: TupleDataObserverService,
                private router: Router,
                private userService: UserService,
                titleService: TitleService) {
        super();
        titleService.setTitle("Chats");

        this.userId = userService.userDetails.userId;

        // Create the TupleSelector to tell the observable what data we want
        let tupleSelector = new TupleSelector(ChatTuple.tupleName, {
            userId: this.userId
        });

        // Setup a subscription for the data
        let sup = tupleDataObserver.subscribeToTupleSelector(tupleSelector)
            .subscribe((tuples: ChatTuple[]) => {
                // We've got new data, assign it to our class variable
                this.chats = tuples;
            });

        // unsubscribe when this component is destroyed
        // This is a feature of ComponentLifecycleEventEmitter
        this.onDestroyEvent.subscribe(() => sup.unsubscribe());

    }

    // ---- Data manipulation methods

    private createChat(data: NewChatDialogData) {
        let action = new CreateChatActionTuple();
        action.userIds = data.users.map((u) => u.userId);
        action.fromUserId = this.userService.loggedInUserDetails.userId;
        this.actionService.pushAction(action)
            .then(() => {
                this.balloonMsg.showSuccess("Chat Created");
            })
            .catch(err => alert(err));
    }


    // ---- User Input methods
    mainClicked() {
        this.router.navigate([chatBaseUrl]);
    }

    newChatClicked() {
        this.newChatDialogData = new NewChatDialogData();
    }

    chatClicked(chat) {
        this.router.navigate([chatBaseUrl, 'messages', chat.id]);
    }

    // ---- Display methods

    userDisplayName(chatUser: ChatUserTuple): string {
        return this.userService.userDisplayName(chatUser.userId);
    }

    isNewChatDialogShown(): boolean {
        return this.newChatDialogData != null;
    }

    otherChatUsers(chat: ChatTuple): ChatUserTuple[] {
        return chat.users.filter(cu => cu.userId != this.userId);
    }

    isChatRead(chat: ChatTuple): boolean {
        let chatUser = chat.users.filter(cu => cu.userId == this.userId)[0];
        return chat.lastActivity <= chatUser.lastReadDate;
    }

    dialogConfirmed(data: NewChatDialogData) {
        // Check if this is a unique chat.
        this.createChat(data);

        this.newChatDialogData = null;
    }

    dialogCanceled() {
        this.newChatDialogData = null;
    }

}