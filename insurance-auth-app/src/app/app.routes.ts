import { Routes } from '@angular/router';
import { SignUpComponent } from './sign-up/sign-up.component';
import { SignInComponent } from './sign-in/sign-in.component';
import { RequestSubmissionComponent } from './request-submission.component';
import { HistoryComponent } from './history.component';

export const appRoutes: Routes = [
  { path: 'sign-up', component: SignUpComponent },
  { path: 'sign-in', component: SignInComponent },
  { path: 'request', component: RequestSubmissionComponent },
  { path: 'history', component: HistoryComponent },
  { path: '', redirectTo: '/sign-in', pathMatch: 'full' } // Default route
];
