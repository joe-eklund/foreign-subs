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
}

const ELEMENT_DATA: VideoBase[] = [
  {position: 1, title: 'Thingy', imdb_id: 'Hydrogen', description: 'H'},
  {position: 2, title: 'Thingy', imdb_id: 'Helium', description: 'He'},
  {position: 3, title: 'Thingy', imdb_id: 'Lithium', description: 'Li'},
  {position: 4, title: 'Thingy', imdb_id: 'Beryllium', description: 'Be'},
  {position: 5, title: 'Thingy', imdb_id: 'Boron', description: 'B'},
  {position: 6, title: 'Thingy', imdb_id: 'Carbon', description: 'C'},
  {position: 7, title: 'Thingy', imdb_id: 'Nitrogen', description: 'N'},
  {position: 8, title: 'Thingy', imdb_id: 'Oxygen', description: 'O'},
  {position: 9, title: 'Thingy', imdb_id: 'Fluorine', description: 'F'},
  {position: 10, title: 'Thingy', imdb_id: 'Neon', description: 'Ne'},
];

@Component({
  selector: 'app-movie-table',
  templateUrl: './movie-table.component.html',
  styleUrls: ['./movie-table.component.scss']
})
export class MovieTableComponent implements OnInit {
  displayedColumns: string[] = ['select', 'position', 'name', 'weight', 'symbol', 'star'];
  dataSource = new MatTableDataSource(ELEMENT_DATA);
  selection = new SelectionModel<VideoBase>(true, []);

  name: string;
  animal: string;

  constructor(
    public dialog: MatDialog,
    private movieService: MoviesService,
  ) {}

  ngOnInit() {
    this.movieService.read().subscribe(res => {
      console.log(res);
    });
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
        this.dataSource.data.forEach(row => this.selection.select(row));
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

  openDialog(element): void {
    if (element == null) {
      element = {};
    }
    const dialogRef = this.dialog.open(ModifyMovieComponent, {
      width: '250px',
      data: element
    });

    dialogRef.afterClosed().subscribe(result => {
      console.log('The dialog was closed');
      this.animal = result;
    });
  }

}
