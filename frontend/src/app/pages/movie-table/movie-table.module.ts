import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MovieTableComponent } from './movie-table.component';
import { MatTableModule } from '@angular/material/table';
import { SearchModule } from '../search/search.module';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatCheckboxModule } from '@angular/material/checkbox';
import { MatIconModule } from '@angular/material/icon';
import { MatMenuModule } from '@angular/material/menu';
import { MatButtonModule } from '@angular/material/button';
import { ModifyMovieComponent } from './modify-movie/modify-movie.component';
import { ReactiveFormsModule, FormsModule } from '@angular/forms';
import { MatDialogModule } from '@angular/material/dialog';


@NgModule({
  declarations: [MovieTableComponent, ModifyMovieComponent],
  imports: [
    CommonModule,
    MatTableModule,
    SearchModule,
    MatFormFieldModule,
    MatInputModule,
    MatCheckboxModule,
    MatIconModule,
    MatMenuModule,
    MatButtonModule,
    MatDialogModule,
    FormsModule,
    ReactiveFormsModule,
  ]
})
export class MovieTableModule { }
