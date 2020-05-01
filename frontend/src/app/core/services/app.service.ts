import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';

import { Observable, BehaviorSubject } from 'rxjs';

import { environment } from '../../../environments/environment';
import { map, catchError } from 'rxjs/operators';

@Injectable()
export class AppService {

  loadingWatcher = new BehaviorSubject<boolean>(false);
  loadingQueue = 0;

  constructor(
    private http: HttpClient,
  ) { }

  successMap = (res) => {
    this.loadingQueue--;
    if (this.loadingQueue === 0) {
      this.loadingWatcher.next(false);
    }
    return res;
  }

  errorMap = (err) => {
    this.loadingQueue--;
    if (this.loadingQueue === 0) {
      this.loadingWatcher.next(false);
    }
    throw err;
  }

  /**
   * sends an http get request to the provided url
   * @param url the url to get
   * @needs [functions] http.get, loadingWatcher.next
   * @returns Observable<any> (should have a list of objects in the response)
   */
  get(url: string): Observable<any> {
    this.loadingQueue++;
    this.loadingWatcher.next(true);
    return this.http.get(environment.apiUrl + '/' + url).pipe(
      map(this.successMap),
      catchError(this.errorMap));
  }

  /**
   * sends an http put request to the provided url with the object in the body of the request
   * @param url the url to get
   * @param obj the object to update
   * @needs [functions] http.put, loadingWatcher.next
   * @returns Observable<any> (should have the object updated in the response)
   */
  put(url: string, obj: any = {}): Observable<any> {
    this.loadingQueue++;
    this.loadingWatcher.next(true);
    return this.http.put(environment.apiUrl + '/' + url, obj).pipe(
      map(this.successMap),
      catchError(this.errorMap));
  }

  /**
   * sends an http post request to the provided url with the object in the body of the request
   * @param url the url to get
   * @param obj the object to update
   * @needs [functions] http.post, loadingWatcher.next
   * @returns Observable<any> (should have the object created in the response)
   */
  post(url: string, obj: any): Observable<any> {
    this.loadingQueue++;
    this.loadingWatcher.next(true);
    return this.http.post(environment.apiUrl + '/' + url, obj).pipe(
      map(this.successMap),
      catchError(this.errorMap));
  }

  /**
   * sends an http delete request to the provided url
   * @param url the url to delete
   * @param obj the body to give the request (usually used for bulk deleting)
   * @needs [functions] http.delete, loadingWatcher.next
   * @returns Observable<any> (should have the object deleted in the response)
   */
  delete(url: string, obj: any = null): Observable<any> {
    const options = {
      headers: new HttpHeaders({
        'Content-Type': 'application/json',
      }),
      body: obj,
    };
    this.loadingQueue++;
    this.loadingWatcher.next(true);
    return this.http.delete(environment.apiUrl + '/' + url, options).pipe(
      map(this.successMap),
      catchError(this.errorMap));
  }
}
