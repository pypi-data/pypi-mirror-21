import {Component, ElementRef, OnInit, ViewChild} from "@angular/core";
import {Ng2BalloonMsgService} from "@synerty/ng2-balloon-msg";
import {ActivatedRoute, Params, Router} from "@angular/router";
import {
    chatBaseUrl,
    ChatTuple,
    ChatUserReadActionTuple,
    ChatUserTuple,
    MessageTuple,
    SendMessageActionTuple
} from "@peek/peek_plugin_chat/_private";

import {TitleService} from "@synerty/peek-mobile-util";
import {UserService} from "@peek/peek_plugin_user";

import {
    ComponentLifecycleEventEmitter,
    TupleActionPushOfflineService,
    TupleActionPushService,
    TupleDataObserverService,
    TupleDataOfflineObserverService,
    TupleSelector
} from "@synerty/vortexjs";

import * as moment from "moment";

declare let NSIndexPath: any;
declare let UITableViewScrollPosition: any;

@Component({
    selector: 'plugin-chat-msg-list',
    templateUrl: 'msg-list.component.mweb.html',
    moduleId: module.id
})
export class MsgListComponent extends ComponentLifecycleEventEmitter implements OnInit {

    chat: ChatTuple = new ChatTuple();
    chatUser: ChatUserTuple | null = null;

    newMessageText: string = "";
    private userId: string;

    @ViewChild('messageListRef') messageListRef: ElementRef;

    constructor(private balloonMsg: Ng2BalloonMsgService,
                private actionService: TupleActionPushService,
                private tupleDataObserver: TupleDataObserverService,
                private tupleDataOfflineObserver: TupleDataOfflineObserverService,
                private tupleOfflineAction: TupleActionPushOfflineService,
                private route: ActivatedRoute,
                private router: Router,
                private userService: UserService,
                titleService: TitleService) {
        super();
        titleService.setTitle("Chat");

        this.userId = userService.userDetails.userId;
    }


    // ---- Data manipulation methods
    ngOnInit() {
        this.route.params.subscribe((params: Params) => {
            let chatId = parseInt(params['chatId']);
            this.loadChat(chatId);
        });

    }

    private loadChat(chatId: number) {


        let tupleSelector = new TupleSelector(ChatTuple.tupleName, {chatId: chatId});

        let sup = this.tupleDataOfflineObserver.subscribeToTupleSelector(tupleSelector)
            .subscribe((tuples: ChatTuple[]) => {
                if (tuples.length === 0)
                    return;

                this.chat = tuples[0];
                this.chatUser = this.chat.users.filter(
                    cu => cu.userId === this.userId)[0];
                setTimeout(() => this.scrollBottom(), 10);

                this.sendRead();
            });
        this.onDestroyEvent.subscribe(() => sup.unsubscribe());

    }

    // ---- Action Methods

    /** Tell the server that we've read this chat up to here.
     */
    private sendRead() {
        let action = new ChatUserReadActionTuple();
        action.chatUserId = this.chatUser.id;
        action.readDateTime = new Date();

        this.actionService.pushAction(action)
            .then(() => {

            })
            .catch((err) => {
                alert(err);
            });
    }

    private sendMessage(priority) {
        let action = new SendMessageActionTuple();
        action.chatId = this.chat.id;
        action.fromUserId = this.userService.userDetails.userId;
        action.message = this.newMessageText;
        action.priority = priority;

        this.actionService.pushAction(action)
            .then(() => {
                this.newMessageText = '';
                this.balloonMsg.showSuccess("Message Sent");

            })
            .catch((err) => {
                alert(err);
            });
    }

    // ---- Display methods
    messages(): MessageTuple[] {
        if (this.chat != null)
            return this.chat.messages;
        return [];
    }

    haveMessages(): boolean {
        return this.chat != null && this.chat.messages.length !== 0;
    }

    sendEnabled(): boolean {
        return this.newMessageText.length != 0;
    }

    isMessageFromThisUser(msg: MessageTuple): boolean {
        return msg.fromUserId == this.userService.userDetails.userId;
    }

    userDisplayName(msg: MessageTuple): string {
        return this.userService.userDisplayName(msg.fromUserId);
    }

    isNormalPriority(msg: MessageTuple): boolean {
        return msg.priority === MessageTuple.PRIORITY_NORMAL;
    }

    isEmergencyPriority(msg: MessageTuple): boolean {
        return msg.priority === MessageTuple.PRIORITY_EMERGENCY;
    }

    isFirstUnreadMesage(msgIndex: number): boolean {
        if (this.chat == null)
            return false;

        // If there are no messages, then false
        // though this method won't be called if this is the case
        if (this.chat.messages.length === 0)
            return false;

        let msg = this.chat.messages[msgIndex];

        // If we've read this message, then it's false.
        if (msg.dateTime <= this.chatUser.lastReadDate)
            return false;

        // From here on, msg is unread, we just need to work out if it's the first

        // If this is the first message...
        if (msgIndex === 0)
            return true;

        let lastMsg = this.chat.messages[msgIndex - 1];
        let lastIsRead = (lastMsg.dateTime <= this.chatUser.lastReadDate);

        // Now, if the last message is read, and this is unread (which it is),
        // then true, this is our first unread message
        if (lastIsRead)
            return true;

        return false;
    }

    dateTime(msg: MessageTuple) {
        return moment(msg.dateTime).format('HH:MM DD-MMM');
    }

    timePast(msg: MessageTuple) {
        return moment.duration(new Date().getTime() - msg.dateTime.getTime()).humanize();
    }

    // ---- scroll update
    private scrollBottom() {
        let position = this.messages().length - 1;
        let element = this.messageListRef.nativeElement;
        if (element["ios"] != null) {
            element["ios"].scrollToRowAtIndexPathAtScrollPositionAnimated(
                NSIndexPath.indexPathForItemInSection(position, 0),
                UITableViewScrollPosition.UITableViewScrollPositionTop,
                true
            );
        }
        else if (element["android"] != null) {
            element["android"].smoothScrollToPosition(position);
            //element.scrollToIndex(position);

        } else if (element["scrollTop"] != null) {
            element.scrollTop = element.scrollHeight;

        }
    }


    // ---- User Input methods
    navToChatsClicked() {
        this.router.navigate([chatBaseUrl, 'chats']);
    }

    sendMsgClicked() {
        this.sendMessage(MessageTuple.PRIORITY_NORMAL);
    }

    sendSosClicked() {
        let confirmResult = confirm("SEND SOS, Are you sure?");

        // On NativeScript, it returns a promise
        if (confirmResult["then"] != null) {
            confirmResult["then"]((result) => {
                if (result)
                    this.sendSos();
            })
        } else if (confirmResult) {
                this.sendSos();
        }
    }

    private sendSos() {
        if (this.newMessageText.length === 0)
            this.newMessageText = "SOS";

        this.sendMessage(MessageTuple.PRIORITY_EMERGENCY);
    }


}