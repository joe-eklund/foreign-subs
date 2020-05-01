import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { LoaderComponent } from './loader.component';
import { MatProgressBarModule } from '@angular/material/progress-bar';



@NgModule({
  declarations: [LoaderComponent],
  imports: [
    CommonModule,
    MatProgressBarModule
  ],
  exports: [LoaderComponent]
})
export class LoaderModule { }
