import { HttpErrorResponse, HttpEvent, HttpHandler, HttpInterceptor, HttpRequest } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Router } from '@angular/router';
import { Observable } from 'rxjs';
import { map, catchError } from 'rxjs/operators';


@Injectable()
export class AuthInterceptor implements HttpInterceptor {

  newRequest: any;
  message = 'Oops, an error occured';

  constructor(
    private router: Router,
  ) {
  }

  /**
   * Adds the token stored in localStorage to every request,
   * ensures that all HTTPErrors are handled.
   * @param req the request being sent
   * @needs [functions] getToken, logout, router.navigate, toastrCtrl.error
   * @affects newRequest, message
   */
  intercept(req: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
    req = req.clone({
      // setHeaders: {
      //   Authorization: `Bearer ${this.getToken()}`
      // }
    });

    return next.handle(req).pipe(map(event => {
      // request handled successfully
      return this.newRequest = event;
    }), catchError((err, caught: Observable<HttpEvent<any>>) => {
      // request errored
      if (err instanceof HttpErrorResponse) {
        if (err.status === 401) {
          this.message = 'Unable to authenticate user. Please login again';
          this.logout();
        } else if (err.status === 400) {
          this.message = 'Invalid request. Please try again';
        } else if (err.status === 404) {
          this.message = 'Requested item not found.';
          this.router.navigate(['not-found']);
        } else if (err.status === 422) {
          this.message = 'There was a problem authenticating the user. Please login again';
          if (err.error.message.includes('Not enough segments')) {
            this.logout();
          }
        } else if (err.status === 413) {
          this.message = 'File exceeded 15MB limit.';
        } else if (err.status === 0) {
          this.message = 'Server is unreachable. Please try again later.';
        } else if (err.status === 500) {
          this.message = 'Internal Server Error. Click popup for more info.';
        } else if (err.status === 410) {
        } else {
          this.message = 'An error occurred';
        }
      }
      throw (err);
    }));
  }

  /**
   * Gets the token from localStorage
   * @needs [functions] localStorage.getItem
   * @returns the token from localstorage
   */
  getToken() {
    return localStorage.getItem('token');
  }

  /**
   * Logs the user out and redirects them to the login page
   * @needs [functions] localStorage.removeItem, router.navigate
   */
  logout() {
    localStorage.removeItem('token');
    localStorage.removeItem('currentUser');
    this.router.navigate(['/login']);
  }

}
