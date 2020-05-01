import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { MovieTableComponent } from './pages/movie-table/movie-table.component';


const routes: Routes = [
  { path: '**', component: MovieTableComponent },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
