import { Component, OnInit } from '@angular/core';
import { VideoBase } from '../movie-table/movie-table.component';
import { MoviesService } from 'src/app/core/services/movies.service';
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-movie',
  templateUrl: './movie.component.html',
  styleUrls: ['./movie.component.scss']
})
export class MovieComponent implements OnInit {

  movie: VideoBase;

  constructor(
    private moviesService: MoviesService,
    private activeRoute: ActivatedRoute,
  ) { }

  ngOnInit() {
    this.activeRoute.params.subscribe(params => {
      this.moviesService.read_one(params.id).subscribe(res => {
        this.movie = res;
      });
    });
  }

  save() {
    this.moviesService.update(this.movie.id, this.movie).subscribe(res => {
      console.log(res);
    });
  }

}
