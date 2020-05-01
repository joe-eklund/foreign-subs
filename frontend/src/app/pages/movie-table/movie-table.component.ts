import { Component, OnInit } from '@angular/core';
import { MatTableDataSource } from '@angular/material/table';
import { SelectionModel } from '@angular/cdk/collections';
import { MatDialog } from '@angular/material/dialog';
import { ModifyMovieComponent } from './modify-movie/modify-movie.component';
import { MoviesService } from 'src/app/core/services/movies.service';
import { Router } from '@angular/router';

export interface VideoBase {
  title: string;
  imdb_id: string;
  description: string;
  position: number;
  id: string;
}

@Component({
  selector: 'app-movie-table',
  templateUrl: './movie-table.component.html',
  styleUrls: ['./movie-table.component.scss']
})
export class MovieTableComponent implements OnInit {
  displayedColumns: string[] = ['position', 'title', 'imdb_id', 'description', 'star'];
  dataSource = new MatTableDataSource<VideoBase>();
  selection = new SelectionModel<VideoBase>(true, []);

  constructor(
    public dialog: MatDialog,
    private movieService: MoviesService,
    private router: Router,
  ) {}

  ngOnInit() {
    this.refresh();
  }

  applyFilter(event: Event) {
    const filterValue = (event.target as HTMLInputElement).value;
    this.dataSource.filter = filterValue.trim().toLowerCase();
  }

  refresh() {
    this.movieService.read().subscribe((res: VideoBase[]) => {
      this.dataSource = new MatTableDataSource(
        res.map((v: VideoBase, idx: number) => ({...v, position: idx + 1}))
      );
    });
  }

  openDialog(element): void {
    if (element == null) {
      element = {};
    }
    const dialogRef = this.dialog.open(ModifyMovieComponent, {
      width: '250px',
      data: element
    });

    dialogRef.afterClosed().subscribe((result: VideoBase) => {
      console.log(result);
      console.log('The dialog was closed');
      if (!result) {
        return;
      }
      if (result.id) {
        this.movieService.update(result.id, result).subscribe(res => {
          console.log('updated');
        });
      } else {
        this.movieService.create(result).subscribe(res => {
          this.refresh();
        });
      }
    });
  }

  viewSingle(element: VideoBase): void {
    this.router.navigate(['/movies/' + element.id]);
  }

  delete(element: VideoBase): void {
    this.movieService.delete(element.id).subscribe(res => {
      this.refresh();
    });
  }
}
