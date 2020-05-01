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

  read_one(id: string): Observable<any> {
    return this.appService.get('movies/' + id);
  }

  create(movie: any): Observable<any> {
    return this.appService.post('movies', movie);
  }

  update(id: string, movie: any): Observable<any> {
    return this.appService.put('movies/' + id, movie);
  }

  delete(id: string): Observable<any> {
    return this.appService.delete('movies/' + id);
  }

  read_versions(movieId): Observable<any> {
    return this.appService.get('movies/' + movieId + '/versions');
  }

  read_one_version(id): Observable<any> {
    return this.appService.get('movies/version');
  }

  create_version(movieId: string, version: any): Observable<any> {
    return this.appService.post('movies/' + movieId + '/versions', version);
  }

  update_version(id: string, version: any): Observable<any> {
    return this.appService.put('movies/versions/' + id, version);
  }

  delete_version(id: string): Observable<any> {
    return this.appService.delete('movies/versions/' + id);
  }
}
