import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { NavComponent } from './nav.component';
import { MatToolbarModule } from '@angular/material/toolbar';



@NgModule({
  declarations: [NavComponent],
  imports: [
    CommonModule,
    MatToolbarModule,
  ],
  exports: [NavComponent]
})
export class NavModule { }
