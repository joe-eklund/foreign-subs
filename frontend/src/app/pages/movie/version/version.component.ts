import { Component, Inject } from '@angular/core';
import { MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';

export interface Version {
  video_base_id: string;
  disc_type: string;
  timestamps: string[];
  description: string;
  track: number;
  id: string;
}

@Component({
  selector: 'app-version',
  templateUrl: './version.component.html',
  styleUrls: ['./version.component.scss']
})
export class VersionComponent {

  constructor(
    public dialogRef: MatDialogRef<VersionComponent>,
    @Inject(MAT_DIALOG_DATA) public data: Version
  ) {}

  onNoClick(): void {
    this.dialogRef.close();
  }

  addTimeStamp(data: KeyboardEvent) {
    if (this.data.timestamps) {
      return this.data.timestamps.push(data.target.value);
    }
    this.data.timestamps = [data.target.value];
  }

  removeTimeStamp(idx) {
    this.data.timestamps.splice(idx, 1);
  }

}
