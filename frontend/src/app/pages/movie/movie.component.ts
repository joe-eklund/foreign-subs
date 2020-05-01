import { Component, OnInit } from '@angular/core';
import { VideoBase } from '../movie-table/movie-table.component';
import { MoviesService } from 'src/app/core/services/movies.service';
import { ActivatedRoute } from '@angular/router';
import { MatDialog } from '@angular/material/dialog';
import { VersionComponent, Version } from './version/version.component';
import { MatTableDataSource } from '@angular/material/table';
import { SelectionModel } from '@angular/cdk/collections';

@Component({
  selector: 'app-movie',
  templateUrl: './movie.component.html',
  styleUrls: ['./movie.component.scss']
})
export class MovieComponent implements OnInit {

  movie: VideoBase;
  displayedColumns: string[] = [
    'position', 'disc_type', 'sub_type', 'timestamps', 'track', 'star'
  ];
  dataSource = new MatTableDataSource<Version>();
  selection = new SelectionModel<Version>(true, []);

  constructor(
    public dialog: MatDialog,
    private moviesService: MoviesService,
    private activeRoute: ActivatedRoute,
  ) { }

  ngOnInit() {
    this.activeRoute.params.subscribe(params => {
      this.moviesService.read_one(params.id).subscribe(res => {
        this.movie = res;
        this.refresh();
      });
    });
  }

  save() {
    this.moviesService.update(this.movie.id, this.movie).subscribe(res => {
      console.log(res);
    });
  }

  editVersion(movieId: string, version: Version): void {
    const dialogRef = this.dialog.open(VersionComponent, {
      width: '250px',
      data: version ? version : {}
    });

    dialogRef.afterClosed().subscribe((result: Version) => {
      console.log('The dialog was closed');
      if (!result) {
        return;
      }
      if (result.id) {
        this.moviesService.update_version(result.id, result).subscribe(res => {
          console.log('updated');
        });
      } else {
        this.moviesService.create_version(movieId, result).subscribe(res => {
          this.refresh();
        });
      }
    });
  }

  applyFilter(event: Event) {
    const filterValue = (event.target as HTMLInputElement).value;
    this.dataSource.filter = filterValue.trim().toLowerCase();
  }

  refresh() {
    this.moviesService.read_versions(this.movie.id).subscribe((res: Version[]) => {
      this.dataSource = new MatTableDataSource(
        res.map((v: Version, idx: number) => ({...v, position: idx + 1}))
      );
    });
  }

  delete(element: VideoBase): void {
    this.moviesService.delete(element.id).subscribe(res => {
      this.refresh();
    });
  }

}
