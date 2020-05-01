import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { AppService } from './app.service';

@Injectable({
  providedIn: 'root'
})
export class MoviesService {

  constructor(
    private appService: AppService,
  ) { }

  read(): Observable<any> {
    return this.appService.get('movies');
  }

  read_one(uri: string): Observable<any> {
    return this.appService.get('movies/' + uri);
  }

  create(movie: any): Observable<any> {
    return this.appService.post('movies', movie);
  }

  update(uri: string, data: any): Observable<any> {
    return this.appService.put('movies/' + uri, data);
  }

  delete(uri: string): Observable<any> {
    return this.appService.delete('movies/' + uri);
  }
}
