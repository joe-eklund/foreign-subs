import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { HTTP_INTERCEPTORS, HttpClientModule } from '@angular/common/http';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { FooterModule } from './core/common/footer/footer.module';
import { LoaderModule } from './core/common/loader/loader.module';
import { NavModule } from './core/common/nav/nav.module';
import { AppService } from './core/services/app.service';
import { AuthInterceptor } from './core/services/interceptors/auth.service';

@NgModule({
  declarations: [
    AppComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    BrowserAnimationsModule,
    HttpClientModule,
    FooterModule,
    LoaderModule,
    NavModule
  ],
  providers: [
    AppService,
    {
      provide: HTTP_INTERCEPTORS,
      useClass: AuthInterceptor,
      multi: true
    },
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
