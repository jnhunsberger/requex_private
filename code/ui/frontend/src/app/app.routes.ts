import {Routes} from "@angular/router";
import {LstmComponent} from "./demo/lstm/lstm.component";

export const ROUTES: Routes = [
    // routes from pages
    {path: 'demo/lstm', component: LstmComponent, data: {title: 'LSTM'}},

    // default redirect
    {path: '**', redirectTo: '/home'}
];
