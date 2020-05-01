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

}