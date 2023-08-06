import {Routes} from "@angular/router";
import {LoggedInGuard} from "@peek/peek_plugin_user";
import {MsgListComponent} from "./msg-list/msg-list.component";
import {ChatListComponent} from "./chat-list/chat-list.component";
import {ChatComponent} from "./chat.component";


// Define the child routes for this plugin
export const pluginRoutes: Routes = [
    {
        path: 'messages/:chatId',
        component: MsgListComponent,
        canActivate: [LoggedInGuard]
    },
    {
        path: 'chats',
        component: ChatListComponent,
        canActivate: [LoggedInGuard]
    },
    {
        path: '',
        component: ChatListComponent,
        canActivate: [LoggedInGuard]
    },
    {
        path: '**',
        component: ChatListComponent,
        canActivate: [LoggedInGuard]
    }

];