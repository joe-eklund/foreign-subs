import { Component, OnInit } from '@angular/core';
import { MatTableDataSource } from '@angular/material/table';
import { SelectionModel } from '@angular/cdk/collections';
import { MatDialog } from '@angular/material/dialog';
import { ModifyMovieComponent } from './modify-movie/modify-movie.component';
import { MoviesService } from 'src/app/core/services/movies.service';

export interface VideoBase {
  title: string;
  imdb_id: string;
  description: string;
  position: number;
  uri: string;
}

@Component({
  selector: 'app-movie-table',
  templateUrl: './movie-table.component.html',
  styleUrls: ['./movie-table.component.scss']
})
export class MovieTableComponent implements OnInit {
  displayedColumns: string[] = ['select', 'position', 'title', 'imdb_id', 'description', 'star'];
  dataSource = new MatTableDataSource();
  selection = new SelectionModel<VideoBase>(true, []);

  constructor(
    public dialog: MatDialog,
    private movieService: MoviesService,
  ) {}

  ngOnInit() {
    this.refresh();
  }

  /** Whether the number of selected elements matches the total number of rows. */
  isAllSelected() {
    const numSelected = this.selection.selected.length;
    const numRows = this.dataSource.data.length;
    return numSelected === numRows;
  }

  /** Selects all rows if they are not all selected; otherwise clear selection. */
  masterToggle() {
    this.isAllSelected() ?
        this.selection.clear() :
        this.dataSource.data.forEach((row: VideoBase) => this.selection.select(row));
  }

  /** The label for the checkbox on the passed row */
  checkboxLabel(row?: VideoBase): string {
    if (!row) {
      return `${this.isAllSelected() ? 'select' : 'deselect'} all`;
    }
    return `${this.selection.isSelected(row) ? 'deselect' : 'select'} row ${row.position + 1}`;
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
      if (result.uri) {
        this.movieService.update(result.uri, result).subscribe(res => {
          console.log('updated');
        });
      } else {
        this.movieService.create(result).subscribe(res => {
          this.refresh();
        });
      }
    });
  }

}
