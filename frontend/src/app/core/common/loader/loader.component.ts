import { Component, OnInit } from '@angular/core';
import { Subject } from 'rxjs';
import { AppService } from 'src/app/core/services/app.service';

@Component({
  selector: 'app-loader',
  templateUrl: './loader.component.html',
  styleUrls: ['./loader.component.scss']
})
export class LoaderComponent implements OnInit {

  loading: Subject<boolean> = this.appService.loadingWatcher;

  constructor(
    private appService: AppService
  ) { }

  ngOnInit() {
  }

}
