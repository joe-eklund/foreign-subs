import { Component, Inject } from '@angular/core';
import { MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { VideoBase } from '../movie-table.component';

@Component({
  selector: 'app-modify-movie',
  templateUrl: './modify-movie.component.html',
  styleUrls: ['./modify-movie.component.scss']
})
export class ModifyMovieComponent {

  constructor(
    public dialogRef: MatDialogRef<ModifyMovieComponent>,
    @Inject(MAT_DIALOG_DATA) public data: VideoBase
  ) {}

  onNoClick(): void {
    this.dialogRef.close();
  }

}
